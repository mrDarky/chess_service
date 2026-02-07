from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import Game, GameBase
from app.routers.auth import get_current_user
from app.database.database import get_db
from typing import List

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/", response_model=dict)
async def create_game(game: GameBase, db = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    """Create a new game record"""
    cursor = await db.execute(
        """INSERT INTO games (user_id, game_type, result, moves, duration)
           VALUES (?, ?, ?, ?, ?)""",
        (current_user["id"], game.game_type, game.result, game.moves, game.duration)
    )
    await db.commit()
    
    # Update rating based on result
    if game.result:
        rating_change = 0
        if game.result == "win":
            rating_change = 20
        elif game.result == "loss":
            rating_change = -15
        elif game.result == "draw":
            rating_change = 5
        
        if rating_change != 0:
            new_rating = max(0, current_user["rating"] + rating_change)
            await db.execute("UPDATE users SET rating = ? WHERE id = ?",
                           (new_rating, current_user["id"]))
            await db.execute(
                "INSERT INTO rating_history (user_id, rating, change, reason) VALUES (?, ?, ?, ?)",
                (current_user["id"], new_rating, rating_change, 
                 f"{game.game_type} - {game.result}")
            )
            await db.commit()
    
    return {"message": "Game recorded", "id": cursor.lastrowid}

@router.get("/my", response_model=List[dict])
async def get_my_games(limit: int = 20, db = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    """Get user's game history"""
    cursor = await db.execute("""
        SELECT * FROM games
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (current_user["id"], limit))
    games = await cursor.fetchall()
    return [dict(game) for game in games]

@router.get("/stats", response_model=dict)
async def get_stats(db = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get user's game statistics"""
    cursor = await db.execute("""
        SELECT 
            COUNT(*) as total_games,
            SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as losses,
            SUM(CASE WHEN result = 'draw' THEN 1 ELSE 0 END) as draws
        FROM games
        WHERE user_id = ?
    """, (current_user["id"],))
    stats = await cursor.fetchone()
    
    # Get puzzle stats
    cursor = await db.execute("""
        SELECT 
            COUNT(*) as total_attempts,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
        FROM puzzle_attempts
        WHERE user_id = ?
    """, (current_user["id"],))
    puzzle_stats = await cursor.fetchone()
    
    return {
        "games": dict(stats) if stats else {},
        "puzzles": dict(puzzle_stats) if puzzle_stats else {},
        "rating": current_user["rating"]
    }
