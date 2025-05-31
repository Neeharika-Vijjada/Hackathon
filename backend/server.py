from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import bcrypt
import jwt
from geopy.distance import geodesic
import math

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "FindBuddy API is running!", "status": "healthy"}

# JWT Configuration
JWT_SECRET = "findbuddy_secret_key_2025"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

security = HTTPBearer()

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    city: str
    phone: str
    bio: Optional[str] = ""
    interests: List[str] = []

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: str
    name: str
    email: str
    city: str
    phone: str
    bio: str
    interests: List[str]
    created_at: datetime
    profile_photo: Optional[str] = None

class ActivityCreate(BaseModel):
    title: str
    description: str
    date: datetime
    location: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_participants: Optional[int] = None
    category: str
    interests: List[str] = []

class Activity(BaseModel):
    id: str
    title: str
    description: str
    date: datetime
    location: str
    city: str
    latitude: Optional[float]
    longitude: Optional[float]
    max_participants: Optional[int]
    category: str
    interests: List[str]
    creator_id: str
    creator_name: str
    participants: List[str] = []
    interested_users: List[str] = []
    created_at: datetime

class JoinActivityRequest(BaseModel):
    activity_id: str

class MessageCreate(BaseModel):
    recipient_id: str
    content: str

class Message(BaseModel):
    id: str
    sender_id: str
    recipient_id: str
    content: str
    created_at: datetime
    read: bool = False

# Helper Functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_data = await db.users.find_one({"id": user_id})
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        
        return User(**user_data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers"""
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def calculate_interest_match_score(user_interests: List[str], activity_interests: List[str]) -> float:
    """Calculate match score between user and activity interests (0-1)"""
    if not user_interests or not activity_interests:
        return 0.1
    
    user_set = set([interest.lower() for interest in user_interests])
    activity_set = set([interest.lower() for interest in activity_interests])
    
    intersection = len(user_set.intersection(activity_set))
    union = len(user_set.union(activity_set))
    
    return intersection / union if union > 0 else 0.1

# Authentication Routes
@api_router.post("/auth/register")
async def register_user(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    user_id = str(uuid.uuid4())
    
    user_doc = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password,
        "city": user_data.city,
        "phone": user_data.phone,
        "bio": user_data.bio,
        "interests": user_data.interests,
        "created_at": datetime.utcnow(),
        "profile_photo": None
    }
    
    await db.users.insert_one(user_doc)
    
    # Create JWT token
    token = create_jwt_token(user_id)
    
    return {
        "message": "User registered successfully",
        "token": token,
        "user": User(**user_doc)
    }

@api_router.post("/auth/login")
async def login_user(credentials: UserLogin):
    user_data = await db.users.find_one({"email": credentials.email})
    if not user_data or not verify_password(credentials.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_jwt_token(user_data["id"])
    
    return {
        "message": "Login successful",
        "token": token,
        "user": User(**user_data)
    }

@api_router.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Activity Routes
@api_router.post("/activities")
async def create_activity(activity_data: ActivityCreate, current_user: User = Depends(get_current_user)):
    activity_id = str(uuid.uuid4())
    
    activity_doc = {
        "id": activity_id,
        "title": activity_data.title,
        "description": activity_data.description,
        "date": activity_data.date,
        "location": activity_data.location,
        "city": activity_data.city,
        "latitude": activity_data.latitude,
        "longitude": activity_data.longitude,
        "max_participants": activity_data.max_participants,
        "category": activity_data.category,
        "interests": activity_data.interests,
        "creator_id": current_user.id,
        "creator_name": current_user.name,
        "participants": [current_user.id],
        "interested_users": [],
        "created_at": datetime.utcnow()
    }
    
    await db.activities.insert_one(activity_doc)
    
    return {
        "message": "Activity created successfully",
        "activity": Activity(**activity_doc)
    }

@api_router.get("/activities/feed")
async def get_activity_feed(
    current_user: User = Depends(get_current_user),
    limit: int = 20,
    distance_km: Optional[float] = 50
):
    # Get all activities
    activities_cursor = db.activities.find({"date": {"$gte": datetime.utcnow()}})
    all_activities = await activities_cursor.to_list(1000)
    
    # Score and filter activities
    scored_activities = []
    
    for activity_data in all_activities:
        # Skip user's own activities
        if activity_data["creator_id"] == current_user.id:
            continue
            
        # Calculate interest match score
        interest_score = calculate_interest_match_score(current_user.interests, activity_data["interests"])
        
        # Calculate distance score (if coordinates available)
        distance_score = 1.0  # Default score if no coordinates
        if activity_data.get("latitude") and activity_data.get("longitude"):
            # For demo, assume user coordinates (in real app, store user location)
            user_lat, user_lon = 40.7128, -74.0060  # Default NYC coordinates
            distance = calculate_distance(
                user_lat, user_lon,
                activity_data["latitude"], activity_data["longitude"]
            )
            if distance <= distance_km:
                distance_score = max(0.1, 1 - (distance / distance_km))
            else:
                continue  # Skip activities outside distance range
        
        # Calculate time score (prefer sooner activities)
        days_until_activity = (activity_data["date"] - datetime.utcnow()).days
        time_score = max(0.1, 1 - (days_until_activity / 30))  # Prefer activities within 30 days
        
        # Combined score
        total_score = (interest_score * 0.5) + (distance_score * 0.3) + (time_score * 0.2)
        
        scored_activities.append({
            "activity": Activity(**activity_data),
            "score": total_score
        })
    
    # Sort by score and return top activities
    scored_activities.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "activities": [item["activity"] for item in scored_activities[:limit]],
        "total_count": len(scored_activities)
    }

@api_router.get("/activities")
async def get_all_activities(limit: int = 50):
    activities_cursor = db.activities.find({"date": {"$gte": datetime.utcnow()}}).sort("created_at", -1)
    activities_data = await activities_cursor.to_list(limit)
    
    return {
        "activities": [Activity(**activity) for activity in activities_data],
        "total_count": len(activities_data)
    }

@api_router.post("/activities/join")
async def join_activity(request: JoinActivityRequest, current_user: User = Depends(get_current_user)):
    activity = await db.activities.find_one({"id": request.activity_id})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user is already a participant
    if current_user.id in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already joined this activity")
    
    # Check if activity is full
    if activity.get("max_participants") and len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Add user to participants
    await db.activities.update_one(
        {"id": request.activity_id},
        {"$push": {"participants": current_user.id}}
    )
    
    return {"message": "Successfully joined activity"}

@api_router.get("/activities/my")
async def get_my_activities(current_user: User = Depends(get_current_user)):
    # Get activities created by user
    created_activities = await db.activities.find({"creator_id": current_user.id}).to_list(100)
    
    # Get activities user joined
    joined_activities = await db.activities.find({"participants": current_user.id, "creator_id": {"$ne": current_user.id}}).to_list(100)
    
    return {
        "created_activities": [Activity(**activity) for activity in created_activities],
        "joined_activities": [Activity(**activity) for activity in joined_activities]
    }

# Basic messaging
@api_router.post("/messages")
async def send_message(message_data: MessageCreate, current_user: User = Depends(get_current_user)):
    message_id = str(uuid.uuid4())
    
    message_doc = {
        "id": message_id,
        "sender_id": current_user.id,
        "recipient_id": message_data.recipient_id,
        "content": message_data.content,
        "created_at": datetime.utcnow(),
        "read": False
    }
    
    await db.messages.insert_one(message_doc)
    
    return {
        "message": "Message sent successfully",
        "message_data": Message(**message_doc)
    }

@api_router.get("/messages/conversations")
async def get_conversations(current_user: User = Depends(get_current_user)):
    # Get all messages involving the current user
    messages_cursor = db.messages.find({
        "$or": [
            {"sender_id": current_user.id},
            {"recipient_id": current_user.id}
        ]
    }).sort("created_at", -1)
    
    messages = await messages_cursor.to_list(1000)
    
    # Group by conversation partner
    conversations = {}
    for message in messages:
        partner_id = message["recipient_id"] if message["sender_id"] == current_user.id else message["sender_id"]
        
        if partner_id not in conversations:
            # Get partner info
            partner_data = await db.users.find_one({"id": partner_id})
            conversations[partner_id] = {
                "partner": User(**partner_data) if partner_data else None,
                "last_message": Message(**message),
                "messages": []
            }
        
        conversations[partner_id]["messages"].append(Message(**message))
    
    return {"conversations": list(conversations.values())}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
