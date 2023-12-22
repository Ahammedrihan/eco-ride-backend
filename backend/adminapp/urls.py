from django.urls import path
from .views import *

urlpatterns = [
    path('home/active-trips',AdminHomeActiveTripsView.as_view()),
    path('home/data',AdminHomePageDataView.as_view()),
    path('home/all-vehicles/',AdminAllVehicleListView.as_view())
  
]
