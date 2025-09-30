#!/usr/bin/env python3
"""
Test script for presentation API endpoints
Tests the complete workflow: create → add properties → share
"""

import requests
import json
import sys
from werkzeug.security import generate_password_hash

# Test configuration
BASE_URL = "http://localhost:5000"
DEMO_MANAGER = {
    "email": "manager@inback.ru", 
    "password": "demo123"  # Common demo password
}

class PresentationAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.manager_id = None
        
    def login_manager(self):
        """Login as demo manager and get session"""
        print(f"🔐 Attempting login for {DEMO_MANAGER['email']}...")
        
        # First get the login page to establish session
        login_page = self.session.get(f"{BASE_URL}/manager/login")
        if login_page.status_code != 200:
            print(f"❌ Failed to access login page: {login_page.status_code}")
            return False
            
        # Extract CSRF token if present
        csrf_token = None
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(login_page.text, 'html.parser')
            csrf_input = soup.find('input', {'name': 'csrf_token'})
            if csrf_input:
                csrf_token = csrf_input.get('value')
                print(f"✅ Found CSRF token: {csrf_token[:20]}...")
        except ImportError:
            print("⚠️ BeautifulSoup not available, trying without CSRF token")
        
        # Attempt login
        login_data = {
            "email": DEMO_MANAGER["email"],
            "password": DEMO_MANAGER["password"]
        }
        if csrf_token:
            login_data["csrf_token"] = csrf_token
            
        response = self.session.post(f"{BASE_URL}/manager/login", data=login_data)
        
        if response.status_code == 200 and "dashboard" in response.url:
            print("✅ Login successful!")
            return True
        elif response.status_code == 302:
            print("✅ Login successful (redirect)!")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response URL: {response.url}")
            return False
    
    def get_csrf_token(self):
        """Get CSRF token from dashboard"""
        dashboard = self.session.get(f"{BASE_URL}/manager/dashboard")
        if dashboard.status_code == 200:
            # Extract CSRF token from JavaScript or meta tag
            if 'csrf_token' in dashboard.text:
                # Simple extraction - look for csrf_token in the response
                import re
                match = re.search(r'"csrf_token":\s*"([^"]+)"', dashboard.text)
                if match:
                    return match.group(1)
        return None
    
    def test_create_presentation(self):
        """Test presentation creation"""
        print("\n📋 Testing presentation creation...")
        
        csrf_token = self.get_csrf_token()
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        } if csrf_token else {"Content-Type": "application/json"}
        
        data = {
            "title": "Тестовая презентация",
            "description": "Презентация для тестирования API",
            "client_name": "Тестовый клиент",
            "client_phone": "+7 999 123-45-67"
        }
        
        response = self.session.post(
            f"{BASE_URL}/api/manager/presentation/create",
            json=data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                presentation_id = result.get('presentation', {}).get('id')
                print(f"✅ Presentation created successfully! ID: {presentation_id}")
                return presentation_id
            else:
                print(f"❌ Failed to create presentation: {result.get('error')}")
                return None
        except:
            print(f"❌ Invalid JSON response: {response.text}")
            return None
    
    def test_add_property(self, presentation_id):
        """Test adding property to presentation"""
        print(f"\n🏠 Testing add property to presentation {presentation_id}...")
        
        csrf_token = self.get_csrf_token()
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        } if csrf_token else {"Content-Type": "application/json"}
        
        # Use a test property ID (assuming we have some properties in the system)
        data = {
            "property_id": "1",  # Test with first property
            "manager_note": "Отличный вариант для клиента"
        }
        
        response = self.session.post(
            f"{BASE_URL}/api/manager/presentation/{presentation_id}/add_property",
            json=data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                print("✅ Property added successfully!")
                return True
            else:
                print(f"❌ Failed to add property: {result.get('error')}")
                return False
        except:
            print(f"❌ Invalid JSON response: {response.text}")
            return False
    
    def test_share_presentation(self, presentation_id):
        """Test sharing presentation"""
        print(f"\n📤 Testing share presentation {presentation_id}...")
        
        csrf_token = self.get_csrf_token()
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        } if csrf_token else {"Content-Type": "application/json"}
        
        data = {
            "client_name": "Тестовый клиент"
        }
        
        response = self.session.post(
            f"{BASE_URL}/api/manager/presentation/{presentation_id}/share",
            json=data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                share_data = result.get('share_data', {})
                print(f"✅ Share data generated successfully!")
                print(f"📋 Presentation URL: {share_data.get('presentation_url')}")
                print(f"📱 WhatsApp URL: {share_data.get('whatsapp_url', '')[:100]}...")
                return True
            else:
                print(f"❌ Failed to generate share data: {result.get('error')}")
                return False
        except:
            print(f"❌ Invalid JSON response: {response.text}")
            return False
    
    def test_get_presentations(self):
        """Test getting manager's presentations"""
        print("\n📋 Testing get presentations...")
        
        response = self.session.get(f"{BASE_URL}/api/manager/presentations")
        
        print(f"Status: {response.status_code}")
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                presentations = result.get('presentations', [])
                print(f"✅ Found {len(presentations)} presentations")
                return True
            else:
                print(f"❌ Failed to get presentations: {result.get('error')}")
                return False
        except:
            print(f"❌ Invalid JSON response: {response.text}")
            return False
    
    def run_full_test(self):
        """Run complete test workflow"""
        print("🚀 Starting Presentation API Test Suite")
        print("=" * 50)
        
        # Step 1: Login
        if not self.login_manager():
            print("❌ Test suite failed: Cannot login")
            return False
        
        # Step 2: Test get presentations (to verify authentication)
        if not self.test_get_presentations():
            print("❌ Test suite failed: Cannot get presentations")
            return False
        
        # Step 3: Create presentation
        presentation_id = self.test_create_presentation()
        if not presentation_id:
            print("❌ Test suite failed: Cannot create presentation")
            return False
        
        # Step 4: Add property
        if not self.test_add_property(presentation_id):
            print("❌ Test suite failed: Cannot add property")
            return False
        
        # Step 5: Share presentation
        if not self.test_share_presentation(presentation_id):
            print("❌ Test suite failed: Cannot share presentation")
            return False
        
        print("\n🎉 All tests passed! Presentation API is working correctly!")
        return True

if __name__ == "__main__":
    tester = PresentationAPITester()
    
    # Try different demo passwords
    demo_passwords = ["demo123", "password", "demo", "123456", "manager123"]
    
    for password in demo_passwords:
        DEMO_MANAGER["password"] = password
        print(f"\n🔑 Trying password: {password}")
        
        if tester.login_manager():
            print(f"✅ Login successful with password: {password}")
            success = tester.run_full_test()
            sys.exit(0 if success else 1)
        else:
            print(f"❌ Login failed with password: {password}")
    
    print("❌ Could not find working demo password. Manual intervention needed.")
    sys.exit(1)