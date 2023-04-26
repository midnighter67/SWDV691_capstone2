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
    path('public_profile<result_user>', views.public_profile, name='publicProfile'), #/<result_id>
    path('review<profile_user>', views.review, name='review'),
    path('business_reviews<info_user>', views.business_reviews, name='businessReviews'),
    path('user_reviews<info_user>', views.user_reviews, name='userReviews'),
    path('reply<review_id>', views.reply, name='reply'),
    path('quote<profile_id>', views.quote, name='quote'),
    # path('review<profile_id>', views.submitReview, name='submitReview'),
]
