from fastapi import APIRouter, Depends, HTTPException
from app.routers.auth import get_current_admin_user
from app.database.database import get_db
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[dict])
async def get_all_users(db = Depends(get_db), 
                       current_user: dict = Depends(get_current_admin_user)):
    """Get all users (admin only)"""
    cursor = await db.execute("""
        SELECT id, username, email, is_admin, rating, created_at
        FROM users
        ORDER BY created_at DESC
    """)
    users = await cursor.fetchall()
    return [dict(user) for user in users]

@router.put("/users/{user_id}/admin", response_model=dict)
async def toggle_admin(user_id: int, is_admin: bool, db = Depends(get_db),
                      current_user: dict = Depends(get_current_admin_user)):
    """Toggle admin status for a user (admin only)"""
    await db.execute("UPDATE users SET is_admin = ? WHERE id = ?", (is_admin, user_id))
    await db.commit()
    return {"message": "User admin status updated"}

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db = Depends(get_db),
                     current_user: dict = Depends(get_current_admin_user)):
    """Delete a user (admin only)"""
    if user_id == current_user["id"]:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    await db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    await db.commit()
    return {"message": "User deleted"}

@router.get("/stats", response_model=dict)
async def get_admin_stats(db = Depends(get_db),
                         current_user: dict = Depends(get_current_admin_user)):
    """Get platform statistics (admin only)"""
    # Total users
    cursor = await db.execute("SELECT COUNT(*) as count FROM users")
    users_count = (await cursor.fetchone())["count"]
    
    # Total courses
    cursor = await db.execute("SELECT COUNT(*) as count FROM courses")
    courses_count = (await cursor.fetchone())["count"]
    
    # Total puzzles
    cursor = await db.execute("SELECT COUNT(*) as count FROM puzzles")
    puzzles_count = (await cursor.fetchone())["count"]
    
    # Total games
    cursor = await db.execute("SELECT COUNT(*) as count FROM games")
    games_count = (await cursor.fetchone())["count"]
    
    # Total purchases
    cursor = await db.execute("SELECT COUNT(*) as count, SUM(amount) as revenue FROM purchases")
    purchase_stats = await cursor.fetchone()
    
    return {
        "users": users_count,
        "courses": courses_count,
        "puzzles": puzzles_count,
        "games": games_count,
        "purchases": purchase_stats["count"] if purchase_stats else 0,
        "revenue": purchase_stats["revenue"] if purchase_stats and purchase_stats["revenue"] else 0
    }

@router.get("/leaderboard", response_model=List[dict])
async def get_leaderboard(limit: int = 10, db = Depends(get_db)):
    """Get top users by rating"""
    cursor = await db.execute("""
        SELECT id, username, rating
        FROM users
        ORDER BY rating DESC
        LIMIT ?
    """, (limit,))
    users = await cursor.fetchall()
    return [dict(user) for user in users]
