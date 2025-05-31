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

class MerchantCreate(BaseModel):
    business_name: str
    email: str
    password: str
    business_type: str  # restaurant, entertainment, sports, events, etc.
    address: str
    city: str
    phone: str
    description: str
    website: Optional[str] = ""

class MerchantLogin(BaseModel):
    email: str
    password: str

class Merchant(BaseModel):
    id: str
    business_name: str
    email: str
    business_type: str
    address: str
    city: str
    phone: str
    description: str
    website: Optional[str]
    verified: bool = False
    created_at: datetime
    logo: Optional[str] = None

class DiscountOfferCreate(BaseModel):
    title: str
    description: str
    discount_percentage: int
    minimum_buddies: int = 2
    valid_until: datetime
    terms_conditions: str
    max_redemptions: Optional[int] = None

class DiscountOffer(BaseModel):
    id: str
    merchant_id: str
    merchant_name: str
    title: str
    description: str
    discount_percentage: int
    minimum_buddies: int
    valid_until: datetime
    terms_conditions: str
    max_redemptions: Optional[int]
    current_redemptions: int = 0
    active: bool = True
    created_at: datetime

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

def create_jwt_token(user_id: str, user_type: str = "user") -> str:
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        user_type = payload.get("user_type", "user")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        if user_type == "merchant":
            raise HTTPException(status_code=401, detail="Merchant token not valid for user endpoints")
        
        user_data = await db.users.find_one({"id": user_id})
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        
        return User(**user_data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_merchant(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        user_type = payload.get("user_type", "user")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        if user_type != "merchant":
            raise HTTPException(status_code=401, detail="User token not valid for merchant endpoints")
        
        merchant_data = await db.merchants.find_one({"id": user_id})
        if not merchant_data:
            raise HTTPException(status_code=401, detail="Merchant not found")
        
        return Merchant(**merchant_data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers"""
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def calculate_interest_match_score(user_interests: List[str], activity_interests: List[str]) -> float:
    """Calculate match score between user and activity interests (0-1)"""
    if not user_interests:
        return 0.3  # Give some base score if user has no interests
    if not activity_interests:
        return 0.2  # Give some base score if activity has no interests
    
    user_set = set([interest.lower().strip() for interest in user_interests])
    activity_set = set([interest.lower().strip() for interest in activity_interests])
    
    # Direct matches
    intersection = len(user_set.intersection(activity_set))
    if intersection > 0:
        union = len(user_set.union(activity_set))
        direct_score = intersection / union
    else:
        direct_score = 0
    
    # Partial matches (substring matching)
    partial_score = 0.0
    for user_interest in user_set:
        for activity_interest in activity_set:
            if user_interest in activity_interest or activity_interest in user_interest:
                partial_score += 0.3
                break
    
    # Combine scores
    final_score = max(direct_score, partial_score)
    return min(1.0, final_score)  # Cap at 1.0

# User Authentication Routes
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
    token = create_jwt_token(user_id, "user")
    
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
    
    token = create_jwt_token(user_data["id"], "user")
    
    return {
        "message": "Login successful",
        "token": token,
        "user": User(**user_data)
    }

@api_router.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Merchant Authentication Routes
@api_router.post("/merchants/register")
async def register_merchant(merchant_data: MerchantCreate):
    # Check if merchant already exists
    existing_merchant = await db.merchants.find_one({"email": merchant_data.email})
    if existing_merchant:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create merchant
    hashed_password = hash_password(merchant_data.password)
    merchant_id = str(uuid.uuid4())
    
    merchant_doc = {
        "id": merchant_id,
        "business_name": merchant_data.business_name,
        "email": merchant_data.email,
        "password": hashed_password,
        "business_type": merchant_data.business_type,
        "address": merchant_data.address,
        "city": merchant_data.city,
        "phone": merchant_data.phone,
        "description": merchant_data.description,
        "website": merchant_data.website,
        "verified": False,
        "created_at": datetime.utcnow(),
        "logo": None
    }
    
    await db.merchants.insert_one(merchant_doc)
    
    # Create JWT token
    token = create_jwt_token(merchant_id, "merchant")
    
    return {
        "message": "Merchant registered successfully",
        "token": token,
        "merchant": Merchant(**merchant_doc)
    }

@api_router.post("/merchants/login")
async def login_merchant(credentials: MerchantLogin):
    merchant_data = await db.merchants.find_one({"email": credentials.email})
    if not merchant_data or not verify_password(credentials.password, merchant_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_jwt_token(merchant_data["id"], "merchant")
    
    return {
        "message": "Login successful",
        "token": token,
        "merchant": Merchant(**merchant_data)
    }

@api_router.get("/merchants/me")
async def get_current_merchant_info(current_merchant: Merchant = Depends(get_current_merchant)):
    return current_merchant

# Activity Routes (Updated for "Activities Around Me")
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

@api_router.get("/activities/around-me")
async def get_activities_around_me(
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    city_filter: Optional[str] = None
):
    """Get all activities in the area (not personalized)"""
    query = {"date": {"$gte": datetime.utcnow()}}
    
    # Filter by city if specified, otherwise use user's city
    target_city = city_filter or current_user.city
    query["city"] = {"$regex": target_city, "$options": "i"}
    
    activities_cursor = db.activities.find(query).sort("created_at", -1)
    activities_data = await activities_cursor.to_list(limit)
    
    return {
        "activities": [Activity(**activity) for activity in activities_data],
        "total_count": len(activities_data),
        "city": target_city
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
    
    # Get activities user joined (excluding ones they created)
    joined_activities = await db.activities.find({
        "participants": current_user.id, 
        "creator_id": {"$ne": current_user.id}
    }).to_list(100)
    
    return {
        "created_activities": [Activity(**activity) for activity in created_activities],
        "joined_activities": [Activity(**activity) for activity in joined_activities]
    }

# Merchant and Discount Routes
@api_router.post("/merchants/discounts")
async def create_discount_offer(
    discount_data: DiscountOfferCreate, 
    current_merchant: Merchant = Depends(get_current_merchant)
):
    discount_id = str(uuid.uuid4())
    
    discount_doc = {
        "id": discount_id,
        "merchant_id": current_merchant.id,
        "merchant_name": current_merchant.business_name,
        "title": discount_data.title,
        "description": discount_data.description,
        "discount_percentage": discount_data.discount_percentage,
        "minimum_buddies": discount_data.minimum_buddies,
        "valid_until": discount_data.valid_until,
        "terms_conditions": discount_data.terms_conditions,
        "max_redemptions": discount_data.max_redemptions,
        "current_redemptions": 0,
        "active": True,
        "created_at": datetime.utcnow()
    }
    
    await db.discount_offers.insert_one(discount_doc)
    
    return {
        "message": "Discount offer created successfully",
        "discount": DiscountOffer(**discount_doc)
    }

@api_router.get("/merchants/discounts/my")
async def get_my_discount_offers(current_merchant: Merchant = Depends(get_current_merchant)):
    discounts_cursor = db.discount_offers.find({"merchant_id": current_merchant.id})
    discounts_data = await discounts_cursor.to_list(100)
    
    return {
        "discounts": [DiscountOffer(**discount) for discount in discounts_data],
        "total_count": len(discounts_data)
    }

@api_router.get("/merchants/near-me")
async def get_merchants_near_me(
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    business_type: Optional[str] = None
):
    """Get merchants and their active offers near the user"""
    query = {"city": {"$regex": current_user.city, "$options": "i"}}
    
    if business_type:
        query["business_type"] = {"$regex": business_type, "$options": "i"}
    
    merchants_cursor = db.merchants.find(query)
    merchants_data = await merchants_cursor.to_list(limit)
    
    # Get active discount offers for these merchants
    merchant_ids = [merchant["id"] for merchant in merchants_data]
    discounts_cursor = db.discount_offers.find({
        "merchant_id": {"$in": merchant_ids},
        "active": True,
        "valid_until": {"$gte": datetime.utcnow()}
    })
    discounts_data = await discounts_cursor.to_list(1000)
    
    # Group discounts by merchant
    merchant_discounts = {}
    for discount in discounts_data:
        merchant_id = discount["merchant_id"]
        if merchant_id not in merchant_discounts:
            merchant_discounts[merchant_id] = []
        merchant_discounts[merchant_id].append(DiscountOffer(**discount))
    
    # Combine merchants with their offers
    merchants_with_offers = []
    for merchant_data in merchants_data:
        merchant = Merchant(**merchant_data)
        offers = merchant_discounts.get(merchant.id, [])
        merchants_with_offers.append({
            "merchant": merchant,
            "active_offers": offers,
            "offers_count": len(offers)
        })
    
    return {
        "merchants": merchants_with_offers,
        "total_count": len(merchants_with_offers)
    }

@api_router.get("/discounts/all")
async def get_all_discount_offers(
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    business_type: Optional[str] = None
):
    """Get all active discount offers"""
    # Build query for active offers
    query = {
        "active": True,
        "valid_until": {"$gte": datetime.utcnow()}
    }
    
    discounts_cursor = db.discount_offers.find(query).sort("created_at", -1)
    discounts_data = await discounts_cursor.to_list(limit)
    
    # If business type filter is specified, filter by merchant business type
    if business_type:
        merchant_ids = [discount["merchant_id"] for discount in discounts_data]
        matching_merchants = await db.merchants.find({
            "id": {"$in": merchant_ids},
            "business_type": {"$regex": business_type, "$options": "i"}
        }).to_list(1000)
        matching_merchant_ids = {merchant["id"] for merchant in matching_merchants}
        discounts_data = [discount for discount in discounts_data 
                         if discount["merchant_id"] in matching_merchant_ids]
    
    return {
        "discounts": [DiscountOffer(**discount) for discount in discounts_data],
        "total_count": len(discounts_data)
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
