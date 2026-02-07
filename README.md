# Chess Training Platform

A comprehensive chess training platform built with FastAPI, Bootstrap 5, and SQLite. The platform offers various training modes including puzzles, blind play, and professional courses with a rating system and admin panel.

## Features

### User Features
- 🎯 **Chess Puzzles**: Solve tactical puzzles to improve pattern recognition
- 👁️ **Blind Play**: Train visualization skills by playing without seeing the board
- 📚 **Course Catalog**: Browse and purchase professional chess courses
- ⭐ **Rating System**: Track your progress with a personal rating
- 🏆 **Leaderboard**: Compete with other players globally
- 📊 **Statistics Dashboard**: View detailed statistics of your games and puzzle attempts
- 🎓 **Multiple Categories**: Courses and puzzles organized by categories and difficulty levels

### Admin Features
- 👥 **User Management**: View, edit, and delete users
- 📝 **Content Management**: Create and manage courses, puzzles, and categories
- 📈 **Analytics Dashboard**: View platform statistics and revenue
- 🔒 **Role Management**: Assign admin privileges to users

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with async support (aiosqlite)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Authentication**: JWT tokens with bcrypt password hashing
- **Chess Logic**: chess.js and chessboard.js libraries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mrDarky/chess_service.git
cd chess_service
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Edit `.env` and set your secret key:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite+aiosqlite:///./chess_service.db
```

## Running the Application

1. Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. The database will be automatically initialized on first run.

## Creating an Admin User

To create an admin user, you need to register a normal user first, then update the database:

1. Register a user through the web interface at `/register`

2. Update the user to admin via SQLite:
```bash
sqlite3 chess_service.db
UPDATE users SET is_admin = 1 WHERE username = 'your_username';
.quit
```

Or create a simple Python script:
```python
import asyncio
import aiosqlite

async def make_admin(username):
    db = await aiosqlite.connect('chess_service.db')
    await db.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (username,))
    await db.commit()
    await db.close()
    print(f"User {username} is now an admin")

asyncio.run(make_admin('your_username'))
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
chess_service/
├── app/
│   ├── database/
│   │   └── database.py        # Database setup and initialization
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── routers/
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── courses.py        # Course management
│   │   ├── puzzles.py        # Puzzle management
│   │   ├── games.py          # Game tracking
│   │   ├── categories.py     # Category management
│   │   └── admin.py          # Admin panel endpoints
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Custom styles
│   │   └── js/
│   │       ├── auth.js       # Authentication logic
│   │       └── admin.js      # Admin panel logic
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Home page
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   ├── dashboard.html    # User dashboard
│   │   ├── courses.html      # Courses page
│   │   ├── puzzles.html      # Puzzles page
│   │   ├── blind_play.html   # Blind play training
│   │   ├── leaderboard.html  # Leaderboard
│   │   └── admin.html        # Admin panel
│   └── auth.py               # Authentication utilities
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore file
└── README.md                 # This file
```

## Database Schema

The platform uses the following main tables:
- `users`: User accounts and ratings
- `categories`: Course and puzzle categories
- `courses`: Available courses
- `puzzles`: Chess puzzles with FEN positions
- `games`: User game history
- `puzzle_attempts`: Puzzle solving attempts
- `purchases`: Course purchases
- `rating_history`: User rating changes

## Usage Examples

### For Students
1. Register an account
2. Solve puzzles to improve tactics
3. Practice blind play to enhance visualization
4. Purchase courses to learn from professionals
5. Track your progress on the dashboard
6. Compete on the leaderboard

### For Admins
1. Access the admin panel at `/admin-panel`
2. Create categories for organizing content
3. Add courses with pricing and difficulty levels
4. Create puzzles with FEN positions and solutions
5. Monitor platform statistics
6. Manage users and permissions

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Admin-only protected routes
- SQL injection prevention with parameterized queries
- CORS protection
- XSS protection with template escaping

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue on GitHub.