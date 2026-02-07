from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import Course, CourseCreate, Purchase, PurchaseCreate
from app.routers.auth import get_current_user, get_current_admin_user
from app.database.database import get_db
from typing import List

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/", response_model=List[dict])
async def get_courses(db = Depends(get_db)):
    """Get all courses"""
    cursor = await db.execute("""
        SELECT c.*, cat.name as category_name 
        FROM courses c
        LEFT JOIN categories cat ON c.category_id = cat.id
        ORDER BY c.created_at DESC
    """)
    courses = await cursor.fetchall()
    return [dict(course) for course in courses]

@router.get("/{course_id}", response_model=dict)
async def get_course(course_id: int, db = Depends(get_db)):
    """Get a specific course"""
    cursor = await db.execute("""
        SELECT c.*, cat.name as category_name 
        FROM courses c
        LEFT JOIN categories cat ON c.category_id = cat.id
        WHERE c.id = ?
    """, (course_id,))
    course = await cursor.fetchone()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return dict(course)

@router.post("/", response_model=dict)
async def create_course(course: CourseCreate, db = Depends(get_db), 
                        current_user: dict = Depends(get_current_admin_user)):
    """Create a new course (admin only)"""
    cursor = await db.execute(
        """INSERT INTO courses (title, description, price, category_id, difficulty) 
           VALUES (?, ?, ?, ?, ?)""",
        (course.title, course.description, course.price, course.category_id, course.difficulty)
    )
    await db.commit()
    return {"message": "Course created", "id": cursor.lastrowid}

@router.put("/{course_id}", response_model=dict)
async def update_course(course_id: int, course: CourseCreate, db = Depends(get_db),
                        current_user: dict = Depends(get_current_admin_user)):
    """Update a course (admin only)"""
    await db.execute(
        """UPDATE courses 
           SET title = ?, description = ?, price = ?, category_id = ?, difficulty = ?
           WHERE id = ?""",
        (course.title, course.description, course.price, course.category_id, 
         course.difficulty, course_id)
    )
    await db.commit()
    return {"message": "Course updated"}

@router.delete("/{course_id}", response_model=dict)
async def delete_course(course_id: int, db = Depends(get_db),
                        current_user: dict = Depends(get_current_admin_user)):
    """Delete a course (admin only)"""
    await db.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    await db.commit()
    return {"message": "Course deleted"}

@router.post("/purchase/{course_id}", response_model=dict)
async def purchase_course(course_id: int, db = Depends(get_db),
                         current_user: dict = Depends(get_current_user)):
    """Purchase a course"""
    # Check if course exists
    cursor = await db.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
    course = await cursor.fetchone()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if already purchased
    cursor = await db.execute(
        "SELECT * FROM purchases WHERE user_id = ? AND course_id = ?",
        (current_user["id"], course_id)
    )
    if await cursor.fetchone():
        raise HTTPException(status_code=400, detail="Course already purchased")
    
    # Create purchase
    cursor = await db.execute(
        "INSERT INTO purchases (user_id, course_id, amount) VALUES (?, ?, ?)",
        (current_user["id"], course_id, course["price"])
    )
    await db.commit()
    return {"message": "Course purchased successfully", "purchase_id": cursor.lastrowid}

@router.get("/my/purchases", response_model=List[dict])
async def get_my_purchases(db = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get user's purchased courses"""
    cursor = await db.execute("""
        SELECT c.*, p.purchased_at, p.amount
        FROM purchases p
        JOIN courses c ON p.course_id = c.id
        WHERE p.user_id = ?
        ORDER BY p.purchased_at DESC
    """, (current_user["id"],))
    purchases = await cursor.fetchall()
    return [dict(purchase) for purchase in purchases]
