from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    rating: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 0.0
    category_id: Optional[int] = None
    difficulty: str = "beginner"

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PuzzleBase(BaseModel):
    title: str
    fen: str
    solution: str
    difficulty: str = "easy"
    category_id: Optional[int] = None
    rating: int = 1200

class PuzzleCreate(PuzzleBase):
    pass

class Puzzle(PuzzleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class GameBase(BaseModel):
    game_type: str
    result: Optional[str] = None
    moves: Optional[str] = None
    duration: Optional[int] = None

class GameCreate(GameBase):
    user_id: int

class Game(GameBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PuzzleAttemptBase(BaseModel):
    puzzle_id: int
    success: bool
    time_taken: Optional[int] = None

class PuzzleAttemptCreate(PuzzleAttemptBase):
    user_id: int

class PuzzleAttempt(PuzzleAttemptBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    course_id: int
    amount: float

class PurchaseCreate(PurchaseBase):
    user_id: int

class Purchase(PurchaseBase):
    id: int
    user_id: int
    purchased_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
