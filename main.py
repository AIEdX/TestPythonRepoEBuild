from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="FastAPI AWS Template",
    description="A template for deploying FastAPI applications on AWS Elastic Beanstalk",
    version="1.0.0"
)

# Pydantic Models
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# In-memory storage
users_db = []

# Middleware for request timing
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request processed in {process_time:.4f} seconds")
    return response

# Root endpoint
@app.get("/", 
         status_code=status.HTTP_200_OK,
         tags=["Health Check"])
async def root():
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FastAPI AWS Template"
    }

# User endpoints
@app.post("/users/", 
          response_model=User,
          status_code=status.HTTP_201_CREATED,
          tags=["Users"])
async def create_user(user: UserCreate):
    logger.info(f"Creating new user with username: {user.username}")
    
    # Check if user already exists
    if any(u.username == user.username for u in users_db):
        logger.warning(f"Username {user.username} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    new_user = User(
        id=len(users_db) + 1,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        created_at=datetime.now()
    )
    users_db.append(new_user)
    
    logger.info(f"User {new_user.username} created successfully")
    return new_user

@app.get("/users/", 
         response_model=List[User],
         status_code=status.HTTP_200_OK,
         tags=["Users"])
async def get_users():
    logger.info("Retrieving all users")
    return users_db

@app.get("/users/{user_id}", 
         response_model=User,
         status_code=status.HTTP_200_OK,
         tags=["Users"])
async def get_user(user_id: int):
    logger.info(f"Retrieving user with ID: {user_id}")
    
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    # Add any initialization code here

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")
    # Add any cleanup code here