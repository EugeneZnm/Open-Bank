# from __future__ import unicode_literals
# from django.db import models
# from django.urls import reverse
# from django.core.validators import ( RegexValidator, MinValueValidator, MaxValueValidator )
# # from .managers import UserManager
# from django.contrib.auth.models import AbstractUser, UserManager
# from django.db.models import Max
# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# from decimal import Decimal
# from django.conf import settings

# Accounts models here.


# from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )
from django.db import models
from django.urls import reverse
from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.base_user import BaseUserManager

from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from .managers import UserManager

User = settings.AUTH_USER_MODEL

NAME_REGEX = '^[a-zA-Z ]*$'

GENDER_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
    )


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    account_no = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
            ]
        )

    full_name = models.CharField(
        max_length=256,
        blank=False,
        validators=[
                RegexValidator(
                    regex=NAME_REGEX,
                    message='Name must be Alphabetic',
                    code='invalid_full_name'
                    )
                ]
        )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    contact_no = models.IntegerField(unique=True)
    Address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    nationality = models.CharField(max_length=256)
    occupation = models.CharField(max_length=256)
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

    height_field = models.IntegerField(default=600, null=True)
    width_field = models.IntegerField(default=600, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = []  # required when user is created

@receiver(pre_save, sender=User)
def create_account_no(sender, instance, *args, **kwargs):
    # checks if user has an account number
    if not instance.account_no:
        # gets the largest account number
        largest = User.objects.all().aggregate(
            Max("account_no")
            )['account_no__max']

        if largest:
            # creates new account number
            instance.account_no = largest + 1
        else:
            # if there is no other user, sets users account number to 10000000.
            instance.account_no = 10000000

    def __str__(self):
        return str(self.account_no)

# transactions models
class Deposit(models.Model):
    user = models.ForeignKey('User')
    amount = models.DecimalField(
      decimal_places=2,
      max_digits=12,
      validators=[
          MinValueValidator(Decimal('10.00'))
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
          MinValueValidator(Decimal('10.00'))
          ]
      )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)