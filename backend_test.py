
import requests
import sys
import random
import string
import time
from datetime import datetime, timedelta

class FindBuddyAPITester:
    def __init__(self, base_url="https://73ee5915-138a-4431-a2f0-3f395e3de1fc.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.user_token = None
        self.merchant_token = None
        self.user_data = None
        self.merchant_data = None
        self.activity_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, token=None, is_merchant=False):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if token:
            headers['Authorization'] = f'Bearer {token}'
        elif is_merchant and self.merchant_token:
            headers['Authorization'] = f'Bearer {self.merchant_token}'
        elif not is_merchant and self.user_token:
            headers['Authorization'] = f'Bearer {self.user_token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                self.test_results.append({"name": name, "status": "PASSED", "details": f"Status: {response.status_code}"})
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                self.test_results.append({"name": name, "status": "FAILED", "details": f"Expected {expected_status}, got {response.status_code}"})
                if response.text:
                    print(f"Response: {response.text}")

            try:
                return success, response.json() if response.text else {}
            except:
                return success, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({"name": name, "status": "FAILED", "details": f"Error: {str(e)}"})
            return False, {}

    def generate_random_string(self, length=8):
        """Generate a random string for test data"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def test_health_check(self):
        """Test API health check endpoint"""
        success, response = self.run_test(
            "API Health Check",
            "GET",
            "",
            200
        )
        return success

    def test_user_registration(self):
        """Test user registration"""
        random_suffix = self.generate_random_string()
        user_data = {
            "name": f"Test User {random_suffix}",
            "email": f"test.user.{random_suffix}@example.com",
            "password": "TestPassword123!",
            "city": "Test City",
            "phone": "1234567890",
            "bio": "This is a test user for API testing",
            "interests": ["networking", "technology", "professional development"]
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=user_data
        )
        
        if success and 'token' in response:
            self.user_token = response['token']
            self.user_data = response['user']
            return True
        return False

    def test_user_login(self):
        """Test user login with the registered user"""
        if not self.user_data:
            print("❌ No user data available for login test")
            return False
            
        login_data = {
            "email": self.user_data["email"],
            "password": "TestPassword123!"
        }
        
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data=login_data
        )
        
        if success and 'token' in response:
            self.user_token = response['token']
            return True
        return False

    def test_get_current_user(self):
        """Test getting current user info"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        return success

    def test_merchant_registration(self):
        """Test merchant registration"""
        random_suffix = self.generate_random_string()
        merchant_data = {
            "business_name": f"Test Business {random_suffix}",
            "email": f"test.business.{random_suffix}@example.com",
            "password": "TestPassword123!",
            "business_type": "restaurant",
            "address": "123 Test Street",
            "city": "Test City",
            "phone": "1234567890",
            "description": "This is a test business for API testing",
            "website": "https://testbusiness.example.com"
        }
        
        success, response = self.run_test(
            "Merchant Registration",
            "POST",
            "merchants/register",
            200,
            data=merchant_data
        )
        
        if success and 'token' in response:
            self.merchant_token = response['token']
            self.merchant_data = response['merchant']
            return True
        return False

    def test_merchant_login(self):
        """Test merchant login with the registered merchant"""
        if not self.merchant_data:
            print("❌ No merchant data available for login test")
            return False
            
        login_data = {
            "email": self.merchant_data["email"],
            "password": "TestPassword123!"
        }
        
        success, response = self.run_test(
            "Merchant Login",
            "POST",
            "merchants/login",
            200,
            data=login_data
        )
        
        if success and 'token' in response:
            self.merchant_token = response['token']
            return True
        return False

    def test_get_current_merchant(self):
        """Test getting current merchant info"""
        success, response = self.run_test(
            "Get Current Merchant",
            "GET",
            "merchants/me",
            200,
            is_merchant=True
        )
        return success

    def test_create_activity(self):
        """Test creating a professional networking activity"""
        tomorrow = datetime.now() + timedelta(days=1)
        
        activity_data = {
            "title": "🚀 Exciting Career Networking Event - Tech Professionals Welcome!",
            "description": "Join us for an evening of professional networking with tech industry leaders. Great opportunity to expand your professional network and discover new career opportunities. #TechNetworking #CareerGrowth",
            "date": tomorrow.isoformat(),
            "location": "Tech Hub Downtown",
            "city": "Test City",
            "max_participants": 50,
            "category": "Professional",
            "interests": ["technology", "networking", "career development"]
        }
        
        success, response = self.run_test(
            "Create Professional Activity",
            "POST",
            "activities",
            200,
            data=activity_data
        )
        
        if success and 'activity' in response:
            self.activity_id = response['activity']['id']
            return True
        return False

    def test_get_activities_around_me(self):
        """Test getting activities around me (now called 'Find Buddies')"""
        success, response = self.run_test(
            "Get Activities Around Me (Find Buddies)",
            "GET",
            "activities/around-me",
            200
        )
        
        if success:
            # Check if we have LinkedIn-style professional activities
            activities = response.get('activities', [])
            professional_activities = [a for a in activities if 'Professional' in a.get('category', '')]
            
            if professional_activities:
                print(f"✅ Found {len(professional_activities)} professional activities")
                return True
            else:
                print("❌ No professional activities found")
                return False
        return False
        
    def test_activities_with_city_filter(self):
        """Test getting activities with city filter"""
        success, response = self.run_test(
            "Get Activities with City Filter",
            "GET",
            "activities/around-me?city_filter=Test%20City",
            200
        )
        
        if success:
            activities = response.get('activities', [])
            city = response.get('city', '')
            print(f"✅ Found {len(activities)} activities in {city}")
            return True
        return False

    def test_join_activity(self):
        """Test joining an activity"""
        if not self.activity_id:
            print("❌ No activity available to join")
            return False
            
        join_data = {
            "activity_id": self.activity_id
        }
        
        # Create a second user to join the activity
        self.test_user_registration()
        
        success, _ = self.run_test(
            "Join Activity",
            "POST",
            "activities/join",
            200,
            data=join_data
        )
        return success

    def test_get_my_activities(self):
        """Test getting user's activities"""
        success, response = self.run_test(
            "Get My Activities",
            "GET",
            "activities/my",
            200
        )
        
        if success:
            created = response.get('created_activities', [])
            joined = response.get('joined_activities', [])
            print(f"✅ User has {len(created)} created and {len(joined)} joined activities")
        return success

    def test_create_discount_offer(self):
        """Test creating a discount offer as a merchant"""
        next_month = datetime.now() + timedelta(days=30)
        
        discount_data = {
            "title": "Group Discount for Tech Professionals",
            "description": "Bring your colleagues from the networking event and save!",
            "discount_percentage": 20,
            "minimum_buddies": 3,
            "valid_until": next_month.isoformat(),
            "terms_conditions": "Valid for groups of 3 or more. Must show FindBuddy app."
        }
        
        success, response = self.run_test(
            "Create Discount Offer",
            "POST",
            "merchants/discounts",
            200,
            data=discount_data,
            is_merchant=True
        )
        return success

    def test_get_merchants_near_me(self):
        """Test getting merchants near me"""
        success, response = self.run_test(
            "Get Merchants Near Me",
            "GET",
            "merchants/near-me",
            200
        )
        
        if success:
            merchants = response.get('merchants', [])
            print(f"✅ Found {len(merchants)} merchants near me")
        return success

    def test_get_all_discount_offers(self):
        """Test getting all discount offers"""
        success, response = self.run_test(
            "Get All Discount Offers",
            "GET",
            "discounts/all",
            200
        )
        
        if success:
            discounts = response.get('discounts', [])
            print(f"✅ Found {len(discounts)} discount offers")
        return success

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting FindBuddy API Tests...")
        
        # Health check
        self.test_health_check()
        
        # User authentication tests
        self.test_user_registration()
        self.test_user_login()
        self.test_get_current_user()
        
        # Merchant authentication tests
        self.test_merchant_registration()
        self.test_merchant_login()
        self.test_get_current_merchant()
        
        # Activity tests
        self.test_create_activity()
        self.test_get_activities_around_me()
        self.test_join_activity()
        self.test_get_my_activities()
        
        # Merchant and discount tests
        self.test_create_discount_offer()
        self.test_get_merchants_near_me()
        self.test_get_all_discount_offers()
        
        # Print results
        print("\n📊 Test Results:")
        print(f"Tests passed: {self.tests_passed}/{self.tests_run} ({self.tests_passed/self.tests_run*100:.1f}%)")
        
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {result['name']}: {result['status']}")
        
        return self.tests_passed == self.tests_run

def main():
    # Get the backend URL from environment or use default
    tester = FindBuddyAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
