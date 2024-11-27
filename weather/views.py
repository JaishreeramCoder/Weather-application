# Create your views here.
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from .models import Profile
admin.site.register(Profile)


@login_required
def weather_home(request):
    weather_data = None
    forecast_data = None
    error_message = None

    if request.method == "POST":
        city = request.POST.get("city")

        # Save city to user's profile
        profile = request.user.profile
        profile.last_city = city
        profile.save()

    else:
        # Use last searched city if no city is entered
        city = request.user.profile.last_city

    if city:
        api_key = "18794c0d5c634a64610676ca7aafd8d0"
        base_url = "https://api.openweathermap.org/data/2.5/forecast"

        try:
            response = requests.get(
                base_url, params={"q": city, "appid": api_key, "units": "metric"}
            )
            response.raise_for_status()
            weather_data = response.json()

            # # Current weather
            # weather_data = {
            #     "city": data["city"]["name"],
            #     "country": data["city"]["country"],
            #     "temperature": data["list"][0]["main"]["temp"],
            #     "description": data["list"][0]["weather"][0]["description"],
            #     "icon": data["list"][0]["weather"][0]["icon"],
            #     "coord": data["city"]["coord"],
            # }

            # 5-day forecast
            forecast_data = []
            for forecast in weather_data["list"]:
                forecast_data.append(
                    {
                        "datetime": forecast["dt_txt"],
                        "temperature": forecast["main"]["temp"],
                        "description": forecast["weather"][0]["description"],
                        "icon": forecast["weather"][0]["icon"],
                    }
                )

        except requests.exceptions.RequestException as e:
            error_message = f"Could not retrieve weather data: {e}"

    return render(
        request,
        "weather/weather_home.html",
        {
            "weather_data": weather_data,
            "forecast_data": forecast_data,
            "error_message": error_message,
            "last_city": city,
        },
    )

# def signup(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("weather_home")
#     else:
#         form = UserCreationForm()
#     return render(request, "weather/signup.html", {"form": form})

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
import random
import string

# Temporary storage for OTP (can be stored in session or database)
otp_dict = {}


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data['username']  # Added username
            password = form.cleaned_data['password']  # Added password
            # Step 1: Generate and send OTP
            otp = form.generate_otp()
            otp_dict[email] = (
                otp  # Store OTP temporarily (consider using session or database)
            )
            form.send_otp_email(email, otp)

            # Step 2: Prompt user to enter OTP
            return render(
                request,
                "registration/verify_otp.html",
                {
                    "form": form,
                    "email": email,
                    "username": username,
                    "password": password,
                },
            )

        else:
            return render(request, "registration/signup.html", {"form": form})

    else:
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})


def verify_otp(request):
    email = request.POST.get('email')
    otp = request.POST.get('otp')
    username = request.POST.get('username')  # Retrieve username
    password = request.POST.get('password')
    print(email,password,username)
    # Step 3: Verify OTP
    if otp == otp_dict.get(email):
        # OTP is correct, create user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Account created successfully! Please login.")
        del otp_dict[email]
        return redirect("login")

    else:
        return redirect("signup")



def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("weather_home")
    return render(request, "weather/login.html")


# forgot password
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
import random

otp_storage_pwd_reset = {}


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            otp_storage_pwd_reset[email] = otp
            subject = "Password Reset OTP"
            message = (
                f"Hello {user.username},\n\n"
                f"Your OTP for password reset is {otp}.\n"
                "If you did not request this, please ignore this email."
            ) 
            send_mail(subject, message, "sharmaadarsh345678@gmail.com", [email])
            messages.success(request, "OTP sent to your email.")
            request.session["email"] = email
            return redirect("verify_otp_password")
        except User.DoesNotExist:
            messages.error(request, "No user found with that email.")
    return render(request, "registration/forgot_password.html")


def verify_otp_password(request):
    if request.method == "POST":
        email = request.session.get("email")
        otp = int(request.POST.get("otp"))
        if email in otp_storage_pwd_reset and otp_storage_pwd_reset[email] == otp:
            del otp_storage_pwd_reset[email]
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP.")
    return render(request, "registration/verify_otp_password.html")


def reset_password(request):
    if request.method == "POST":
        email = request.session.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save() 
                messages.success(request, "Password reset successful. Please login.")
                return redirect("login")
            except User.DoesNotExist:
                messages.error(request, "No user found with that email.")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "registration/reset_password.html")
