from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from base.models import Profile
from base.forms import ProfileForm


def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        Profile.objects.create(
            user=user
        )

        messages.success(request, "Account created successfully!")

        return redirect("login")

    return render(request, "register.html")

def login_view(request):
    
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout_view(request):
    
    logout(request)

    messages.success(request, "Logged out successfully!")

    return redirect("login")


@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "phone_number": "",
            "address": "",
        }
    )

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )
    
    
@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully!"
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )
    
    
@login_required
def change_password(request):

    if request.method == "POST":

        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if not request.user.check_password(old_password):

            messages.error(
                request,
                "Current password is incorrect."
            )

            return redirect("change_password")

        if new_password != confirm_password:

            messages.error(
                request,
                "New passwords do not match."
            )

            return redirect("change_password")

        if len(new_password) < 8:

            messages.error(
                request,
                "Password must be at least 8 characters."
            )

            return redirect("change_password")

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(
            request,
            request.user
        )

        messages.success(
            request,
            "Password changed successfully!"
        )

        return redirect("profile")

    return render(
        request,
        "change_password.html"
    )
    