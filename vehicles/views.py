from django.shortcuts import render, redirect
from django.contrib.auth.admin import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import Regveh, Gesveh, Flow
from datetime import datetime, timedelta
# Create your views here.


def checkReg(request):
    if request.method == "POST":
        # print("krishna")
        response_data = {}
        entry = request.POST["entry"]
        entry = entry.strip().upper()
        vn = None
        try:
            if Flow.objects.filter(vn=entry, timeout__isnull=True).exists():
                response_data["is_success"] = False
                response_data["FlowError"] = True
                response_data["message"] = "Vehicle Exit data is not entered"
            else:
                vn = Regveh.objects.filter(vn=entry)
            # print("krish")
                if not vn:
                    vn = Gesveh.objects.filter(
                        vn=entry).order_by('-firstentry').first()
                    if vn:
                        if vn.firstentry+timedelta(days=vn.nod) <= datetime.now():
                            response_data["is_success"] = False
                        else:
                            response_data["is_success"] = True
                            response_data["message"] = "Vehicle Permission is already granted"
                    else:
                        response_data["is_success"] = False
                else:
                    response_data["is_success"] = True
                    response_data["message"] = "Registered Vehicle"
        except Exception as e:
            response_data["is_success"] = False
            response_data["message"] = "Some error occurred. Please let Admin know."

        return JsonResponse(response_data)
    return redirect('login')
