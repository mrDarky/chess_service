from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import Category, CategoryCreate
from app.routers.auth import get_current_admin_user
from app.database.database import get_db
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[dict])
async def get_categories(db = Depends(get_db)):
    """Get all categories"""
    cursor = await db.execute("SELECT * FROM categories ORDER BY name")
    categories = await cursor.fetchall()
    return [dict(cat) for cat in categories]

@router.get("/{category_id}", response_model=dict)
async def get_category(category_id: int, db = Depends(get_db)):
    """Get a specific category"""
    cursor = await db.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
    category = await cursor.fetchone()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return dict(category)

@router.post("/", response_model=dict)
async def create_category(category: CategoryCreate, db = Depends(get_db),
                         current_user: dict = Depends(get_current_admin_user)):
    """Create a new category (admin only)"""
    cursor = await db.execute(
        "INSERT INTO categories (name, description) VALUES (?, ?)",
        (category.name, category.description)
    )
    await db.commit()
    return {"message": "Category created", "id": cursor.lastrowid}

@router.put("/{category_id}", response_model=dict)
async def update_category(category_id: int, category: CategoryCreate, db = Depends(get_db),
                         current_user: dict = Depends(get_current_admin_user)):
    """Update a category (admin only)"""
    await db.execute(
        "UPDATE categories SET name = ?, description = ? WHERE id = ?",
        (category.name, category.description, category_id)
    )
    await db.commit()
    return {"message": "Category updated"}

@router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: int, db = Depends(get_db),
                         current_user: dict = Depends(get_current_admin_user)):
    """Delete a category (admin only)"""
    await db.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    await db.commit()
    return {"message": "Category deleted"}
