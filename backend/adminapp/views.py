from django.shortcuts import render
from  rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import *
from .serializers import *
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta ,date




class AdminHomeActiveTripsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request):
        try:
            active_trips = Trip.objects.all()
            serializer = AdminHomeActiveTripSerializer(active_trips,many = True)

            return Response({"message":"Admin fetch all trip data success","data":serializer.data},status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Admin side No active trips to fetch"},status=status.HTTP_204_NO_CONTENT)
        
class AdminHomePageDataView(APIView):

    def get(self,request):
        try:
            number_of_drivers = CustomUser.objects.filter(role = "driver").count()
            number_of_drivers_active = CustomUser.objects.filter(role = "driver",is_active = True).count()
            number_of_drivers_blocked = CustomUser.objects.filter(role = "driver",is_active = False).count()
            
            number_of_users = CustomUser.objects.filter(role = "user").count()
            number_of_users_active = CustomUser.objects.filter(role = "user",is_active = True).count()
            number_of_users_blocked = CustomUser.objects.filter(role = "user",is_active = False).count()
            
            number_of_vehicles = VehicleInfo.objects.all().count()
            number_of_default_vehicles = VehicleInfo.objects.filter(default = True).count()
            number_of_non_activevehicles = VehicleInfo.objects.filter(default = False).count()

            number_of_finished_trips = FinishedTrips.objects.all().count()
            number_of_finished_pay_online = FinishedTrips.objects.filter(payment_method = "payafter").count()
            number_of_finished_payafter = FinishedTrips.objects.filter(payment_method = "online").count()

            today_date = datetime.now().date()
            today_trips = FinishedTrips.objects.filter(created_at__date = today_date ).count()

            yesterday_date = today_date - timedelta(days=1)
            yesterday_trips = FinishedTrips.objects.filter(created_at__date=yesterday_date).count()

            online_pay_count =  FinishedTrips.objects.filter(payment_method = "online").count()
            pay_after_count = FinishedTrips.objects.filter(payment_method = "payafter").count()



  
            data = {
                "number_of_drivers":number_of_drivers,
                "number_of_drivers_active":number_of_drivers_active,
                "number_of_drivers_blocked":number_of_drivers_blocked,
                "number_of_users":number_of_users,
                "number_of_users_active":number_of_users_active,
                "number_of_users_blocked":number_of_users_blocked,
                "number_of_vehicles":number_of_vehicles,
                "number_of_default_vehicles":number_of_default_vehicles,
                "number_of_non_activevehicles":number_of_non_activevehicles,
                "number_of_finished_trips":number_of_finished_trips,
                "number_of_finished_pay_online":number_of_finished_pay_online,
                "number_of_finished_payafter":number_of_finished_payafter,
                "today_trips":today_trips,
                "yesterday_trips":yesterday_trips,
                "online_pay_count":online_pay_count,
                "pay_after_count":pay_after_count

            }
            return Response({"message":"data fetched ","data":data},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)  # Handle  exception or log it
            return Response({"message": f"not able to fetch data, {str(e)}"}, status=status.HTTP_204_NO_CONTENT)
            



class AdminAllVehicleListView(APIView):
    def get(self,request):
        try:
            all_vehicle = VehicleInfo.objects.all()
            count = all_vehicle.count()
            print(all_vehicle)
            serializers = AdminAllVehicleListSerializer(all_vehicle,many=True)
            print(serializers.data)
            return Response ({"message":"got all vehicle","data":serializers.data,"count":count},status=status.HTTP_200_OK)
        except:
            return Response({"message":"not able to fetch vehicles"},status=status.HTTP_204_NO_CONTENT)


