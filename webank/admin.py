from django.contrib import admin
from .models import User,Deposit,Withdrawal
# Register your models here.
admin.site.register(User)
admin.site.register(Deposit)
admin.site.register(Withdrawal)