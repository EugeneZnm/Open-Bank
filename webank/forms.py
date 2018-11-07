import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget

# import user model
from .models import User
from .models import Deposit, Withdrawal

class UserRegistrationForm(UserCreationForm):
    born = forms.DateField(
        widget=SelectDateWidget()
    )

    class Meta:
        model = User
        fields = ["full_name",
                  "gender",
                  "born",
                  "email,"
                  "phone",
                  "city",
                  "nationality",
                  "account_type",
                  "picture",
                  "password1",
                  "password2"
                  ]

    def save(self, commit = True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.born = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    form for allowing user login
    """
    def clean(self, *args, **kwargs):
        account_no = self.cleaned_data.get("account_no")
        password = self.cleaned_data.get("password")

        if account_no and password:
            user_obj = User.objects.filter(account_no=account_no.first)
            if user_obj:
                user = authenticate(email=user_obj.email, password=password)
                if not user:
                    raise forms.ValidationError("This Account Does Not Exist, Check if your Input is Correct")
                if not user.check_password(password):
                    raise forms.ValidationError("Password Does Not Match")
                if not user.is_active:
                    raise forms.ValidationError("Account is Inactive")
            else:
                raise forms.ValidationError("This Account Doesn't Exist.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class DepositForm(forms.ModelForm):
    """
    form for depositing cash
    """
    class Meta:
        model = Deposit
        fields = ["amount"]

class WithdrawalForm(forms.ModelForm):
    """ form for withdrawing cash"""

    class Meta:
        model =Withdrawal
        fields = ["amount"]