# Chess Training Platform - Setup Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/mrDarky/chess_service.git
cd chess_service
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

5. **Run the application**
```bash
python main.py
```

6. **Access the platform**
Open your browser and navigate to: `http://localhost:8000`

## Creating an Admin User

### Method 1: Using Python Script
```python
import asyncio
import aiosqlite
from app.auth import get_password_hash

async def create_admin():
    db = await aiosqlite.connect('chess_service.db')
    hashed_password = get_password_hash('your_password')
    await db.execute(
        "INSERT INTO users (username, email, hashed_password, is_admin) VALUES (?, ?, ?, ?)",
        ('admin', 'admin@example.com', hashed_password, 1)
    )
    await db.commit()
    await db.close()

asyncio.run(create_admin())
```

### Method 2: Using SQLite Command Line
```bash
sqlite3 chess_service.db
UPDATE users SET is_admin = 1 WHERE username = 'your_username';
.quit
```

## Sample Data

To populate the database with sample data for testing:

```python
import asyncio
import aiosqlite
from app.auth import get_password_hash

async def create_sample_data():
    db = await aiosqlite.connect('chess_service.db')
    
    # Create categories
    categories = [
        ('Tactics', 'Tactical puzzles and exercises'),
        ('Openings', 'Opening theory and practice'),
        ('Endgames', 'Endgame techniques and strategies')
    ]
    for name, desc in categories:
        await db.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (name, desc)
        )
    
    # Create courses
    courses = [
        ('Beginner Chess Tactics', 'Learn fundamental tactical patterns', 29.99, 1, 'beginner'),
        ('Mastering the Sicilian Defense', 'Complete guide to the Sicilian', 49.99, 2, 'intermediate'),
    ]
    for title, desc, price, cat_id, diff in courses:
        await db.execute(
            "INSERT INTO courses (title, description, price, category_id, difficulty) VALUES (?, ?, ?, ?, ?)",
            (title, desc, price, cat_id, diff)
        )
    
    # Create puzzles
    puzzles = [
        ('Knight Fork', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'Nf3', 'easy', 1, 1000),
        ('Back Rank Mate', 'r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1', 'Bxf7+', 'medium', 1, 1300),
    ]
    for title, fen, sol, diff, cat_id, rating in puzzles:
        await db.execute(
            "INSERT INTO puzzles (title, fen, solution, difficulty, category_id, rating) VALUES (?, ?, ?, ?, ?, ?)",
            (title, fen, sol, diff, cat_id, rating)
        )
    
    await db.commit()
    await db.close()
    print("Sample data created!")

asyncio.run(create_sample_data())
```

## API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Common Issues

### Port Already in Use
If port 8000 is already in use, modify the port in `main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Change port here
```

### Database Locked
If you get a "database is locked" error:
- Ensure no other instances of the application are running
- Close any SQLite browser tools that may have the database open
- Restart the application

### Missing Dependencies
If you encounter import errors:
```bash
pip install -r requirements.txt --upgrade
```

## Production Deployment

### Security Checklist
- [ ] Change SECRET_KEY in .env to a strong random value
- [ ] Use HTTPS (SSL/TLS certificate)
- [ ] Set up proper CORS configuration
- [ ] Implement rate limiting
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Enable logging and monitoring
- [ ] Add SRI hashes to CDN scripts

### Environment Variables
```bash
SECRET_KEY=your-production-secret-key-here
DATABASE_URL=sqlite+aiosqlite:///./chess_service.db
```

### Using Gunicorn (Production Server)
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Features Overview

### For Students
1. Register and create an account
2. Solve chess puzzles to improve tactics
3. Practice blind play for visualization
4. Purchase and access courses
5. Track progress on dashboard
6. Compete on the leaderboard

### For Admins
1. Access admin panel at `/admin-panel`
2. Manage users and permissions
3. Create and edit courses
4. Add puzzles with FEN positions
5. Organize content with categories
6. View platform statistics

## Support

For issues or questions:
- GitHub Issues: https://github.com/mrDarky/chess_service/issues
- Documentation: See README.md

## License

MIT License - See LICENSE file for details
