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
        self.tests_run = 0
        self.tests_passed = 0
        self.test_user_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
        self.test_password = "TestPass123!"
        self.test_activity_id = None

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

    def test_get_activity_feed(self):
        """Test getting personalized activity feed"""
        success, response = self.run_test(
            "Get Activity Feed",
            "GET",
            "activities/feed",
            200
        )
        
        if success:
            activities = response.get('activities', [])
            print(f"Received {len(activities)} activities in feed")
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
        
        # Store second user's token
        second_user_token = self.token
        
        # Restore original user to create a new activity
        self.token = original_token
        self.user = original_user
        
        # Create a new activity for the second user to join
        tomorrow = datetime.now() + timedelta(days=1)
        activity_data = {
            "title": "Test Activity for Joining",
            "description": "This is a test activity for the second user to join",
            "date": tomorrow.isoformat(),
            "location": "Test Location",
            "city": "Test City",
            "category": "Testing",
            "max_participants": 10,
            "interests": ["testing", "coding", "api"]
        }
        
        success, response = self.run_test(
            "Create Activity for Joining",
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
        
        # Switch to second user
        self.token = second_user_token
        
        # Now join the activity with the second user
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
        
        # Restore original token and user
        self.token = original_token
        self.user = original_user
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
            
        # Test getting activity feed
        if not self.test_get_activity_feed():
            print("❌ Getting activity feed failed")
            
        # Test joining activity
        if not self.test_join_activity():
            print("❌ Joining activity failed")
            
        # Test getting my activities
        if not self.test_get_my_activities():
            print("❌ Getting my activities failed")
            
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