from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.core.validators import ( RegexValidator, MinValueValidator, MaxValueValidator )
# from .managers import UserManager
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver

from decimal import Decimal
from django.conf import settings

# Accounts models here.


# name validator
Name_Regex = '^[a-zA-Z ]*S'

# determining user gender types
GENDER_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("None", "None"),
)

# user account type choice
Account_Choice = (
    ("Current Account", "Current Account"),
    ("Savings Account", "Savings Account"),
)

# User_Type = (
#     ("Business", "Business"),
#     ("Individual", "")
# )


class User(AbstractBaseUser):
    """
    user details including name and account details
    """
    username = None
    first_name = None
    last_name = None

    # user account details
    account_no = models.PositiveIntegerField(
        #validating minimum and maximum values of account numbers
        unique=True,
        validators = [
            MinValueValidator(1000000),
            MaxValueValidator(999999999999),
        ]
    )

    # validating user name, restricted to alphabets
    full_name = models.CharField(

        max_length=300,
        blank=False,
        validators = [
            RegexValidator(
                regex= Name_Regex,
                message='User Name must be Alphabetic',
                code = 'invalid full name'
            )
        ]
    )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICE)
    born = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    phone = models.IntegerField(unique=True)
    city = models.CharField(max_length=256)
    nationality = models.CharField(max_length=300)
    account_type = models.CharField(max_length=14, choices=Account_Choice)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    picture = models.ImageField(
        null=True,
        blank=True,
        height_field="height_field",
        width_field="width_field",
    )

    height_field = models.IntegerField(defualt= 500, null=True)
    width_field = models.IntegerField(defualt = 500, null=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


@receiver(pre_save,sender=User)
def create_account_no(sender, instance, *args, **kwargs):
# checking whether user has account number
    if not instance.account_no:
        # getting largest account number
        largest = User.objects.all().aggregate(
            Max("account_no"))['account_no__Max']
        if largest:
            # creatigaccount new number
            instance.account_no = largest + 1
        else:
            instance.account_no = 1000000

    def __str__(self):
        return str(self.account_no)


# transactions models
class Deposit(models.Model):
    """ Models for user deposit """
    user = models.ForeignKey(User)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('100.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Withdrawal(models.Model):
    user = models.ForeignKey(User)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('50.00'))
        ]
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)