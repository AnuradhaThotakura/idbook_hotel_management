from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from booking_details.models import Booking
from datetime import datetime, time, timedelta
import json

class HotelBookingAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="admin123")
        
        self.signup_url = "/auth/signup/"
        self.login_url = "/auth/login/"
        self.profile_url = "/profile/"
        self.booking_url = "/bookings/"
        self.admin_users_url = "/admin/users/"
        self.admin_booking_count_url = "/admin/booking-count/"
    
    def authenticate(self):
        """Authenticate and get JWT token"""
        response = self.client.post(self.login_url, {"email": "test@example.com", "password": "password123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    
    def test_signup(self):
        """Test user signup"""
        data = {"username": "newuser", "email": "new@example.com", "password": "password123"}
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_login(self):
        data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(self.login_url, data, format="json")
        print("Response Status:", response.status_code)
        print("Response Data:", response.data)  # Check if it gives an error
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_profile_update(self):
        """Test updating user profile"""
        self.authenticate()
        data = {"address": "123 Main St", "gender": "F"}
        response = self.client.post(self.profile_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_booking(self):
        """Test creating a booking"""
        self.authenticate()
        data = {
            "hotel_name": "Grand Hotel",
            "check_in_date": (datetime.today()).date().isoformat(),
            "check_out_date": (datetime.today() + timedelta(days=2)).date().isoformat(),
            "check_in_time": time(14, 0).isoformat(),
            "check_out_time": time(11, 0).isoformat(),
            "num_persons": 2,
            "room_type": "Deluxe Suite",
            "total_price": "500.00"
        }
        response = self.client.post(self.booking_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_user_bookings(self):
        """Test retrieving all bookings for a user"""
        self.authenticate()
        response = self.client.get(self.booking_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_list_users(self):
        """Test admin getting list of users"""
        self.client.login(username="admin", password="admin123")
        response = self.client.get(self.admin_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_booking_count(self):
        """Test admin getting booking count per user"""
        self.client.login(username="admin", password="admin123")
        response = self.client.get(self.admin_booking_count_url, {"start_date": "2025-03-01", "end_date": "2025-03-31"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
