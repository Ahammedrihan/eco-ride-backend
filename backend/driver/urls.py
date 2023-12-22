from django.urls import path
from .views import DriverProfileView,DriverManageVehicle,DriverActiveLocationView,DriverManageAddress,DriverDefaultAddressView
from .views import ActiveDriverView,DriverAllTrips,DriverTripData,DriverSideTripStatusButton,FinishRide ,DriverProfileAllTripsView
urlpatterns = [
    path("driver/profile/<int:driver_id>/",DriverProfileView.as_view(),name="driver-profile"),
    path("driver/profile/vehicle-delete/<int:vehicle_id>/",DriverManageVehicle.as_view(),name="driver-delete"),
    path("driver/profile/set-default/<int:vehicle_id>/<int:driver_id>/",DriverManageVehicle.as_view(),name="driver-delete"),
    path("driver/profile/set-default-address/<int:address_id>/",DriverManageAddress.as_view(),name="driver-set-location"),
    path("driver/location-set-activate/",DriverActiveLocationView.as_view(),name="driver-set-location"),
    path("driver/default-address/<int:driver_id>/",DriverDefaultAddressView.as_view(),name = "driver-active-location"),
    path("driver/set-active-drivers/",ActiveDriverView.as_view()),
    path("driver/active-trip-details/<int:driver_id>/",DriverAllTrips.as_view()),
    path("driver/trip-data/",DriverTripData.as_view()),
    path("driver/trip-status-button/",DriverSideTripStatusButton.as_view()),
    path("driver/finish-trip/",FinishRide.as_view()),
    path("driver/all-trips/",DriverProfileAllTripsView.as_view()),
    

]

