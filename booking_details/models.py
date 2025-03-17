from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    STATUS_CHOICES = [("confirmed", "Confirmed"), ("canceled", "Canceled")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    hotel_name = models.CharField(max_length=255)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    num_persons = models.IntegerField()
    room_type = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
