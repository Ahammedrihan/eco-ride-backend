from accounts.models import Trip
from rest_framework import serializers

class BookTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'