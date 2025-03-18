from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import *
from .serializers import *
from datetime import datetime
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to log in

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request):
        """Retrieve or create a customer profile for the authenticated user"""
        profile, created = CustomerProfile.objects.get_or_create(user=request.user)
        serializer = CustomerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Update the customer profile"""
        profile, created = CustomerProfile.objects.get_or_create(user=request.user)
        serializer = CustomerProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can create bookings

    def post(self, request):
        """Create a new hotel booking"""
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBookingsView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access their bookings

    def get(self, request):
        """Retrieve all bookings for the authenticated user"""
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetBookingByIdView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access their bookings

    def get(self, request, booking_id):
        """Retrieve a single booking by booking ID"""
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

class GetBookingsByDateRangeView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request):
        """Retrieve bookings within a date range (based on check-in date)"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {"error": "Please provide both start_date and end_date in YYYY-MM-DD format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(user=request.user, check_in_date__range=[start_date, end_date])
        serializer = BookingSerializer(bookings, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListUsersView(APIView):
    permission_classes = [IsAdminUser]  # Only Admins can access

    def get(self, request):
        """Retrieve all registered users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserBookingCountView(APIView):
    permission_classes = [IsAdminUser]  # Only Admins can access

    def get(self, request):
        """Get total bookings per user within a date range (based on check-in date)"""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Please provide both start_date and end_date in YYYY-MM-DD format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Aggregate total bookings per user
        booking_counts = (
            Booking.objects.filter(check_in_date__range=[start_date, end_date])
            .values("user__id", "user__username")
            .annotate(total_bookings=Count("id"))
        )

        return Response(booking_counts, status=status.HTTP_200_OK)
