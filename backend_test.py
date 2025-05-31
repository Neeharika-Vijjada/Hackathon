import requests
import sys
import json
import uuid
from datetime import datetime, timedelta

class FindBuddyAPITester:
    def __init__(self, base_url="https://73ee5915-138a-4431-a2f0-3f395e3de1fc.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user = None
        self.merchant = None
        self.merchant_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_user_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
        self.test_merchant_email = f"test_merchant_{uuid.uuid4().hex[:8]}@example.com"
        self.test_password = "TestPass123!"
        self.test_activity_id = None
        self.test_discount_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
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
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json().get('detail', 'No detail provided')
                    print(f"Error detail: {error_detail}")
                except:
                    print(f"Response text: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test API health check endpoint"""
        success, response = self.run_test(
            "API Health Check",
            "GET",
            "",
            200
        )
        if success:
            print(f"API Message: {response.get('message', 'No message')}")
        return success

    def test_register_user(self):
        """Test user registration"""
        user_data = {
            "name": "Test User",
            "email": self.test_user_email,
            "password": self.test_password,
            "city": "Test City",
            "phone": "1234567890",
            "bio": "This is a test user for API testing",
            "interests": ["hiking", "reading", "coding"]
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=user_data
        )
        
        if success and 'token' in response:
            self.token = response['token']
            self.user = response.get('user')
            print(f"Registered user with email: {self.test_user_email}")
            return True
        return False

    def test_login(self):
        """Test user login"""
        login_data = {
            "email": self.test_user_email,
            "password": self.test_password
        }
        
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data=login_data
        )
        
        if success and 'token' in response:
            self.token = response['token']
            self.user = response.get('user')
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
        
        if success:
            print(f"Current user: {response.get('name', 'Unknown')}")
        return success

    def test_create_activity(self):
        """Test creating a new activity"""
        tomorrow = datetime.now() + timedelta(days=1)
        activity_data = {
            "title": "Test Activity",
            "description": "This is a test activity created by the API tester",
            "date": tomorrow.isoformat(),
            "location": "Test Location",
            "city": "Test City",
            "category": "Testing",
            "max_participants": 10,
            "interests": ["testing", "coding", "api"]
        }
        
        success, response = self.run_test(
            "Create Activity",
            "POST",
            "activities",
            200,
            data=activity_data
        )
        
        if success and 'activity' in response:
            self.test_activity_id = response['activity']['id']
            print(f"Created activity with ID: {self.test_activity_id}")
            return True
        return False

    def test_get_activities_around_me(self):
        """Test getting activities around me"""
        success, response = self.run_test(
            "Get Activities Around Me",
            "GET",
            "activities/around-me",
            200
        )
        
        if success:
            activities = response.get('activities', [])
            print(f"Received {len(activities)} activities around me")
        return success

    def test_join_activity(self):
        """Test joining an activity"""
        if not self.test_activity_id:
            print("❌ No activity ID available to join")
            return False
        
        # Create a second user to join the activity
        second_user_email = f"test_user2_{uuid.uuid4().hex[:8]}@example.com"
        second_user_data = {
            "name": "Test User 2",
            "email": second_user_email,
            "password": self.test_password,
            "city": "Test City",
            "phone": "1234567890",
            "bio": "This is a second test user for API testing",
            "interests": ["hiking", "reading", "coding"]
        }
        
        # Save current token and user
        original_token = self.token
        original_user = self.user
        
        # Register second user
        success, response = self.run_test(
            "Register Second User",
            "POST",
            "auth/register",
            200,
            data=second_user_data
        )
        
        if not success:
            # Restore original token and user
            self.token = original_token
            self.user = original_user
            return False
        
        # Store second user's token and ID
        second_user_token = self.token
        second_user_id = response.get('user', {}).get('id')
        
        # Have second user create an activity
        tomorrow = datetime.now() + timedelta(days=1)
        activity_data = {
            "title": "Second User's Activity",
            "description": "This is an activity created by the second user",
            "date": tomorrow.isoformat(),
            "location": "Test Location",
            "city": "Test City",
            "category": "Testing",
            "max_participants": 10,
            "interests": ["testing", "coding", "api"]
        }
        
        success, response = self.run_test(
            "Create Activity as Second User",
            "POST",
            "activities",
            200,
            data=activity_data
        )
        
        if not success or 'activity' not in response:
            # Restore original token and user
            self.token = original_token
            self.user = original_user
            return False
            
        activity_id_to_join = response['activity']['id']
        
        # Switch back to first user
        self.token = original_token
        self.user = original_user
        
        # Now join the activity with the first user
        join_data = {
            "activity_id": activity_id_to_join
        }
        
        success, response = self.run_test(
            "Join Activity",
            "POST",
            "activities/join",
            200,
            data=join_data
        )
        
        if success:
            print(f"Successfully joined activity: {activity_id_to_join}")
            
            # Verify the user is now in the participants list
            # Get my activities to verify
            success, my_activities_response = self.run_test(
                "Verify Joined Activities",
                "GET",
                "activities/my",
                200
            )
            
            if success:
                joined_activities = my_activities_response.get('joined_activities', [])
                joined_ids = [act.get('id') for act in joined_activities]
                
                if activity_id_to_join in joined_ids:
                    print(f"✅ Verified user is in participants list for activity {activity_id_to_join}")
                else:
                    print(f"❌ User not found in participants list for activity {activity_id_to_join}")
                    success = False
        
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
            print(f"User has {len(created)} created activities and {len(joined)} joined activities")
        return success

    # New tests for merchant functionality
    def test_register_merchant(self):
        """Test merchant registration"""
        merchant_data = {
            "business_name": "Test Business",
            "email": self.test_merchant_email,
            "password": self.test_password,
            "business_type": "restaurant",
            "address": "123 Test St",
            "city": "Test City",
            "phone": "1234567890",
            "description": "This is a test business for API testing",
            "website": "https://testbusiness.com"
        }
        
        # Save current token and user
        original_token = self.token
        original_user = self.user
        
        success, response = self.run_test(
            "Merchant Registration",
            "POST",
            "merchants/register",
            200,
            data=merchant_data
        )
        
        if success and 'token' in response:
            self.merchant_token = response['token']
            self.merchant = response.get('merchant')
            print(f"Registered merchant with email: {self.test_merchant_email}")
            
            # Store merchant token but restore user token for other tests
            self.token = original_token
            self.user = original_user
            return True
        
        # Restore original token and user
        self.token = original_token
        self.user = original_user
        return False

    def test_merchant_login(self):
        """Test merchant login"""
        login_data = {
            "email": self.test_merchant_email,
            "password": self.test_password
        }
        
        # Save current token and user
        original_token = self.token
        original_user = self.user
        
        success, response = self.run_test(
            "Merchant Login",
            "POST",
            "merchants/login",
            200,
            data=login_data
        )
        
        if success and 'token' in response:
            self.merchant_token = response['token']
            self.merchant = response.get('merchant')
            
            # Use merchant token temporarily
            self.token = self.merchant_token
            
            # Test getting merchant info
            success_info, merchant_info = self.run_test(
                "Get Current Merchant",
                "GET",
                "merchants/me",
                200
            )
            
            if success_info:
                print(f"Current merchant: {merchant_info.get('business_name', 'Unknown')}")
            
            # Restore original token and user
            self.token = original_token
            self.user = original_user
            return success_info
        
        # Restore original token and user
        self.token = original_token
        self.user = original_user
        return False

    def test_create_discount_offer(self):
        """Test creating a discount offer as a merchant"""
        if not self.merchant_token:
            print("❌ No merchant token available to create discount")
            return False
        
        # Save current token and user
        original_token = self.token
        original_user = self.user
        
        # Use merchant token
        self.token = self.merchant_token
        
        # Create discount offer
        next_month = datetime.now() + timedelta(days=30)
        discount_data = {
            "title": "Test Discount",
            "description": "This is a test discount created by the API tester",
            "discount_percentage": 20,
            "minimum_buddies": 2,
            "valid_until": next_month.isoformat(),
            "terms_conditions": "Test terms and conditions",
            "max_redemptions": 100
        }
        
        success, response = self.run_test(
            "Create Discount Offer",
            "POST",
            "merchants/discounts",
            200,
            data=discount_data
        )
        
        if success and 'discount' in response:
            self.test_discount_id = response['discount']['id']
            print(f"Created discount offer with ID: {self.test_discount_id}")
            
            # Test getting merchant's discount offers
            success_get, discounts_response = self.run_test(
                "Get Merchant's Discount Offers",
                "GET",
                "merchants/discounts/my",
                200
            )
            
            if success_get:
                discounts = discounts_response.get('discounts', [])
                print(f"Merchant has {len(discounts)} discount offers")
            
            # Restore original token and user
            self.token = original_token
            self.user = original_user
            return success_get
        
        # Restore original token and user
        self.token = original_token
        self.user = original_user
        return False

    def test_get_merchants_near_me(self):
        """Test getting merchants near me as a user"""
        success, response = self.run_test(
            "Get Merchants Near Me",
            "GET",
            "merchants/near-me",
            200
        )
        
        if success:
            merchants = response.get('merchants', [])
            print(f"Received {len(merchants)} merchants near me")
            
            # Check if our test merchant is in the list
            if self.merchant:
                merchant_ids = [m.get('merchant', {}).get('id') for m in merchants]
                if self.merchant.get('id') in merchant_ids:
                    print(f"✅ Found our test merchant in the list")
                else:
                    print(f"❌ Our test merchant not found in the list")
        
        return success

    def test_get_all_discounts(self):
        """Test getting all discount offers as a user"""
        success, response = self.run_test(
            "Get All Discount Offers",
            "GET",
            "discounts/all",
            200
        )
        
        if success:
            discounts = response.get('discounts', [])
            print(f"Received {len(discounts)} discount offers")
            
            # Check if our test discount is in the list
            if self.test_discount_id:
                discount_ids = [d.get('id') for d in discounts]
                if self.test_discount_id in discount_ids:
                    print(f"✅ Found our test discount in the list")
                else:
                    print(f"❌ Our test discount not found in the list")
        
        return success

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting FindBuddy API Tests")
        
        # Test health check
        if not self.test_health_check():
            print("❌ Health check failed, stopping tests")
            return False
            
        # Test user registration
        if not self.test_register_user():
            print("❌ User registration failed, stopping tests")
            return False
            
        # Test getting current user
        if not self.test_get_current_user():
            print("❌ Getting current user failed")
            
        # Test creating activity
        if not self.test_create_activity():
            print("❌ Creating activity failed")
            
        # Test getting activities around me
        if not self.test_get_activities_around_me():
            print("❌ Getting activities around me failed")
            
        # Test joining activity
        if not self.test_join_activity():
            print("❌ Joining activity failed")
            
        # Test getting my activities
        if not self.test_get_my_activities():
            print("❌ Getting my activities failed")
            
        # Test merchant registration
        if not self.test_register_merchant():
            print("❌ Merchant registration failed")
        
        # Test merchant login
        if not self.test_merchant_login():
            print("❌ Merchant login failed")
        
        # Test creating discount offer
        if not self.test_create_discount_offer():
            print("❌ Creating discount offer failed")
        
        # Test getting merchants near me
        if not self.test_get_merchants_near_me():
            print("❌ Getting merchants near me failed")
        
        # Test getting all discounts
        if not self.test_get_all_discounts():
            print("❌ Getting all discounts failed")
        
        # Test login with the created user
        if not self.test_login():
            print("❌ Login failed")
            
        # Print results
        print(f"\n📊 Tests passed: {self.tests_passed}/{self.tests_run}")
        return self.tests_passed == self.tests_run

def main():
    tester = FindBuddyAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())