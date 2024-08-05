from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.db import IntegrityError
from .models import Profile

def sign_up (request: HttpRequest):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "A user with that username already exists.", "alert-danger")
            return render(request, "signUp.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists.", "alert-danger")
            return render(request, "signUp.html") 
        
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username = request.POST["username"], password=request.POST["password"], email=request.POST["email"],first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()
            messages.success(request, "You have been Registered Successfully", "alert-success")
            #send confirmation email
            content_html = render_to_string("mail/welcoming.html",{"userName":new_user}) #set email
            send_to = new_user.email
            email_message = EmailMessage("welcoming", content_html, settings.EMAIL_HOST_USER, [send_to])
            email_message.content_subtype = "html"
            #email_message.connection = email_message.get_connection(True)
            email_message.send()
            return redirect("account:sign_in")
        except IntegrityError:
            messages.error(request, "An error occurred during registration.", "alert-danger")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}", "alert-danger")
    return render(request, "signUp.html")



def sign_in(request: HttpRequest):
        
    if request.method == "POST":
   #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            #login the user
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")
    return render(request, 'signIn.html')


def log_out(request:HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))


def profile_view(request:HttpRequest, user_name):
        
    try:
        user = User.objects.get(username=user_name)
        profile= Profile.objects.get(username=user_name)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()
        #profile:Profile = user.profile  
        #profile = Profile.objects.get(user=user)
    except Exception as e:
        print(e)
        # return render(request,'404.html')
    
    return render(request,"profile.html",{"user":user, "profile":profile})