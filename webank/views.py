
# from django.contrib import messages
# from django.contrib.auth import (authenticate, login, logout)
# from django.contrib.auth.decorators import login_required
# from django.http import Http404
# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import UserLoginForm, UserRegistrationForm, DepositForm,WithdrawalForm
# # models import

from django.db.models import Sum
from .models import User
from .models import Deposit
from .models import Withdrawal
# Create your views here.

from django.contrib import messages
from django.contrib.auth import (authenticate,login,logout)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegistrationForm,DepositForm,WithdrawalForm
from .models import User,Deposit,Withdrawal


def register_view(request):  # Creates a New Account & login New users
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create a Bank Account"
        form = UserRegistrationForm(
            request.POST or None,
            request.FILES or None
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
                '''Thank You For Creating A Bank Account {}.
                Your Account Number is {}, Please use this number to login
                '''.format(new_user.full_name, new_user.account_no))

            return redirect("home")

        context = {"title": title, "form": form}

        return render(request, "start.html", context)

# user login
def login_view(request):  # users will login with their Email & Password
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Load Account Details"
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            account_no = form.cleaned_data.get("account_no")
            user_obj = User.objects.filter(account_no=account_no).first()
            password = form.cleaned_data.get("password")
            # authenticates Email & Password
            user = authenticate(email=user_obj.email, password=password)
            login(request, user)
            messages.success(request, 'Welcome, {}!' .format(user.full_name))
            return redirect("home")

        context = {"form": form,
                   "title": title }

        return render(request, "start.html", context)

def logout_view(request):  # logs out the logged in users
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("home")


# home page
def home(request):
    if not request.user.is_authenticated:
        return render(request, "home.html", {})
    else:
        user = request.user
        deposit = Deposit.objects.filter(user=user)
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
def deposit_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Deposit"
        form = DepositForm(request.POST or None)

        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            # adds users deposit to balance.
            deposit.user.balance += deposit.amount
            deposit.user.save()
            deposit.save()
            messages.success(request, 'You Have Deposited {} $.'
                             .format(deposit.amount))
            return redirect("home")

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "deposit.html", context)



@login_required()
def withdrawal_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Withdraw"
        form = WithdrawalForm(request.POST or None)

        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            # checks if user is tring Withdraw more than his balance.
            if withdrawal.user.balance >= withdrawal.amount:
                # substracts users withdrawal from balance
                withdrawal.user.balance -= withdrawal.amount
                withdrawal.user.save()
                withdrawal.save()
                messages.error(request, 'You Have Withdrawn {} $.'
                               .format(withdrawal.amount))
                return redirect("home")

            else:
                messages.error(
                    request,
                    'You Can Not Withdraw More Than You Balance.'
                    )

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "withdraw.html", context)

