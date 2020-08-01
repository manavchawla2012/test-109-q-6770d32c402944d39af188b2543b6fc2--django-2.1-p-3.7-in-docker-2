from django.urls import path
from restapi.views import *


urlpatterns = [
    path("driver/register/", create_driver),
    path("driver/<int:driver_id>/sendLocation/", store_location),
    path("passenger/available_cabs/", cabs_available)
]