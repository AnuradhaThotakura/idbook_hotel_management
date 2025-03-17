from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from .views import  *
urlpatterns = [
    path('', include(router.urls)),
    path("login/", login_user, name="login"),
    path("profile/", user_profile, name="user_profile"),
    path("bookings/", create_booking, name="create_booking"),  # Create booking
    path("bookings/all/", get_bookings, name="get_bookings"),  # Get all bookings
    path("bookings/<int:booking_id>/", get_booking_by_id, name="get_booking_by_id"),  # Get single booking
    path("bookings/date-range/", get_bookings_by_date_range, name="get_bookings_by_date_range"),  
    path("admin/users/", list_users, name="list_users"),
    path("admin/user-booking-count/", user_booking_count, name="user_booking_count"),


]
