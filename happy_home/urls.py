from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_view, name='login'),
    # path('logout', views.logout_user, name='logout'),
    path('create_account', views.register, name='createAccount'),
    # path('user_profile', views.edit_profile, name='userProfile'),
]
