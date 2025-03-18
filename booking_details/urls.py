from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from .views import  *
urlpatterns = [
    path('', include(router.urls)),
    path("login/", LoginView.as_view(), name="login"), 
    path("profile/", UserProfileView.as_view(), name="user_profile"),  # Use .as_view() for CBVs
    path("bookings/", CreateBookingView.as_view(), name="create_booking"),  # Use .as_view() for CBVs# Create booking
    path("bookings/all/", GetBookingsView.as_view(), name="get_bookings"),  # Use .as_view() for CBVs
    path("bookings/<int:booking_id>/", GetBookingByIdView.as_view(), name="get_booking_by_id"),  # Use .as_view() for CBVs
    path("bookings/date-range/", GetBookingsByDateRangeView.as_view(), name="get_bookings_by_date_range"),
    path("admin/users/", ListUsersView.as_view(), name="list_users"),
    path("admin/user-booking-count/", UserBookingCountView.as_view(), name="user_booking_count"),


]
