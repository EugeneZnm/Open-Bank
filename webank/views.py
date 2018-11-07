from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserResgitrationForm
from .models import User
# Create your views here.


def register_view(request):
    """
    Account creation and new user login
    """
    if request.user.is_authenticated:
        return redirect("Home")
    else:
        title = "Create your Bank Account"
        form = UserResgitrationForm(
            request.POST or None,
            request.FILES or None,
        )

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        user.save()
        new_user = authenticate(email=user.email, password=password)
        login(request, new_user)
        messages.success(
            request,
            """
            Welcome To We Bank {},
            Your Account Number is {}. Use Your account Number to login
            """.format(new_user.full_name, new_user.account_no)
        )
        return redirect("Home")

    context = {"title": title, "form":form}

    return render(request, "start.html", context)


# user login
def login_view(request):
    """ user login with email and password """
    if request.user.is_authenticated:
        return redirect("Home")
    else:
        title = "Load Account Details"
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            account_no = form.cleaned_data.get("account_no")
            user_obj = User.objects.filter(account_no=account_no).first()
            password = form.cleaned_data.get("password")

            # Email and password validation
            user = authenticate(email=user_obj.email, password=password)
            login(request, user)
            messages.success(request, "Welcome, to Your Account {}!!".format(user.full_name))
            return redirect("Home")
        context = {"form":form, "title": title}

        return render(request, "start.html", context)


# user logout
def logout_view(request):
    """
    user logout function """
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("Home")
