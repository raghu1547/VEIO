from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.admin import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserRegForm
from django.contrib import messages, auth
from django.contrib.auth.admin import User
from .models import UserProfile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from vehicles.tasks import regemail

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        user = request.user
        if(user.userprofile.is_SO):
            return redirect('security_officer')
        return redirect('security')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        rememberme = request.POST.get('rememberMe', None)
        if rememberme != 'on':
            request.session.set_expiry(0)
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Logged in Successfully")
            if(user.userprofile.is_SO):
                return redirect('security_officer')
            return redirect('security')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def regUser(form):
    user = User.objects.create_user(username=form['username'], first_name=form['first_name'],
                                    last_name=form['last_name'], email=form['email'], password=form['password1'])
    user.save()
    userprofile = UserProfile(user=user, phone_no=form['phone_number'])
    userprofile.save()
    regemail(user)


def register(request):
    if request.user.is_authenticated:
        user = request.user
        if(user.userprofile.is_SO):
            return redirect('security_officer')
        return redirect('security')
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            print(form['username'])
            print(form.cleaned_data)
            regUser(form.cleaned_data)
            messages.success(request, "Registration Successful")
            return redirect('login')
        else:
            if form['email'].errors:
                messages.error(request, "A User with the Email already exists")
            else:
                messages.error(request, "Something Went Wrong")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def checkUser(request):
    if request.method == "POST":
        response_data = {}
        loginUser = request.POST["user"]
        user = None
        try:
            try:
                user = User.objects.get(username=loginUser)
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                response_data["is_success"] = True
            else:
                response_data["is_success"] = False
        except Exception as e:
            response_data["is_success"] = False
            response_data["msg"] = "Some error occurred. Please let Admin know."

        return JsonResponse(response_data)
    else:
        return redirect('login')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('login')
