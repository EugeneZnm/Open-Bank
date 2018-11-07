from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.core.validators import ( RegexValidator, MinValueValidator, MaxValueValidator )
from .managers import UserManager
# Accounts models here.


# name validator
Name_Regex = '^[a-zA-Z ]*S'

GENDER_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
)

class User(AbstractUser):
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
            MinValueValidator(1000000)
            MaxValueValidator(999999999999)
        ]
    )


    full_name = models.CharField(
    """ validating user name, restricted to alphabets """,

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
