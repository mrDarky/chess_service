from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import Puzzle, PuzzleCreate, PuzzleAttempt, PuzzleAttemptBase
from app.routers.auth import get_current_user, get_current_admin_user
from app.database.database import get_db
from typing import List

router = APIRouter(prefix="/puzzles", tags=["puzzles"])

@router.get("/", response_model=List[dict])
async def get_puzzles(difficulty: str = None, db = Depends(get_db)):
    """Get all puzzles, optionally filtered by difficulty"""
    if difficulty:
        cursor = await db.execute(
            "SELECT * FROM puzzles WHERE difficulty = ? ORDER BY rating",
            (difficulty,)
        )
    else:
        cursor = await db.execute("SELECT * FROM puzzles ORDER BY rating")
    puzzles = await cursor.fetchall()
    return [dict(puzzle) for puzzle in puzzles]

@router.get("/{puzzle_id}", response_model=dict)
async def get_puzzle(puzzle_id: int, db = Depends(get_db)):
    """Get a specific puzzle"""
    cursor = await db.execute("SELECT * FROM puzzles WHERE id = ?", (puzzle_id,))
    puzzle = await cursor.fetchone()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return dict(puzzle)

@router.post("/", response_model=dict)
async def create_puzzle(puzzle: PuzzleCreate, db = Depends(get_db),
                        current_user: dict = Depends(get_current_admin_user)):
    """Create a new puzzle (admin only)"""
    cursor = await db.execute(
        """INSERT INTO puzzles (title, fen, solution, difficulty, category_id, rating)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (puzzle.title, puzzle.fen, puzzle.solution, puzzle.difficulty, 
         puzzle.category_id, puzzle.rating)
    )
    await db.commit()
    return {"message": "Puzzle created", "id": cursor.lastrowid}

@router.put("/{puzzle_id}", response_model=dict)
async def update_puzzle(puzzle_id: int, puzzle: PuzzleCreate, db = Depends(get_db),
                        current_user: dict = Depends(get_current_admin_user)):
    """Update a puzzle (admin only)"""
    await db.execute(
        """UPDATE puzzles 
           SET title = ?, fen = ?, solution = ?, difficulty = ?, category_id = ?, rating = ?
           WHERE id = ?""",
        (puzzle.title, puzzle.fen, puzzle.solution, puzzle.difficulty,
         puzzle.category_id, puzzle.rating, puzzle_id)
    )
    await db.commit()
    return {"message": "Puzzle updated"}

@router.delete("/{puzzle_id}", response_model=dict)
async def delete_puzzle(puzzle_id: int, db = Depends(get_db),
                        current_user: dict = Depends(get_current_admin_user)):
    """Delete a puzzle (admin only)"""
    await db.execute("DELETE FROM puzzles WHERE id = ?", (puzzle_id,))
    await db.commit()
    return {"message": "Puzzle deleted"}

@router.post("/attempt", response_model=dict)
async def submit_puzzle_attempt(attempt: PuzzleAttemptBase, db = Depends(get_db),
                                current_user: dict = Depends(get_current_user)):
    """Submit a puzzle attempt"""
    cursor = await db.execute(
        """INSERT INTO puzzle_attempts (user_id, puzzle_id, success, time_taken)
           VALUES (?, ?, ?, ?)""",
        (current_user["id"], attempt.puzzle_id, attempt.success, attempt.time_taken)
    )
    await db.commit()
    
    # Update user rating if successful
    if attempt.success:
        new_rating = current_user["rating"] + 10
        await db.execute("UPDATE users SET rating = ? WHERE id = ?",
                        (new_rating, current_user["id"]))
        await db.execute(
            "INSERT INTO rating_history (user_id, rating, change, reason) VALUES (?, ?, ?, ?)",
            (current_user["id"], new_rating, 10, f"Solved puzzle {attempt.puzzle_id}")
        )
        await db.commit()
    
    return {"message": "Attempt recorded", "success": attempt.success}

@router.get("/my/attempts", response_model=List[dict])
async def get_my_attempts(db = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get user's puzzle attempts"""
    cursor = await db.execute("""
        SELECT pa.*, p.title as puzzle_title, p.difficulty
        FROM puzzle_attempts pa
        JOIN puzzles p ON pa.puzzle_id = p.id
        WHERE pa.user_id = ?
        ORDER BY pa.created_at DESC
        LIMIT 50
    """, (current_user["id"],))
    attempts = await cursor.fetchall()
    return [dict(attempt) for attempt in attempts]
