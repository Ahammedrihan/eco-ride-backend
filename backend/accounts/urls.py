from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name ="register"),
    path('driver-register/',DriverRegistrationView.as_view(),name ="driver_register"),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/<int:user_id>/',UserProfileView.as_view(),name ="profile"),
    path('reset-password/',UserChangePasswordView.as_view(),name ="reset-password"),
    path('get-users/', UserListView.as_view(), name='users-list'),
    path('user-logout/', LogoutView.as_view(), name='users-list'),
    path('get-drivers/', DriverListView.as_view(), name='drivers-list'),
    path('user-block/<int:user_id>/', UserBlock.as_view(), name='user-block'),
    path('user-address/<int:user_id>/',UserAddAddressView.as_view(), name='user-address'),
    path('add-vehicle/<int:user_id>/',AddVehicleView.as_view(),name = "add-vehicle"),
    path('basic-profile-fetch/<int:user_id>/',UserBasicProfileView.as_view(),name = "basic-profile-fetch"),
    path('basic-profile-add/',UserBasicProfileAdd.as_view()),
    path('address/delete/<int:address_id>/',DeleteAddress.as_view(),name = "address-delete"),
    path("nearby-drivers/<int:user_id>/",FindNearByDriver.as_view()),
    path("user-default-address",UserDefaultAddress.as_view()),
    path("user-travel-distance/",UserFromToDestinationDistanceFinder.as_view()),
    path("trip-amount/",TripAmount.as_view()),
    path("all-trips",UserAllTrips.as_view())
]
