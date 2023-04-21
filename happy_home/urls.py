from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_user, name='login'),
    path('home', views.logout_user, name='logout'),
    path('create_account', views.register, name='createAccount'),
    path('change_password', views.change_password, name='changePassword'),
    path('user_profile', views.edit_profile, name='userProfile'),
    path('business_profile', views.edit_profile, name='businessProfile'),
    path('search_results', views.search_results, name='searchResults'),
    path('public_profile<result_id>', views.public_profile, name='publicProfile'), #/<result_id>
]
