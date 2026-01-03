import requests
import sys
import json
from datetime import datetime

class FinancialAdvisorAPITester:
    def __init__(self, base_url="https://moneygrowth-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
        
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    {details}")

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=30)

            success = response.status_code == expected_status
            
            if success:
                try:
                    response_data = response.json()
                    self.log_test(name, True, f"Status: {response.status_code}")
                    return True, response_data
                except:
                    self.log_test(name, True, f"Status: {response.status_code} (No JSON response)")
                    return True, {}
            else:
                try:
                    error_data = response.json()
                    self.log_test(name, False, f"Expected {expected_status}, got {response.status_code}: {error_data}")
                except:
                    self.log_test(name, False, f"Expected {expected_status}, got {response.status_code}: {response.text}")
                return False, {}

        except Exception as e:
            self.log_test(name, False, f"Error: {str(e)}")
            return False, {}

    def test_auth_flow(self):
        """Test authentication flow"""
        print("\n🔐 Testing Authentication Flow...")
        
        # Test user registration
        test_user_data = {
            "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
            "password": "TestPass123!",
            "full_name": "Test User"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=test_user_data
        )
        
        if success and 'token' in response:
            self.token = response['token']
            self.user_id = response['user']['id']
            
            # Test login with same credentials
            login_success, login_response = self.run_test(
                "User Login",
                "POST",
                "auth/login",
                200,
                data={"email": test_user_data["email"], "password": test_user_data["password"]}
            )
            
            # Test get current user
            self.run_test(
                "Get Current User",
                "GET",
                "auth/me",
                200
            )
            
            return True
        else:
            print("❌ Registration failed, cannot continue with authenticated tests")
            return False

    def test_profile_management(self):
        """Test profile management"""
        print("\n👤 Testing Profile Management...")
        
        # Get initial profile
        self.run_test(
            "Get Profile",
            "GET",
            "profile",
            200
        )
        
        # Update profile
        profile_update = {
            "monthly_income": 5000.0,
            "monthly_expenses": 3000.0,
            "savings_goal": 10000.0,
            "risk_tolerance": "moderate",
            "skills": ["programming", "writing"],
            "location": "New York, USA",
            "time_availability": "part-time",
            "financial_level": "intermediate"
        }
        
        self.run_test(
            "Update Profile",
            "PUT",
            "profile",
            200,
            data=profile_update
        )

    def test_income_generation(self):
        """Test income generation module"""
        print("\n💰 Testing Income Generation Module...")
        
        # Generate income opportunities
        success, response = self.run_test(
            "Generate Income Opportunities",
            "POST",
            "income-generation",
            200
        )
        
        # Get income opportunities
        self.run_test(
            "Get Income Opportunities",
            "GET",
            "income-generation",
            200
        )

    def test_budget_analysis(self):
        """Test budget analysis module"""
        print("\n📊 Testing Budget Analysis Module...")
        
        # Analyze budget
        success, response = self.run_test(
            "Analyze Budget",
            "POST",
            "budget/analyze",
            200
        )
        
        # Get latest budget analysis
        self.run_test(
            "Get Latest Budget Analysis",
            "GET",
            "budget/latest",
            200
        )

    def test_investment_advisor(self):
        """Test investment advisor module"""
        print("\n📈 Testing Investment Advisor Module...")
        
        # Get investment advice
        success, response = self.run_test(
            "Get Investment Advice",
            "POST",
            "investment/advice",
            200
        )
        
        # Get latest investment advice
        self.run_test(
            "Get Latest Investment Advice",
            "GET",
            "investment/latest",
            200
        )

    def test_opportunity_scanner(self):
        """Test opportunity scanner module"""
        print("\n🔍 Testing Opportunity Scanner Module...")
        
        # Scan opportunities
        success, response = self.run_test(
            "Scan Opportunities",
            "POST",
            "opportunities/scan",
            200
        )
        
        # Get latest opportunity scan
        self.run_test(
            "Get Latest Opportunity Scan",
            "GET",
            "opportunities/latest",
            200
        )

    def test_education_hub(self):
        """Test education hub module"""
        print("\n🎓 Testing Education Hub Module...")
        
        # Get lessons
        self.run_test(
            "Get All Lessons",
            "GET",
            "education/lessons?level=all",
            200
        )
        
        self.run_test(
            "Get Beginner Lessons",
            "GET",
            "education/lessons?level=beginner",
            200
        )
        
        # Complete a lesson
        self.run_test(
            "Complete Lesson",
            "POST",
            "education/complete/1",
            200
        )
        
        # Get progress
        self.run_test(
            "Get Progress",
            "GET",
            "education/progress",
            200
        )

    def test_ai_chat(self):
        """Test AI chat module"""
        print("\n🤖 Testing AI Chat Module...")
        
        # Send chat message
        chat_data = {
            "message": "What are some good investment strategies for beginners?",
            "context": {}
        }
        
        success, response = self.run_test(
            "Send Chat Message",
            "POST",
            "ai-chat",
            200,
            data=chat_data
        )
        
        # Get chat history
        self.run_test(
            "Get Chat History",
            "GET",
            "ai-chat/history",
            200
        )

    def test_market_data(self):
        """Test market data endpoints"""
        print("\n📊 Testing Market Data...")
        
        # Get market overview
        self.run_test(
            "Get Market Overview",
            "GET",
            "market/overview",
            200
        )
        
        # Get specific stock data
        self.run_test(
            "Get Stock Data (AAPL)",
            "GET",
            "market/stock/AAPL",
            200
        )

    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        print("\n📋 Testing Dashboard Stats...")
        
        self.run_test(
            "Get Dashboard Stats",
            "GET",
            "dashboard/stats",
            200
        )

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting AI Financial Growth Advisor API Tests")
        print(f"🌐 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test authentication first
        if not self.test_auth_flow():
            print("\n❌ Authentication failed - stopping tests")
            return False
        
        # Test all modules
        self.test_profile_management()
        self.test_income_generation()
        self.test_budget_analysis()
        self.test_investment_advisor()
        self.test_opportunity_scanner()
        self.test_education_hub()
        self.test_ai_chat()
        self.test_market_data()
        self.test_dashboard_stats()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed - check details above")
            return False

def main():
    tester = FinancialAdvisorAPITester()
    success = tester.run_all_tests()
    
    # Save test results
    with open('/app/test_reports/backend_test_results.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_tests": tester.tests_run,
            "passed_tests": tester.tests_passed,
            "success_rate": (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0,
            "results": tester.test_results
        }, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())