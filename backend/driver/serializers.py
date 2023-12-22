from rest_framework import serializers
from accounts.models import CustomUser,AccountInfo,VehicleInfo,Trip,ActiveDrivers,FinishedTrips,Profile




# <======================DRIVER PROFILE VIEW SERIALIZER=======================>


class DriverProfileAccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = "__all__"

class DriverProfileVehicleInfo(serializers.ModelSerializer):
    class Meta:
        model = VehicleInfo
        fields = "__all__"

class DriverProfileSerializer(serializers.ModelSerializer):

    vehicle_info = DriverProfileVehicleInfo(read_only=True, many=True)
    account_info = DriverProfileAccountInfoSerializer(read_only=True, many=True)
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "phone", "last_name", "is_active", "date_joined",  "vehicle_info", "account_info"]


# serilizer meythod field, related 


# <======================DRIVER PROFILE VIEW SERIALIZER END=======================>



class DeleteDriverSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    class Meta:
        model = VehicleInfo
        fields = "__all__"

class DriverActiveLocationSerializer(serializers.ModelSerializer):
    active_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = ActiveDrivers
        fields = ['user', 'active_vehicle', 'existing_address', 'latitude', 'longitude', 'active_time']
        




# <======================NEAR BY DRIVER VIEW SERIALIZER END=======================>



class NearByDriverAccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = '__all__'

class NearByDriverVehicleInfo(serializers.ModelSerializer):
    class Meta:
        model = VehicleInfo
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender', 'dob', 'age', 'alternate_phone', 'profile_image']


class DriverProfileSerializer(serializers.ModelSerializer):
    account_info = serializers.SerializerMethodField()

    def get_account_info(self, obj):
        account_info_instances = obj.account_info.all()
        return NearByDriverAccountInfoSerializer(account_info_instances, many=True).data
    profile_info = serializers.SerializerMethodField()

    def get_profile_info(self, obj):
        try:
            # Attempt to retrieve the associated Profile instance
            profile_instance = obj.profile_info.get()
            return ProfileSerializer(profile_instance).data
        except Profile.DoesNotExist:
            # Handle the case where no Profile instance is found
            return None


    vehicle_info = NearByDriverVehicleInfo(read_only=True, many=True)
    class Meta:
        model = CustomUser
        fields = ['id','email','first_name','phone','last_name', "vehicle_info", "account_info","profile_info"]


# class NearByDriverSerializer(serializers.Serializer):


 


class DriverBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "phone", "last_name", "is_active", "date_joined"]
    

 
#-------------------------

class DriverAllTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class FinishedTripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedTrips
        fields = "__all__"

        

    
