from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'finplanner'

urlpatterns = [

    # RESTRUCTURED VIEWS
    path('', views.home, name='home'),
    path('index', views.index, name='index'),
    path('landing', views.LandingView.landing, name ="landing"),
    path('new_account', views.new_account, name='new_account'),
    path('account/(?P<id>\d+)', views.account_detail, name="detail"),

    path('dashboard',views.Dashboard.index, name="dashboard"),
    path('expense/add',views.ExpenseCreate.as_view(), name="create_expense"),
    path('expenses', views.IndexView.as_view(), name ="expenses"),
    path('expense/update/<int:pk>', views.ExpenseUpdate.as_view(), name="update_expense"),
    path('analytics/<int:year>',views.AnalyticsView.annually, name="annually"),
    path('analytics', views.Dashboard.index, name="analytics"),

       # /analytics/2018/02
    path('analytics/<int:year>/<int:month>', views.AnalyticsView.monthly, name="monthly"),

    # /analytics/2018/02/20
    path('analytics/<int:year>/<int:month>/<int:day>',views.AnalyticsView.daily, name="daily"),
    path('accounts/', views.AccountList.as_view()),






    # # path('', views.login, name='login'),
    # path('', views.index, name='index'),
    # path('accounts/login/', views.login, name='login'),
    # path('register', views.register, name='register'),
    # path('dashboard', views.dashboard, name='dashboard'),
    # path('user/(?P<username>\w+)', views.profile, name='profile'),
    # path('accounts/edit', views.edit_profile, name='edit_profile'),
    # path('list/(?P<bank_id>\d+)', views.account_list, name="list"),
    # # path('add', views.AccountCreateView.as_view(), name="add"),
    # path('account/(?P<id>\d+)', views.account_detail, name="detail"),
    #
    # path('new_account/(?P<bank_id>\d+)', views.new_account, name='new_account'),


]

urlpatterns = format_suffix_patterns(urlpatterns)
