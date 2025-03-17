from rest_framework import serializers
from .models import *

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['address', 'gender', 'photo']

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"  # Ensure all fields are included
        read_only_fields = ["user", "status", "created_at"]
