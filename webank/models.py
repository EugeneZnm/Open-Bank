from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.core.validators import ( RegexValidator, MinValueValidator, MaxValueValidator )
# from .managers import UserManager
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
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

    gender =models.CharField(max_length=6, choices=GENDER_CHOICE)
    account_type = models.CharField(max_length=14, choices=Account_Choice)
    email = models.EmailField(unique=True, blank=False)
    phone = models.IntegerField(unique=True)
    city = models.CharField(max_length=256)
    nationality = models.CharField(max_length=300)
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

    def __str__(self):
        return str(self.account_no)