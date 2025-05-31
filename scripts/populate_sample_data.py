#!/usr/bin/env python3
"""
Script to populate FindBuddy with realistic sample data
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

# Add the backend directory to the path
sys.path.append('/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import bcrypt
import uuid

# Load environment variables
load_dotenv('/app/backend/.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

async def create_sample_users():
    """Create sample users for activities"""
    sample_users = [
        {
            "id": str(uuid.uuid4()),
            "name": "Sarah Chen",
            "email": "sarah.chen@example.com",
            "password": hash_password("password123"),
            "city": "Santa Clara",
            "phone": "555-0101",
            "bio": "Love exploring new places and meeting new people! Big fan of outdoor activities and cultural events.",
            "interests": ["photography", "hiking", "festivals", "food", "art"],
            "created_at": datetime.utcnow(),
            "profile_photo": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Mike Rodriguez",
            "email": "mike.rodriguez@example.com",
            "password": hash_password("password123"),
            "city": "San Jose",
            "phone": "555-0102",
            "bio": "Sports enthusiast and fitness lover. Always up for a good workout or game!",
            "interests": ["basketball", "fitness", "sports", "gaming", "music"],
            "created_at": datetime.utcnow(),
            "profile_photo": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Emma Thompson",
            "email": "emma.thompson@example.com",
            "password": hash_password("password123"),
            "city": "Palo Alto",
            "phone": "555-0103",
            "bio": "Foodie and coffee enthusiast. Love trying new restaurants and cafes with friends!",
            "interests": ["coffee", "food", "cooking", "wine", "culture"],
            "created_at": datetime.utcnow(),
            "profile_photo": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Alex Kim",
            "email": "alex.kim@example.com",
            "password": hash_password("password123"),
            "city": "Mountain View",
            "phone": "555-0104",
            "bio": "Tech professional new to the Bay Area. Looking to explore and make new connections!",
            "interests": ["technology", "networking", "hiking", "movies", "board games"],
            "created_at": datetime.utcnow(),
            "profile_photo": None
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Jessica Wong",
            "email": "jessica.wong@example.com",
            "password": hash_password("password123"),
            "city": "Fremont",
            "phone": "555-0105",
            "bio": "Yoga instructor and wellness advocate. Love outdoor activities and mindful living.",
            "interests": ["yoga", "meditation", "wellness", "nature", "reading"],
            "created_at": datetime.utcnow(),
            "profile_photo": None
        }
    ]
    
    # Clear existing sample users
    await db.users.delete_many({"email": {"$regex": "@example.com"}})
    
    # Insert sample users
    await db.users.insert_many(sample_users)
    print(f"✅ Created {len(sample_users)} sample users")
    return sample_users

async def create_sample_activities(users):
    """Create realistic sample activities"""
    base_date = datetime.utcnow()
    
    sample_activities = [
        {
            "id": str(uuid.uuid4()),
            "title": "Water Lantern Festival in Santa Clara - Looking for Company! 🏮",
            "description": "Hey everyone! Anyone up for attending the Water Lantern Festival in Santa Clara next weekend? It's supposed to be absolutely magical - hundreds of lanterns floating on the water at sunset. I've been wanting to go but would love some company! We can grab dinner beforehand too. Let me know if you're interested! ✨",
            "date": base_date + timedelta(days=8),
            "location": "Central Park Lake, Santa Clara",
            "city": "Santa Clara",
            "latitude": 37.3541079,
            "longitude": -121.9552356,
            "max_participants": 6,
            "category": "Festival",
            "interests": ["festivals", "photography", "culture", "art"],
            "creator_id": users[0]["id"],
            "creator_name": users[0]["name"],
            "participants": [users[0]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=2)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Saturday Morning Basketball at Fremont Park 🏀",
            "description": "Looking for 3-4 people to join our Saturday morning basketball session! We play every week from 9-11 AM at Fremont Central Park. All skill levels welcome - it's more about having fun and staying active. Usually grab coffee after the game too. Drop a comment if you're in!",
            "date": base_date + timedelta(days=4),
            "location": "Fremont Central Park Basketball Courts",
            "city": "Fremont",
            "latitude": 37.5482697,
            "longitude": -121.9885719,
            "max_participants": 8,
            "category": "Sports",
            "interests": ["basketball", "sports", "fitness", "coffee"],
            "creator_id": users[1]["id"],
            "creator_name": users[1]["name"],
            "participants": [users[1]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=5)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Food Truck Festival & Wine Tasting This Weekend! 🍷🌮",
            "description": "There's an amazing food truck festival happening in downtown San Jose this weekend with over 20 vendors! Plus they're doing wine tastings from local vineyards. Perfect way to spend a Sunday afternoon - eat great food, try some wines, and enjoy live music. Who wants to join me for a foodie adventure?",
            "date": base_date + timedelta(days=6),
            "location": "Plaza de César Chávez, San Jose",
            "city": "San Jose",
            "latitude": 37.3382082,
            "longitude": -121.8863286,
            "max_participants": 5,
            "category": "Food & Drink",
            "interests": ["food", "wine", "music", "culture"],
            "creator_id": users[2]["id"],
            "creator_name": users[2]["name"],
            "participants": [users[2]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=8)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "New to Bay Area - Board Game Night Anyone? 🎲",
            "description": "Hey! I just moved to Mountain View for work and looking to meet some cool people. I have a collection of board games (Settlers of Catan, Ticket to Ride, Azul, etc.) and thought it would be fun to host a game night. BYOB and I'll provide snacks! Let's make it happen this Friday evening.",
            "date": base_date + timedelta(days=3),
            "location": "Community Center, Mountain View",
            "city": "Mountain View",
            "latitude": 37.3860517,
            "longitude": -122.0838511,
            "max_participants": 6,
            "category": "Social",
            "interests": ["board games", "networking", "social", "games"],
            "creator_id": users[3]["id"],
            "creator_name": users[3]["name"],
            "participants": [users[3]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=12)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Sunrise Yoga & Hiking at Rancho San Antonio 🧘‍♀️",
            "description": "Starting the week right with sunrise yoga followed by a gentle hike! Meeting at Rancho San Antonio at 6:30 AM for yoga session, then we'll do the easy loop trail. Perfect way to connect with nature and start Monday feeling refreshed. Bring your own mat and water bottle. All levels welcome! ☀️",
            "date": base_date + timedelta(days=2),
            "location": "Rancho San Antonio Open Space Preserve",
            "city": "Cupertino",
            "latitude": 37.3244444,
            "longitude": -122.0647222,
            "max_participants": 8,
            "category": "Wellness",
            "interests": ["yoga", "hiking", "nature", "wellness", "meditation"],
            "creator_id": users[4]["id"],
            "creator_name": users[4]["name"],
            "participants": [users[4]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=18)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Photography Walk in Palo Alto - Golden Hour Magic 📸",
            "description": "Calling all photography enthusiasts! Planning a golden hour photo walk through downtown Palo Alto and Stanford campus. We'll explore interesting architecture, street art, and hopefully catch some beautiful light. Bring any camera (phone cameras totally fine too!). Let's capture some amazing shots together and maybe grab dinner after!",
            "date": base_date + timedelta(days=7),
            "location": "University Avenue, Palo Alto",
            "city": "Palo Alto",
            "latitude": 37.4419,
            "longitude": -122.1430,
            "max_participants": 5,
            "category": "Photography",
            "interests": ["photography", "art", "walking", "creativity"],
            "creator_id": users[0]["id"],
            "creator_name": users[0]["name"],
            "participants": [users[0]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(minutes=45)
        },
        # New activities
        {
            "id": str(uuid.uuid4()),
            "title": "Beach Volleyball Tournament at Santa Cruz 🏐",
            "description": "Who's ready for some sun, sand, and volleyball? Organizing a friendly tournament at Santa Cruz Beach this weekend! We'll have multiple courts, music, and BBQ after the games. Perfect way to spend a Saturday by the ocean. All skill levels welcome - come for the fun, not just to win! 🌊",
            "date": base_date + timedelta(days=5),
            "location": "Santa Cruz Beach Volleyball Courts",
            "city": "Santa Cruz",
            "latitude": 36.9741,
            "longitude": -122.0308,
            "max_participants": 16,
            "category": "Sports",
            "interests": ["volleyball", "beach", "sports", "bbq", "music"],
            "creator_id": users[1]["id"],
            "creator_name": users[1]["name"],
            "participants": [users[1]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=3)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Tech Meetup: AI & Machine Learning Trends 🤖",
            "description": "Monthly tech meetup for AI enthusiasts! This month we're discussing the latest trends in machine learning, ChatGPT applications, and career opportunities in AI. Great networking opportunity for professionals and students. Pizza and drinks provided. RSVP to secure your spot!",
            "date": base_date + timedelta(days=9),
            "location": "WeWork San Francisco",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 50,
            "category": "Networking",
            "interests": ["technology", "AI", "networking", "career", "learning"],
            "creator_id": users[3]["id"],
            "creator_name": users[3]["name"],
            "participants": [users[3]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=6)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Salsa Dancing Class for Beginners 💃",
            "description": "¡Vamos a bailar! Join us for a beginner-friendly salsa dancing class every Tuesday evening. No partner needed - we rotate throughout the class so everyone gets to dance with everyone! Afterwards we usually head to a nearby bar for drinks and more dancing. Come learn some moves and have fun!",
            "date": base_date + timedelta(days=1),
            "location": "Dance Studio, Downtown San Jose",
            "city": "San Jose",
            "latitude": 37.3382082,
            "longitude": -121.8863286,
            "max_participants": 20,
            "category": "Dance",
            "interests": ["dancing", "salsa", "music", "social", "culture"],
            "creator_id": users[2]["id"],
            "creator_name": users[2]["name"],
            "participants": [users[2]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=1)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Karaoke Night at Lucky Strike! 🎤",
            "description": "It's time to unleash your inner rockstar! Join us for an epic karaoke night at Lucky Strike. Whether you're a shower singer or a confident performer, everyone's welcome! We've got private rooms booked and a great group already confirmed. Drinks, snacks, and lots of laughs guaranteed!",
            "date": base_date + timedelta(days=4),
            "location": "Lucky Strike, San Francisco",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 12,
            "category": "Entertainment",
            "interests": ["karaoke", "music", "entertainment", "singing", "social"],
            "creator_id": users[4]["id"],
            "creator_name": users[4]["name"],
            "participants": [users[4]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(minutes=30)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Weekend Farmers Market & Brunch Crawl 🥐",
            "description": "Let's explore the best farmers markets in the Bay Area followed by an epic brunch crawl! We'll start at Ferry Building Farmers Market, sample local produce, then hit 3-4 amazing brunch spots in the area. Perfect Saturday adventure for food lovers and explorers!",
            "date": base_date + timedelta(days=6),
            "location": "Ferry Building Marketplace",
            "city": "San Francisco",
            "latitude": 37.7955,
            "longitude": -122.3933,
            "max_participants": 8,
            "category": "Food & Drink",
            "interests": ["food", "brunch", "farmers market", "exploring", "social"],
            "creator_id": users[0]["id"],
            "creator_name": users[0]["name"],
            "participants": [users[0]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=4)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Trivia Night Challenge at Local Pub 🧠",
            "description": "Think you're smart? Prove it at trivia night! Our team needs 2-3 more people to dominate the weekly trivia challenge at Murphy's Pub. Categories include pop culture, history, science, and sports. Winner gets free appetizers for the whole table! Let's show them what we've got!",
            "date": base_date + timedelta(days=3),
            "location": "Murphy's Pub, Palo Alto",
            "city": "Palo Alto",
            "latitude": 37.4419,
            "longitude": -122.1430,
            "max_participants": 6,
            "category": "Social",
            "interests": ["trivia", "social", "competition", "knowledge", "pub"],
            "creator_id": users[1]["id"],
            "creator_name": users[1]["name"],
            "participants": [users[1]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=7)
        }
    ]
    
    # Clear existing sample activities
    await db.activities.delete_many({"creator_id": {"$in": [user["id"] for user in users]}})
    
    # Insert sample activities
    await db.activities.insert_many(sample_activities)
    print(f"✅ Created {len(sample_activities)} sample activities")
    return sample_activities

async def create_sample_merchants():
    """Create sample merchants with realistic businesses"""
    sample_merchants = [
        {
            "id": str(uuid.uuid4()),
            "business_name": "AMC Theaters Bay Area",
            "email": "partnerships@amcbayarea.com",
            "password": hash_password("merchant123"),
            "business_type": "entertainment",
            "address": "2855 Stevens Creek Blvd",
            "city": "Santa Clara",
            "phone": "555-AMC-MOVIE",
            "description": "Your premier movie theater destination in the Bay Area. Featuring the latest blockbusters, comfortable seating, and premium concessions.",
            "website": "https://www.amctheatres.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Climbing Club & Café",
            "email": "info@climbingclubcafe.com",
            "password": hash_password("merchant123"),
            "business_type": "sports",
            "address": "1234 Castro Street",
            "city": "Mountain View",
            "phone": "555-CLIMB-UP",
            "description": "Indoor rock climbing gym with café. Perfect place to challenge yourself and grab a post-workout smoothie with friends!",
            "website": "https://www.climbingclubcafe.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Bella Vista Italian Kitchen",
            "email": "manager@bellavistaitalian.com",
            "password": hash_password("merchant123"),
            "business_type": "restaurant",
            "address": "567 University Avenue",
            "city": "Palo Alto",
            "phone": "555-BELLA-01",
            "description": "Authentic Italian cuisine in the heart of Palo Alto. Fresh pasta, wood-fired pizzas, and an extensive wine selection.",
            "website": "https://www.bellavistaitalian.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Escape Reality Games",
            "email": "bookings@escaperealitygames.com",
            "password": hash_password("merchant123"),
            "business_type": "entertainment",
            "address": "890 The Alameda",
            "city": "San Jose",
            "phone": "555-ESCAPE-1",
            "description": "Immersive escape room experiences for groups. Team building, date nights, or just fun with friends!",
            "website": "https://www.escaperealitygames.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Zen Garden Spa & Wellness",
            "email": "hello@zengardensp.com",
            "password": hash_password("merchant123"),
            "business_type": "services",
            "address": "456 El Camino Real",
            "city": "Fremont",
            "phone": "555-ZEN-SPA1",
            "description": "Full-service spa offering massages, facials, and wellness treatments. Relax and rejuvenate with your friends!",
            "website": "https://www.zengardenspa.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        }
    ]
    
    # Clear existing sample merchants
    await db.merchants.delete_many({"email": {"$regex": "@.*\\.com"}})
    
    # Insert sample merchants
    await db.merchants.insert_many(sample_merchants)
    print(f"✅ Created {len(sample_merchants)} sample merchants")
    return sample_merchants

async def create_sample_discount_offers(merchants):
    """Create sample discount offers from merchants"""
    base_date = datetime.utcnow()
    
    sample_offers = [
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[0]["id"],  # AMC Theaters
            "merchant_name": merchants[0]["business_name"],
            "title": "Bring Your Buddy - Free Popcorn! 🍿",
            "description": "Come to any movie with a friend and get a free large popcorn! Perfect for date nights, friend hangouts, or family outings. Valid for any showtime, any movie. The more the merrier!",
            "discount_percentage": 0,  # Special offer, not percentage
            "minimum_buddies": 2,
            "valid_until": base_date + timedelta(days=60),
            "terms_conditions": "Valid with purchase of 2 or more movie tickets. One free large popcorn per group. Cannot be combined with other offers.",
            "max_redemptions": 500,
            "current_redemptions": 23,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[1]["id"],  # Climbing Club
            "merchant_name": merchants[1]["business_name"],
            "title": "Climb Together - 25% Off Day Passes! 🧗‍♀️",
            "description": "Bring a climbing buddy and both of you save 25% on day passes! Includes equipment rental and chalk. Great way to try climbing for the first time or challenge yourselves together!",
            "discount_percentage": 25,
            "minimum_buddies": 2,
            "valid_until": base_date + timedelta(days=45),
            "terms_conditions": "Valid for groups of 2-4 people. Includes day pass and basic equipment rental. Safety briefing required for first-time climbers.",
            "max_redemptions": 100,
            "current_redemptions": 8,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[2]["id"],  # Bella Vista
            "merchant_name": merchants[2]["business_name"],
            "title": "Dinner for Friends - 20% Off Groups of 4+ 🍝",
            "description": "Gather your friends for an authentic Italian dinner! Groups of 4 or more get 20% off their entire bill. Perfect for birthday celebrations, date nights, or just catching up with friends over amazing food and wine!",
            "discount_percentage": 20,
            "minimum_buddies": 4,
            "valid_until": base_date + timedelta(days=30),
            "terms_conditions": "Valid for groups of 4 or more people. Cannot be combined with other promotions. Valid Sunday-Thursday only. Reservations recommended.",
            "max_redemptions": 200,
            "current_redemptions": 45,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[3]["id"],  # Escape Reality
            "merchant_name": merchants[3]["business_name"],
            "title": "Team Escape Challenge - 30% Off Groups! 🔐",
            "description": "Book any escape room for 3+ people and save 30%! Perfect for team building, birthday parties, or just an exciting night out with friends. Can you escape in time?",
            "discount_percentage": 30,
            "minimum_buddies": 3,
            "valid_until": base_date + timedelta(days=90),
            "terms_conditions": "Valid for groups of 3-8 people. Advance booking required. Valid any day of the week. Multiple rooms available.",
            "max_redemptions": 150,
            "current_redemptions": 12,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[4]["id"],  # Zen Garden Spa
            "merchant_name": merchants[4]["business_name"],
            "title": "Spa Day with Friends - 15% Off Duo Packages 💆‍♀️",
            "description": "Treat yourself and a friend to a relaxing spa day! Book any duo package (massage, facial, or wellness treatment) and save 15%. Unwind together and leave feeling refreshed and renewed!",
            "discount_percentage": 15,
            "minimum_buddies": 2,
            "valid_until": base_date + timedelta(days=120),
            "terms_conditions": "Valid for spa duo packages only. Appointment required 48 hours in advance. Valid Monday-Friday only.",
            "max_redemptions": 75,
            "current_redemptions": 3,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[0]["id"],  # AMC Second Offer
            "merchant_name": merchants[0]["business_name"],
            "title": "Weekend Movie Night - 2 for 1 Tickets! 🎬",
            "description": "Weekend special! Buy one movie ticket, get one free for any Saturday or Sunday showing. Perfect for couples, friends, or family outings. Don't miss out on the latest blockbusters!",
            "discount_percentage": 50,
            "minimum_buddies": 2,
            "valid_until": base_date + timedelta(days=14),
            "terms_conditions": "Valid weekends only (Saturday & Sunday). Excludes premium format screenings. One free ticket per paid ticket.",
            "max_redemptions": 300,
            "current_redemptions": 67,
            "active": True,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Clear existing sample offers
    await db.discount_offers.delete_many({"merchant_id": {"$in": [merchant["id"] for merchant in merchants]}})
    
    # Insert sample discount offers
    await db.discount_offers.insert_many(sample_offers)
    print(f"✅ Created {len(sample_offers)} sample discount offers")
    return sample_offers

async def main():
    """Main function to populate all sample data"""
    print("🚀 Populating FindBuddy with sample data...")
    
    try:
        # Create sample users
        users = await create_sample_users()
        
        # Create sample activities
        activities = await create_sample_activities(users)
        
        # Create sample merchants
        merchants = await create_sample_merchants()
        
        # Create sample discount offers
        offers = await create_sample_discount_offers(merchants)
        
        print("\n🎉 Sample data population completed successfully!")
        print(f"📊 Summary:")
        print(f"   • {len(users)} sample users created")
        print(f"   • {len(activities)} sample activities created")
        print(f"   • {len(merchants)} sample merchants created")
        print(f"   • {len(offers)} sample discount offers created")
        print("\n🔗 You can now explore FindBuddy with realistic content!")
        
    except Exception as e:
        print(f"❌ Error populating sample data: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())