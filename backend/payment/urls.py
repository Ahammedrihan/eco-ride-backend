from django.urls import path
from .views import RazorpayOrderView,ConfirmTrip,VerifyOnTripBeforeRide

urlpatterns = [
    path('verify-ontrip/',VerifyOnTripBeforeRide.as_view()),
    path('create-razopay-order/',RazorpayOrderView.as_view()),
    path('confirm-trip/',ConfirmTrip.as_view()),

    
]
