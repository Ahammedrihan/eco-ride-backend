from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from accounts.models import CustomUser ,VehicleInfo,ActiveDrivers,AccountInfo,Trip,FinishedTrips
from .serializers import DriverProfileSerializer,DeleteDriverSerializer,DriverActiveLocationSerializer,DriverProfileAccountInfoSerializer
from .serializers import DriverActiveLocationSerializer ,DriverAllTripSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.utils import timezone
from accounts.serializers import UserSerializer
from driver.serializers import FinishedTripsSerializer


class DriverProfileView(APIView):
    permission_classes  = [IsAuthenticated]

    def get(self,request,driver_id):
        try:
            driver = CustomUser.objects.get(id = driver_id)
            serializer = DriverProfileSerializer(driver)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)



class DriverManageVehicle(APIView):
    permission_classes  = [IsAuthenticated]

    def post(self,request,vehicle_id):
        try:
            print(vehicle_id)
            print(request)
            vehicle = VehicleInfo.objects.get(id = vehicle_id)
            vehicle.delete()
            return Response({"message":"vehicle deleted succesfully"},status=status.HTTP_204_NO_CONTENT)
        except VehicleInfo.DoesNotExist:
            return Response ({"error":"vehicle Not Found"},status=status.HTTP_404_NOT_FOUND)
    

    def patch(self,request,vehicle_id,driver_id):
        try:
            vehicle = VehicleInfo.objects.get(id = vehicle_id)
            other_vehicles = VehicleInfo.objects.filter(user_id = driver_id).exclude(id = vehicle_id).update(default = False)
            if vehicle :
                vehicle.default = True
                vehicle.save()
                return Response({"msg":" Set default Success"},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error":"Vehicle not found for the specified driver and ID"},status=status.HTTP_404_NOT_FOUND)
        except VehicleInfo.DoesNotExist:
            return Response ({"error":"vehicle Not Found"},status=status.HTTP_404_NOT_FOUND)



class DriverManageAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,address_id):
        try:
            address = AccountInfo.objects.get(id = address_id)
            address.delete()
            return Response({"message":"Address deleteion Sucess"},status=status.HTTP_200_OK)
        except AccountInfo.DoesNotExist:
            return Response({"message":"Address Not Found"},status=status.HTTP_404_NOT_FOUND)
        
    def patch(self,request,address_id):
        driver_id = request.user.id
        try:
            address = AccountInfo.objects.get(id = address_id)
            AccountInfo.objects.filter(user_id= driver_id).exclude(id = address_id).update(default = False)
            if address:
                address.default = True
                address.save()
                return Response({"message":" Address Set Default Success"},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"Address Not Found"},status=status.HTTP_404_NOT_FOUND)
        except AccountInfo.DoesNotExist:
             return Response({"message":"Address Not Found"},status=status.HTTP_404_NOT_FOUND)



class DriverActiveLocationView(APIView):
    permission_classes =[IsAuthenticated]

    def post(self,request):
        print(request.data)
        serializer = DriverActiveLocationSerializer(data = request.data)
        if serializer.is_valid():

           return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)



class DriverDefaultAddressView(APIView):
    permission_classes =[IsAuthenticated]
        
    def get(self,request,driver_id):
        try:
            driver = CustomUser.objects.get(id = driver_id)
            try:
                default_driver_address = AccountInfo.objects.get(user_id = driver,default = True)
                serializer = DriverProfileAccountInfoSerializer(default_driver_address)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except AccountInfo.DoesNotExist:
                return Response({"message":"You don't have any active  address"},status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"message":"Driver Not Found"},status=status.HTTP_404_NOT_FOUND)

        

class ActiveDriverView(APIView):
    permission_classes = [IsAuthenticated]
    def post (self,request):

        driver_present = ActiveDrivers.objects.filter(user_id =request.user.id )
        if driver_present:
            return Response({"message":"Driver Already active"},status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                user_id = request.user.id
                active_vehicle = VehicleInfo.objects.get(user = user_id,default = True)
                try:
                    driver_default_address = AccountInfo.objects.get(user = user_id,default = True)
                except:
                    pass
                data = { 
                    "user":user_id,
                    "active_vehicle" : active_vehicle.id,
                    "latitude": request.data.get("latitude"),
                    "longitude": request.data.get("longitude"),
                }
                data["active_time"] = timezone.now()
                if data["latitude"] and data["longitude"]:
                    data["existing_address"] = None
                else:
                    data["existing_address"] = driver_default_address.id
                serializer = DriverActiveLocationSerializer(data = data)
                if serializer.is_valid():
                    
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except VehicleInfo.DoesNotExist:
                return Response({"message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Unexpected error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        driver_id = request.user.id
        active_driver_instance = ActiveDrivers.objects.get(user_id = driver_id)
        active_driver_instance.delete()
        return Response({"message":"deletion sucess"},status=status.HTTP_200_OK)
    
    def get(self,request):
        driver_id = request.user.id
        try:
            driver_active = ActiveDrivers.objects.get(user_id =driver_id )
            if driver_active:
                return Response({"message":"Driver Found on Active drivers table"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"Driver Not present in Active drivers table"},status=status.HTTP_226_IM_USED)



class DriverAllTrips(ListAPIView):
    serializer_class = DriverAllTripSerializer

    def get(self,driver_id):
        driver_trips = Trip.objects.filter(driver_id = driver_id)
        return driver_trips



class DriverTripData(APIView):
    def get(self,request):
        driver_id = request.user.id
        try:
            active_trip = Trip.objects.get(driver_id = driver_id)
            user_id = active_trip.user_id
            user_details = CustomUser.objects.get(id = user_id)
            user_name = user_details.first_name +" "+ user_details.last_name
            user_phone = user_details.phone
            user_email = user_details.email
            serializer = DriverAllTripSerializer(active_trip)
            data = {
                'trip' : serializer.data,
                'user_name': user_name,
                'user_phone':user_phone,
                'user_email':user_email

            }
            return Response({"message":"Driver is assigned for trip","data":data},status=status.HTTP_200_OK)
        except:
            return Response({"message":"No active Trips for driver"},status=status.HTTP_204_NO_CONTENT)
        


class DriverSideTripStatusButton(APIView):
    def get(self,request):
        driver_id = request.user.id
        try:
            active_trip = Trip.objects.get(driver_id = driver_id)
            try:
                if active_trip.trip_status == "pending":
                    active_trip.trip_status = "accepted"
                    active_trip.save()
                elif active_trip.trip_status == "accepted":
                    active_trip.trip_status = "started"
                    active_trip.save()
                elif active_trip.trip_status == "started":
                    active_trip.trip_status = "finished"
                    active_trip.save()
                return Response({"message":"status update succesfull"},status=status.HTTP_201_CREATED)
            except:
                return Response({"message":"status update failed"},status=status.HTTP_304_NOT_MODIFIED)
        except:
            return Response({"message":"No such active tips found"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        


class FinishRide(APIView):
    def post(self,request):
        driver_id = request.user.id
        try:
            active_trip = Trip.objects.get(driver_id = driver_id)
            try:
                if active_trip.trip_status == "finished":
                    active_trip.payment_status = True
                    active_trip.save()
                    try:
                        serializer = FinishedTripsSerializer(data = {
                            'user' : active_trip.user.pk,
                            'driver' :active_trip.driver.pk,
                            'vehicle':active_trip.vehicle.pk,
                            'start_lat':active_trip.start_lat,
                            'start_long':active_trip.start_long,
                            'end_lat':active_trip.end_lat,
                            'end_long':active_trip.end_long,
                            'start_location_name':active_trip.start_location_name,
                            'end_location_name':active_trip.end_location_name,
                            'created_at':active_trip.created_at,
                            'amount':active_trip.amount,
                            'payment_method':active_trip.payment_method,
                            'razorpay_order_id':active_trip.razorpay_order_id,
                            'razorpay_payment_id':active_trip.razorpay_payment_id,
                            'total_distance':active_trip.total_distance,
                            'payment_status':active_trip.payment_status,
                            'Trip_end_time':timezone.now()
                        } )
                        print(serializer.is_valid())
                        if serializer.is_valid():
                            serializer.save()
                            active_trip.delete()
                            return Response({"message":"data added to finished trip table","data":serializer.data},status=status.HTTP_200_OK)
                        else:
                            print(serializer.errors,"!!!!!!!!!!!!!!")
                            return Response({"message": "Trip status is not finished or payment status is already True","error":serializer.errors}, status=status.HTTP_304_NOT_MODIFIED)
                    except:
                        return Response({"message":"Data not able to interchange"},status=status.HTTP_400_BAD_REQUEST)

            except:
                return Response({"message":"trip status is not finished"},status=status.HTTP_304_NOT_MODIFIED)
        except:
            return Response({"message":"No such active tips found"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    
    
class DriverProfileAllTripsView(APIView):
  
    def get(self,request):
        driver_id = request.user.id 
        try:
            driver_trips = FinishedTrips.objects.filter(driver_id = driver_id)
            serializer = FinishedTripsSerializer(driver_trips, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"message":"Driver has no trip details"},status=status.HTTP_204_NO_CONTENT)











