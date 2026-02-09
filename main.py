from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.database.database import init_db
from app.routers import auth, courses, puzzles, games, categories, admin
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    await init_db()
    print("Application started successfully")
    yield

app = FastAPI(title="Chess Training Platform", version="1.0.0", lifespan=lifespan)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with user-friendly messages"""
    errors = []
    for error in exc.errors():
        field = error.get("loc", [])[-1] if error.get("loc") else "field"
        msg = error.get("msg", "Invalid value")
        errors.append(f"{field}: {msg}")
    
    error_message = "; ".join(errors)
    return JSONResponse(
        status_code=422,
        content={"detail": error_message}
    )

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(puzzles.router)
app.include_router(games.router)
app.include_router(categories.router)
app.include_router(admin.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/courses-page", response_class=HTMLResponse)
async def courses_page(request: Request):
    """Courses page"""
    return templates.TemplateResponse("courses.html", {"request": request})

@app.get("/puzzles-page", response_class=HTMLResponse)
async def puzzles_page(request: Request):
    """Puzzles page"""
    return templates.TemplateResponse("puzzles.html", {"request": request})

@app.get("/blind-play", response_class=HTMLResponse)
async def blind_play_page(request: Request):
    """Blind play training page"""
    return templates.TemplateResponse("blind_play.html", {"request": request})

@app.get("/admin-panel", response_class=HTMLResponse)
async def admin_panel_page(request: Request):
    """Admin panel page"""
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_page(request: Request):
    """Leaderboard page"""
    return templates.TemplateResponse("leaderboard.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    try:
        port = int(os.getenv("PORT", 8000))
    except ValueError:
        print("Error: PORT environment variable must be a valid integer. Using default port 8000.")
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
