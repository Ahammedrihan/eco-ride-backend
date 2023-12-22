from rest_framework import serializers
from accounts.models import * 




class AdminHomeActiveTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"

class AdminAllVehicleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleInfo
        fields = "__all__"