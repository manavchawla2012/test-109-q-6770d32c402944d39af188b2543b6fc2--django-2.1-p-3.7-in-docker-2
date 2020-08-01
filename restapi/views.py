# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
from restapi.models import Driver, DriverLocation
from django.db import IntegrityError


# Create your views here.


def create_driver(request):
    if request.method == "POST":
        required_fields = ["name", "email", "phone_number", "license_number", "car_number"]
        try:
            data = request.body.decode("utf-8")
            if not data:
                return return_json_error("Data Required", 400)
            else:
                data = json.loads(data)
                error = check_required_fields(required_fields, data)
                if error:
                    return return_json_error(error, 400)
                else:
                    new_driver = Driver(**data)
                    new_driver.full_clean()
                    new_driver.save()
                    data["id"] = new_driver.id
                    return JsonResponse(data, status=201)
        except Exception as e:
            return return_json_error(str(e), 400)
    else:
        return return_json_error("Request Method Not Allowed", 400)


def cabs_available(request):
    if request.method == "POST":
        required_fields = ["longitude", "latitude"]
        try:
            data = request.body.decode("utf-8")
            data = json.loads(data)
            error = check_required_fields(required_fields, data)
            if error:
                return return_json_error(error, 400)
            else:
                customer_longitude = float(data["longitude"])
                customer_latitude = float(data["latitude"])
                cabs = DriverLocation.objects.all().values("longitude", "latitude", "driver__name",
                                                           "driver__car_number", "driver__phone_number")
                available_cabs = []
                for cab in cabs:
                    distance = haversine(customer_longitude, customer_latitude, cab["longitude"], cab["latitude"])
                    if distance < 4:
                        cab.pop("longitude")
                        cab.pop("latitude")
                        cab["name"] = cab.pop("driver__name")
                        cab["car_number"] = cab.pop("driver__car_number")
                        cab["phone_number"] = cab.pop("driver__phone_number")
                        available_cabs.append(cab)

                if available_cabs:
                    return JsonResponse({"available_cabs": available_cabs}, status=200)
                else:
                    return JsonResponse({"message": "No cabs available!"}, status=200)

        except Exception as e:
            return return_json_error(str(e), 400)
    else:
        return return_json_error("Request Method Not Allowed", 400)


def store_location(request, driver_id):
    if request.method == "POST":
        required_fields = ["longitude", "latitude"]
        try:
            data = request.body.decode("utf-8")
            data = json.loads(data)
            error = check_required_fields(required_fields, data)
            if error:
                return return_json_error(error, 400)
            else:
                DriverLocation.objects.update_or_create(driver_id=driver_id, defaults=data)
                return JsonResponse({"status": "success"}, status=202)
        except IntegrityError as ie:
            return return_json_error("Driver Id not found", 400)
        except Exception as e:
            return return_json_error(str(e), 400)
    else:
        return return_json_error("Request Method Not Allowed", 400)


def check_required_fields(fields: list, body: dict):
    error = ""
    for field in fields:
        if not body.get(field):
            error = error + f"{field},"
    return error.rstrip(",") + " not found" if error else None


def return_json_error(msg, status):
    return JsonResponse({"status": "failure", "reason": msg}, status=status)


def haversine(lon1: float, lat1: float, lon2: float, lat2: float):
    from math import radians, cos, sin, asin, sqrt
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r
