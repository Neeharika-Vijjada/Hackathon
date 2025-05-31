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
            "title": "🚀 Exciting Career Networking Event - Tech Professionals Welcome!",
            "description": "Hello LinkedIn network! I'm organizing an exclusive networking event for tech professionals in the Bay Area. We'll have senior engineers from Google, Meta, and startups sharing insights on career growth, latest tech trends, and job opportunities. Perfect for anyone looking to expand their professional network and learn from industry leaders. Light refreshments and business card exchange included. #TechNetworking #CareerGrowth #BayAreaTech",
            "date": base_date + timedelta(days=8),
            "location": "WeWork, Downtown San Francisco",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 50,
            "category": "Professional",
            "interests": ["networking", "technology", "career", "professional development"],
            "creator_id": users[0]["id"],
            "creator_name": users[0]["name"],
            "participants": [users[0]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=2)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "💼 Startup Founders Meetup - Seeking Co-Founders & Advisors",
            "description": "Attention entrepreneurs and startup enthusiasts! I'm hosting a monthly meetup for startup founders, aspiring entrepreneurs, and potential co-founders. This month's theme: 'Building MVP to Product-Market Fit'. We'll have pitch sessions, networking rounds, and mentorship opportunities. Whether you're looking for a technical co-founder, seeking investment advice, or want to join an early-stage startup, this is the perfect place to connect. #StartupLife #Entrepreneurship #Networking #Innovation",
            "date": base_date + timedelta(days=4),
            "location": "Plug and Play Tech Center, Sunnyvale",
            "city": "Sunnyvale",
            "latitude": 37.4043,
            "longitude": -122.0748,
            "max_participants": 40,
            "category": "Business",
            "interests": ["startups", "entrepreneurship", "business", "innovation", "networking"],
            "creator_id": users[1]["id"],
            "creator_name": users[1]["name"],
            "participants": [users[1]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=5)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "🎯 Digital Marketing Workshop - Learn Growth Hacking Strategies",
            "description": "Excited to announce a hands-on digital marketing workshop! As a marketing professional with 8+ years of experience, I'll be sharing proven strategies for user acquisition, conversion optimization, and brand building. Topics include: SEO/SEM, social media marketing, content strategy, and analytics. Perfect for marketing professionals, business owners, and anyone looking to upskill in digital marketing. Attendees will receive templates, checklists, and networking opportunities. #DigitalMarketing #GrowthHacking #SEO #ContentMarketing #ProfessionalDevelopment",
            "date": base_date + timedelta(days=6),
            "location": "General Assembly, San Francisco",
            "city": "San Francisco",
            "latitude": 37.7849,
            "longitude": -122.4094,
            "max_participants": 25,
            "category": "Education",
            "interests": ["marketing", "digital marketing", "growth", "education", "business"],
            "creator_id": users[2]["id"],
            "creator_name": users[2]["name"],
            "participants": [users[2]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=8)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "🌐 AI & Machine Learning Study Group - Weekly Sessions",
            "description": "Launching a weekly AI/ML study group for professionals looking to transition into AI roles or enhance their current skills. We'll cover machine learning fundamentals, deep learning, NLP, and practical applications using Python, TensorFlow, and PyTorch. Each session includes hands-on coding, paper discussions, and project presentations. Open to all skill levels - from beginners to experienced professionals wanting to stay current with AI trends. #ArtificialIntelligence #MachineLearning #ProfessionalDevelopment #TechEducation #DataScience",
            "date": base_date + timedelta(days=3),
            "location": "Stanford Research Park, Palo Alto",
            "city": "Palo Alto",
            "latitude": 37.4419,
            "longitude": -122.1430,
            "max_participants": 15,
            "category": "Technology",
            "interests": ["AI", "machine learning", "technology", "data science", "education"],
            "creator_id": users[3]["id"],
            "creator_name": users[3]["name"],
            "participants": [users[3]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=12)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "🏢 Leadership & Management Workshop - Building High-Performance Teams",
            "description": "Calling all managers and aspiring leaders! I'm facilitating a leadership workshop focused on building and managing high-performance teams in tech environments. Drawing from my experience leading teams at Fortune 500 companies, we'll cover: effective communication, conflict resolution, team motivation, and performance management. Interactive sessions with real case studies and peer learning. Ideal for engineering managers, product managers, and senior professionals. #Leadership #Management #TeamBuilding #ProfessionalGrowth #TechLeadership",
            "date": base_date + timedelta(days=2),
            "location": "LinkedIn Sunnyvale Campus",
            "city": "Sunnyvale",
            "latitude": 37.4043,
            "longitude": -122.0748,
            "max_participants": 20,
            "category": "Leadership",
            "interests": ["leadership", "management", "professional development", "team building"],
            "creator_id": users[4]["id"],
            "creator_name": users[4]["name"],
            "participants": [users[4]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=18)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "📊 Data Analytics Bootcamp - From SQL to Tableau",
            "description": "Announcing a comprehensive 3-day data analytics bootcamp! As a senior data analyst, I'll be teaching practical skills that companies actually need: SQL querying, data visualization with Tableau, Python for data analysis, and statistical fundamentals. Perfect for professionals looking to transition into data roles or enhance their analytical skills. Hands-on exercises with real datasets and career guidance included. #DataAnalytics #SQL #Tableau #CareerChange #ProfessionalTraining",
            "date": base_date + timedelta(days=7),
            "location": "UC Berkeley Extension, San Francisco",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 30,
            "category": "Education",
            "interests": ["data analytics", "SQL", "tableau", "education", "career development"],
            "creator_id": users[0]["id"],
            "creator_name": users[0]["name"],
            "participants": [users[0]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(minutes=45)
        },
        # Additional professional networking events
        {
            "id": str(uuid.uuid4()),
            "title": "🎪 Product Management Roundtable - Strategy & Execution",
            "description": "Fellow product managers, let's connect! I'm organizing a monthly roundtable for PM professionals to discuss challenges, share best practices, and learn from each other. This session focuses on product strategy, roadmap planning, and cross-functional collaboration. We'll have case study discussions, framework sharing, and networking time. Open to PMs at all levels - from APMs to VPs of Product. Great opportunity to expand your PM network in the Bay Area. #ProductManagement #Strategy #Networking #TechCareers",
            "date": base_date + timedelta(days=5),
            "location": "Airbnb Headquarters, San Francisco",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 25,
            "category": "Professional",
            "interests": ["product management", "strategy", "networking", "technology"],
            "creator_id": users[1]["id"],
            "creator_name": users[1]["name"],
            "participants": [users[1]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=3)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "💡 Innovation Lab - Ideation to Implementation Workshop",
            "description": "Join me for an innovation workshop designed for professionals looking to drive change in their organizations! We'll explore design thinking methodologies, rapid prototyping, and lean startup principles. Perfect for intrapreneurs, R&D professionals, and innovation teams. Interactive sessions with real problem-solving and takeaway frameworks you can implement immediately. #Innovation #DesignThinking #Entrepreneurship #ProfessionalDevelopment #Workshops",
            "date": base_date + timedelta(days=9),
            "location": "IDEO Design Studio, Palo Alto",
            "city": "Palo Alto",
            "latitude": 37.4419,
            "longitude": -122.1430,
            "max_participants": 20,
            "category": "Innovation",
            "interests": ["innovation", "design thinking", "entrepreneurship", "workshops"],
            "creator_id": users[3]["id"],
            "creator_name": users[3]["name"],
            "participants": [users[3]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=6)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "🔗 Sales & Business Development Networking Event",
            "description": "Attention sales professionals and BD executives! I'm hosting a networking event specifically for sales and business development professionals in tech. We'll discuss sales strategies, market trends, and partnership opportunities. Featured speakers from successful SaaS companies will share insights on enterprise sales, channel partnerships, and customer success. Great for account executives, sales managers, and BD professionals looking to grow their network. #Sales #BusinessDevelopment #B2B #SaaS #Networking",
            "date": base_date + timedelta(days=1),
            "location": "Salesforce Tower, San Francisco",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 35,
            "category": "Sales",
            "interests": ["sales", "business development", "B2B", "networking"],
            "creator_id": users[2]["id"],
            "creator_name": users[2]["name"],
            "participants": [users[2]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=1)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "🎨 UX/UI Design Portfolio Review & Career Guidance",
            "description": "Calling all UX/UI designers! As a design director with 10+ years of experience, I'm offering portfolio reviews and career guidance sessions. We'll cover portfolio best practices, interview preparation, and career advancement strategies. Whether you're a junior designer looking to level up or an experienced designer considering a career move, this session provides valuable insights and networking opportunities. #UXDesign #UIDesign #Portfolio #CareerAdvice #DesignCareers",
            "date": base_date + timedelta(days=4),
            "location": "Adobe San Francisco Office",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 15,
            "category": "Design",
            "interests": ["UX design", "UI design", "portfolio", "career", "design"],
            "creator_id": users[4]["id"],
            "creator_name": users[4]["name"],
            "participants": [users[4]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(minutes=30)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "🏦 Fintech Innovation Panel - Future of Financial Services",
            "description": "Excited to moderate a fintech innovation panel featuring industry leaders from top financial institutions and fintech startups. We'll discuss cryptocurrency adoption, digital banking transformation, regulatory challenges, and investment opportunities in fintech. Panelists include VPs from major banks, fintech founders, and venture capitalists. Networking reception follows the panel discussion. #Fintech #Innovation #Finance #Cryptocurrency #Banking #InvestmentOpportunities",
            "date": base_date + timedelta(days=6),
            "location": "Wells Fargo Innovation Center, San Francisco",
            "city": "San Francisco",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "max_participants": 100,
            "category": "Finance",
            "interests": ["fintech", "finance", "innovation", "cryptocurrency", "banking"],
            "creator_id": users[0]["id"],
            "creator_name": users[0]["name"],
            "participants": [users[0]["id"]],
            "interested_users": [],
            "created_at": datetime.utcnow() - timedelta(hours=4)
        },
        {
            "id": str(uuid.uuid4()),
            "title": "⚡ DevOps & Cloud Architecture Workshop - AWS Best Practices",
            "description": "Join me for a hands-on DevOps workshop focused on AWS cloud architecture and deployment best practices! As a senior DevOps engineer, I'll cover containerization with Docker, orchestration with Kubernetes, CI/CD pipelines, and infrastructure as code. Includes live demos and practical exercises. Perfect for developers, system administrators, and anyone interested in cloud technologies. Bring your laptop for hands-on learning! #DevOps #AWS #CloudComputing #Kubernetes #Docker #TechWorkshop",
            "date": base_date + timedelta(days=3),
            "location": "Amazon Web Services Office, Palo Alto",
            "city": "Palo Alto",
            "latitude": 37.4419,
            "longitude": -122.1430,
            "max_participants": 25,
            "category": "Technology",
            "interests": ["DevOps", "AWS", "cloud computing", "kubernetes", "docker"],
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
        },
        # New merchants
        {
            "id": str(uuid.uuid4()),
            "business_name": "TopGolf San Jose",
            "email": "events@topgolf-sj.com",
            "password": hash_password("merchant123"),
            "business_type": "entertainment",
            "address": "1500 Great Mall Dr",
            "city": "Milpitas",
            "phone": "555-TOP-GOLF",
            "description": "High-tech driving range meets sports bar! Perfect for groups looking to have fun, compete, and enjoy great food and drinks.",
            "website": "https://www.topgolf.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "The Cheesecake Factory",
            "email": "groups@cheesecakefactory.com",
            "password": hash_password("merchant123"),
            "business_type": "restaurant",
            "address": "1875 S Bascom Ave",
            "city": "Campbell",
            "phone": "555-CHEESECAKE",
            "description": "Over 250 menu items including our famous cheesecakes! Perfect for large groups and celebrations with friends.",
            "website": "https://www.thecheesecakefactory.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Dave & Buster's",
            "email": "parties@daveandbusters.com",
            "password": hash_password("merchant123"),
            "business_type": "entertainment",
            "address": "3030 Hillview Ave",
            "city": "Palo Alto",
            "phone": "555-DAVE-BUST",
            "description": "Arcade games, sports viewing, and delicious food! The ultimate destination for group fun and friendly competition.",
            "website": "https://www.daveandbusters.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Urban Air Adventure Park",
            "email": "groups@urbanair.com",
            "password": hash_password("merchant123"),
            "business_type": "sports",
            "address": "5650 Cottle Rd",
            "city": "San Jose",
            "phone": "555-URBAN-AIR",
            "description": "Indoor adventure park with trampolines, obstacle courses, and climbing walls. Perfect for active groups and birthday parties!",
            "website": "https://www.urbanair.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Starbucks Reserve",
            "email": "events@starbucksreserve.com",
            "password": hash_password("merchant123"),
            "business_type": "restaurant",
            "address": "1 Ferry Building",
            "city": "San Francisco",
            "phone": "555-STARBUCKS",
            "description": "Premium coffee experience with rare beans and expert brewing. Great spot for coffee lovers to meet and chat!",
            "website": "https://www.starbucksreserve.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Bowlero Fremont",
            "email": "parties@bowlero.com",
            "password": hash_password("merchant123"),
            "business_type": "entertainment",
            "address": "4555 Cushing Pkwy",
            "city": "Fremont",
            "phone": "555-BOWLERO",
            "description": "Modern bowling with cosmic lighting, arcade games, and full bar. Perfect for group outings and celebrations!",
            "website": "https://www.bowlero.com",
            "verified": True,
            "created_at": datetime.utcnow(),
            "logo": None
        },
        {
            "id": str(uuid.uuid4()),
            "business_name": "Cyclebar Studio",
            "email": "hello@cyclebar.com",
            "password": hash_password("merchant123"),
            "business_type": "sports",
            "address": "123 Main Street",
            "city": "Santa Clara",
            "phone": "555-CYCLE-BAR",
            "description": "Premium indoor cycling studio with energizing music and motivating instructors. Great for fitness buddies!",
            "website": "https://www.cyclebar.com",
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
        },
        # New offers for additional merchants
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[5]["id"] if len(merchants) > 5 else merchants[0]["id"],  # TopGolf
            "merchant_name": merchants[5]["business_name"] if len(merchants) > 5 else "TopGolf San Jose",
            "title": "Golf with Friends - 40% Off Bay Rentals! ⛳",
            "description": "Bring your crew for an epic golf experience! Groups of 4+ get 40% off bay rentals during weekday happy hours. Includes clubs and unlimited time until 6 PM!",
            "discount_percentage": 40,
            "minimum_buddies": 4,
            "valid_until": base_date + timedelta(days=60),
            "terms_conditions": "Valid Monday-Friday 2-6 PM only. Groups of 4-6 people. Includes clubs and balls. Food and drinks sold separately.",
            "max_redemptions": 100,
            "current_redemptions": 15,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[6]["id"] if len(merchants) > 6 else merchants[1]["id"],  # Cheesecake Factory
            "merchant_name": merchants[6]["business_name"] if len(merchants) > 6 else "The Cheesecake Factory",
            "title": "Group Celebration - Free Cheesecake! 🍰",
            "description": "Celebrating with friends? Groups of 6+ get a complimentary cheesecake of your choice! Perfect for birthdays, graduations, or any special occasion worth celebrating together.",
            "discount_percentage": 0,  # Special offer
            "minimum_buddies": 6,
            "valid_until": base_date + timedelta(days=90),
            "terms_conditions": "Valid for groups of 6 or more. One complimentary cheesecake per table. Cannot be combined with other offers. Reservations recommended.",
            "max_redemptions": 200,
            "current_redemptions": 28,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[7]["id"] if len(merchants) > 7 else merchants[2]["id"],  # Dave & Buster's
            "merchant_name": merchants[7]["business_name"] if len(merchants) > 7 else "Dave & Buster's",
            "title": "Power Hour - 30% Off Game Cards! 🎮",
            "description": "Game on with your buddies! Groups of 3+ get 30% off all game cards during weekday power hours. Perfect for friendly competition and tons of fun!",
            "discount_percentage": 30,
            "minimum_buddies": 3,
            "valid_until": base_date + timedelta(days=45),
            "terms_conditions": "Valid Monday-Thursday 3-6 PM. Groups of 3-8 people. Discount applies to game cards only, not food or drinks.",
            "max_redemptions": 150,
            "current_redemptions": 42,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[8]["id"] if len(merchants) > 8 else merchants[3]["id"],  # Urban Air
            "merchant_name": merchants[8]["business_name"] if len(merchants) > 8 else "Urban Air Adventure Park",
            "title": "Squad Jump - 25% Off Group Packages! 🤸‍♀️",
            "description": "Jump into fun with your squad! Groups of 4+ save 25% on adventure packages. Includes trampolines, obstacles, and climbing. Perfect for active friend groups!",
            "discount_percentage": 25,
            "minimum_buddies": 4,
            "valid_until": base_date + timedelta(days=75),
            "terms_conditions": "Valid for groups of 4-12 people. Includes 90-minute adventure package. Safety waivers required for all participants.",
            "max_redemptions": 80,
            "current_redemptions": 12,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[9]["id"] if len(merchants) > 9 else merchants[4]["id"],  # Starbucks Reserve
            "merchant_name": merchants[9]["business_name"] if len(merchants) > 9 else "Starbucks Reserve",
            "title": "Coffee Club - Buy 3 Get 1 Free! ☕",
            "description": "Perfect for coffee dates and study groups! When 4 friends order specialty drinks together, the 4th drink is on us. Enjoy premium coffee experiences together!",
            "discount_percentage": 25,
            "minimum_buddies": 4,
            "valid_until": base_date + timedelta(days=30),
            "terms_conditions": "Valid for groups ordering together. Applies to specialty reserve drinks only. Free drink must be equal or lesser value.",
            "max_redemptions": 500,
            "current_redemptions": 89,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[10]["id"] if len(merchants) > 10 else merchants[0]["id"],  # Bowlero
            "merchant_name": merchants[10]["business_name"] if len(merchants) > 10 else "Bowlero Fremont",
            "title": "Strike Night - 50% Off Lane Rentals! 🎳",
            "description": "Roll with your crew and save big! Groups of 4+ get 50% off lane rentals during weeknight specials. Includes shoes and unlimited bowling until midnight!",
            "discount_percentage": 50,
            "minimum_buddies": 4,
            "valid_until": base_date + timedelta(days=60),
            "terms_conditions": "Valid Sunday-Thursday 8 PM-midnight. Groups of 4-8 people. Includes shoe rental. Food and drinks sold separately.",
            "max_redemptions": 120,
            "current_redemptions": 35,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[11]["id"] if len(merchants) > 11 else merchants[1]["id"],  # Cyclebar
            "merchant_name": merchants[11]["business_name"] if len(merchants) > 11 else "Cyclebar Studio",
            "title": "Fitness Friends - 3 Classes for $60! 🚴‍♀️",
            "description": "Sweat together, stay together! Groups of 3+ can split a 3-class package for just $60 total. Get fit and have fun with your workout buddies!",
            "discount_percentage": 40,
            "minimum_buddies": 3,
            "valid_until": base_date + timedelta(days=90),
            "terms_conditions": "Valid for groups of 3 people only. Classes must be booked and taken together. Package expires 30 days after purchase.",
            "max_redemptions": 50,
            "current_redemptions": 8,
            "active": True,
            "created_at": datetime.utcnow()
        },
        # Additional new offers to make merchant page more engaging
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[0]["id"],  # AMC Third Offer
            "merchant_name": merchants[0]["business_name"],
            "title": "Student Movie Night - 50% Off Tuesday Tickets! 🎓",
            "description": "Students unite! Every Tuesday, bring your study buddies and get 50% off all movie tickets. Perfect for unwinding after a long day of classes!",
            "discount_percentage": 50,
            "minimum_buddies": 2,
            "valid_until": base_date + timedelta(days=120),
            "terms_conditions": "Valid Tuesdays only. Must show valid student ID. Minimum 2 tickets per transaction.",
            "max_redemptions": 400,
            "current_redemptions": 156,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[5]["id"] if len(merchants) > 5 else merchants[0]["id"],  # TopGolf Second Offer
            "merchant_name": merchants[5]["business_name"] if len(merchants) > 5 else "TopGolf San Jose",
            "title": "Corporate Team Building - 25% Off Private Bays! ⛳",
            "description": "Build stronger teams with TopGolf! Corporate groups of 8+ get 25% off private bay rentals. Includes team challenges and networking opportunities.",
            "discount_percentage": 25,
            "minimum_buddies": 8,
            "valid_until": base_date + timedelta(days=180),
            "terms_conditions": "Valid for corporate bookings only. Advance reservation required. Includes 2-hour bay rental and team activities.",
            "max_redemptions": 50,
            "current_redemptions": 12,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[6]["id"] if len(merchants) > 6 else merchants[1]["id"],  # Cheesecake Factory Second Offer
            "merchant_name": merchants[6]["business_name"] if len(merchants) > 6 else "The Cheesecake Factory",
            "title": "Happy Hour Buddies - Buy 2 Get 1 Free Appetizers! 🍽️",
            "description": "Happy hour just got happier! Groups of 3+ ordering appetizers get the third one free. Perfect for after-work meetups with colleagues!",
            "discount_percentage": 33,
            "minimum_buddies": 3,
            "valid_until": base_date + timedelta(days=60),
            "terms_conditions": "Valid Monday-Friday 3-6 PM only. Dine-in only. Free appetizer must be equal or lesser value.",
            "max_redemptions": 300,
            "current_redemptions": 89,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[7]["id"] if len(merchants) > 7 else merchants[2]["id"],  # Dave & Buster's Second Offer
            "merchant_name": merchants[7]["business_name"] if len(merchants) > 7 else "Dave & Buster's",
            "title": "Birthday Party Package - 20% Off Group Celebrations! 🎂",
            "description": "Make birthdays legendary! Groups celebrating birthdays get 20% off party packages including games, food, and reserved seating.",
            "discount_percentage": 20,
            "minimum_buddies": 6,
            "valid_until": base_date + timedelta(days=365),
            "terms_conditions": "Valid for birthday celebrations only. Must mention birthday when booking. Includes party host and decorations.",
            "max_redemptions": 100,
            "current_redemptions": 23,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[8]["id"] if len(merchants) > 8 else merchants[3]["id"],  # Urban Air Second Offer
            "merchant_name": merchants[8]["business_name"] if len(merchants) > 8 else "Urban Air Adventure Park",
            "title": "Weekend Warriors - 30% Off Saturday Adventures! 🤸‍♂️",
            "description": "Weekend adventure squad assemble! Saturday groups of 5+ get 30% off all adventure packages. Perfect for active friend groups!",
            "discount_percentage": 30,
            "minimum_buddies": 5,
            "valid_until": base_date + timedelta(days=90),
            "terms_conditions": "Valid Saturdays only. Groups of 5-15 people. Includes full adventure park access and safety equipment.",
            "max_redemptions": 75,
            "current_redemptions": 34,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[9]["id"] if len(merchants) > 9 else merchants[4]["id"],  # Starbucks Reserve Second Offer
            "merchant_name": merchants[9]["business_name"] if len(merchants) > 9 else "Starbucks Reserve",
            "title": "Study Group Special - Free Wifi + 15% Off! 📚",
            "description": "Study buddies welcome! Groups studying together get 15% off all food and drinks plus priority seating in our quiet zones.",
            "discount_percentage": 15,
            "minimum_buddies": 3,
            "valid_until": base_date + timedelta(days=120),
            "terms_conditions": "Valid for study groups only. Must stay minimum 2 hours. Quiet zones available first-come-first-served.",
            "max_redemptions": 200,
            "current_redemptions": 67,
            "active": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "merchant_id": merchants[10]["id"] if len(merchants) > 10 else merchants[0]["id"],  # Bowlero Second Offer
            "merchant_name": merchants[10]["business_name"] if len(merchants) > 10 else "Bowlero Fremont",
            "title": "League Night - Join with Friends & Save 40%! 🎳",
            "description": "Start a bowling league with your crew! Groups of 4+ joining our weekly leagues get 40% off league fees for the first month.",
            "discount_percentage": 40,
            "minimum_buddies": 4,
            "valid_until": base_date + timedelta(days=30),
            "terms_conditions": "Valid for new league signups only. Minimum 4-week commitment. Includes shoes and weekly league play.",
            "max_redemptions": 25,
            "current_redemptions": 8,
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