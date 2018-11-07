from django.shortcuts import render
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, DepositForm,WithdrawalForm
# models import
from .models import User
from .models import Deposit
from .models import Withdrawal
# Create your views here.


def register_view(request):
    """
    Account creation and new user login
    """
    if request.user.is_authenticated:
        return redirect("Home")
    else:
        title = "Create your Bank Account"
        form = UserRegistrationForm(
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
        return redirect("home")

    context = {"title": title, "form":form}

    return render(request, "start.html", context)


# user login
def login_view(request):
    """ user login with email and password """
    if request.user.is_authenticated:
        return redirect("home")
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
        return redirect("home")


# home page
def Home(request):
    if not request.user.is_authenticated:
        return render(request, "home.html")
    else:
        user = request.user
        deposit =Deposit.objects.filter(user=user)
        deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']
        withdrawal = Withdrawal.objects.filter(user=user)
        withdrawal_sum = withdrawal.aggregate(Sum('amount'))['amount__sum']

        context = {
            "user": user,
            "deposit": deposit,
            "deposit_sum": deposit_sum,
            "withdrawal": withdrawal,
            "withdrawal_sum": withdrawal_sum,
        }

        return render(request, "transactions.html", context)

# transactions
@login_required()
def deposit(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Deposit"
        form =DepositForm(request.POST or None)

        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user =request.user
            deposit.user.save()
            deposit.save()
            messages.success(request, "Successful deposit of Kshs {}.".format(deposit.amount))
            return redirect("home")

        context = {
            "title": title,
            "form": form
            }
        return render(request, "transactions.html", context)


@login_required()
def widthdraw(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "WIthdraw"
        form = WithdrawalForm(request.POST or None)

        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            # checking if amount is more than available balance
            if withdrawal.user.balance >= withdrawal.amount:
                # deduction of withdrawal amount from balance
               withdrawal.user.balance -=withdrawal.amount
               withdrawal.user.save()
               withdrawal.save()
               messages.error(request, 'Amount withdrawn is Kshs {}.'.format(withdrawal.amount))
               return redirect("home")
            else:
                messages.error(
                    request,
                    'Withdrawal Amount Exceedes Available Balance'
                )
        context = {
             "title": title,
             "form": form
            }

        return render(request, 'transactions.html', context)
