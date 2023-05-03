from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
# from django.http import HttpResponse
# from django.http import HttpRequest
from .models import Provider, Consumer, Reply, Review, User
from .forms import LoginForm, SignUpForm, UserProfileForm, BusinessProfileForm, UpdatePasswordForm, ReviewForm, ReplyForm, QuoteForm
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from smtplib import SMTPException
import math
# import json

# Create your views here.


def home(request):
    """ Initial landing page that also hosts the search funtion """
    return render(request, 'home.html', {})

def login_user(request):
    """ User authentication for both user and provider"""
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_provider:
                login(request, user)
                return redirect('home')
            elif user is not None and user.is_user:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, ('Invalid username or password'))
        else:
            messages.success(request, ('Form is invalid'))
    return render(request, 'login.html', {'form':form, 'msg':msg})

def logout_user(request):
    """ Logout registered authenticated users and businesses """
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('login')

def register(request):
    """ register account for both user and business using a role field """
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  #  and (provider ^ consumer)
            provider = form.cleaned_data['is_provider']
            consumer = form.cleaned_data['is_user']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            if provider ^ consumer:
                form.save() # user = form.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                if provider:
                    post = Provider()
                else:
                    post = Consumer()
                post.user = request.user.id
                post.email = email
                post.save()
                messages.success(request, ('Account registered successfully.'))
            else:
                messages.success(request, ('Please select only one account, business or user.'))
                return redirect('createAccount')
            if provider:
                return redirect('businessProfile')
            else:
                return redirect('userProfile')
        else:
            messages.success(request, ('Form invalid.  Must be business or user.'))
    else:
        form = SignUpForm()
    return render(request,'create_account.html', {'form': form})

def delete_account(request, user_username):
    """ delete user account, consumer or provider record, and any provider reviews/replies """
    if request.user.is_authenticated:
        try:
            registered_user = User.objects.get(username=user_username)
            if request.user.is_provider:
                provider = Provider.objects.get(user=request.user.id)
                Review.objects.filter(provider=provider.user).delete()
                Provider.objects.filter(user=request.user.id).delete()
            else:
                Consumer.objects.filter(user=request.user.id).delete()
            logout(request)
            registered_user.delete()
            messages.success(request, ('Account deleted'))
        except registered_user.DoesNotExist:
            messages.success(request, ('Account does not exist'))
        except Exception as e:
            messages.success(request, ('Delete failed: ' + e.message))
    return render(request,'home.html', {})

def change_password(request):
    """ Update pass word for registered users, both user and business """
    if request.method == "POST":
        form = UpdatePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
          form.save()
          update_session_auth_hash(request, form.user) # so updating password doesn't logout user
          messages.success(request, ('Password updated'))
          return redirect('home') 
    else:
        form =UpdatePasswordForm(user=request.user)
    context = {'password_form': form}
    return render(request, 'change_password.html', context) # return render(request, 'change_password.html', context)

def edit_profile(request):
    """ Update and display profile data for both user and business """
    provider = False
    if request.user.is_authenticated:
        if request.user.is_provider:
            provider = True
            info = Provider.objects.get(email=request.user.email)
            form = BusinessProfileForm(request.POST or None, instance=info)
        elif request.user.is_user:
            info = Consumer.objects.get(email=request.user.email)
            form = UserProfileForm(request.POST or None, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, ('Profile Updated'))
            # return redirect('user_profile')
    if provider:
        context = {'business_profile_form': form, 'info': info}
        route = 'business_profile.html'
    else:
        context = {'user_profile_form': form, 'info': info}
        route = 'user_profile.html'
    return render(request, route, context) # {'info': info, 'form': form}

def search_results(request):
    """ generate a list of businesses based on search text or chosen category """
    if request.method == "POST":
        if 'cleanSearch' in request.POST:
            results = Provider.objects.filter(cleaning=True)
            return render(request, 'search_results.html', {'results':results})
        elif 'plumbingSearch' in request.POST:
            results = Provider.objects.filter(plumbing=True)
            return render(request, 'search_results.html', {'results':results})
        elif 'electricalSearch' in request.POST:
            results = Provider.objects.filter(electrical=True)
            return render(request, 'search_results.html', {'results':results})
        elif 'improvementSearch' in request.POST:
            results = Provider.objects.filter(improvement=True)
            return render(request, 'search_results.html', {'results':results})
        elif 'landscapeSearch' in request.POST:
            results = Provider.objects.filter(landscape=True)
            return render(request, 'search_results.html', {'results':results})
        else:
            text = request.POST.get('searchText')
            if text != None:
                results = Provider.objects.filter(name__contains=text)
                return render(request, 'search_results.html', {'results':results})
            else:
                results = None
                return render(request, 'search_results.html', {'results':results})
    else:
        return render(request, 'home.html', {})
    
def public_profile(request, result_user): 
    """ display business data including review average """
    profile = Provider.objects.get(user=result_user)
    reviews = Review.objects.filter(provider=result_user)
    stats = {}
    total = 0
    index = 0
    floor = 0
    half = 0
    for review in reviews:
        index = index + 1
        total = total + review.rating
    if index == 0:
        average = 0
    else:
        average = round(total/index,1)
    floor = math.floor(average)
    x = average - floor
    if (x > 0.7):
        floor = floor + 1
        half = 0
    elif (x >= 0.3 and x <= 0.7):
        half = 1
    stats['average'] = average
    stats['floor'] = floor
    stats['half'] = half
    stats['index'] = index + 1
    
    return render(request, 'public_profile.html', {'profile':profile, 'stats':stats})

def review(request, profile_user):
    """ Save review rating and text left by user """
    # url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        current = Consumer.objects.get(email=request.user.email)
        profile = Provider.objects.get(user=profile_user)
        if request.method == "POST":
            try:
                reviews = Review.objects.get(consumer=current.user, provider=profile_user)
                form = ReviewForm(request.POST, instance=reviews)
                form.save()
                messages.success(request, ('Review updated'))
                # return redirect('url')
            except Review.DoesNotExist:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    data = Review()
                    data.title = form.cleaned_data['title']
                    data.rating = form.cleaned_data['rating']
                    data.text = form.cleaned_data['text']
                    
                    data.provider = profile_user
                    data.consumer = current.user
                    data.save()
                   
                    messages.success(request, ('Review saved'))
            return redirect('publicProfile', profile_user)
        else:
            return render(request, 'review.html', {'profile':profile})
    else:
        messages.success(request, ('You must be logged in to leave a review'))
        profile = Provider.objects.get(user=profile_user)
        return render(request, 'public_profile.html', {'profile':profile} )
    

def reply(request, review_id):
    """ save reply text in response to a review that was left by a registered user """
    url = request.META.get('HTTP_REFERER')
    reply = 0
    review = Review.objects.get(id=review_id)
    if request.method == "POST":
        try:
            reply = Reply.objects.get(review__id=review_id)
            form = ReplyForm(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your reply has been updated')
                return redirect('businessReviews', review.provider)
            else:
                messages.success(request, 'form invalid')
                return redirect('reply', review_id)
            # return redirect(url)
        except Reply.DoesNotExist:
            form = ReplyForm(request.POST)
            if form.is_valid():
                data = Reply()
                data.review_id = review_id
                data.text = form.cleaned_data['text']
                data.save()
                messages.success(request, 'Your reply has been saved')
                # return redirect(url)
                return redirect('businessReviews', review.provider)
            else:
                messages.success(request, 'form invalid')
                return redirect('reply', review_id)
    else:
        review = Review.objects.get(id=review_id)
        try:
            reply = Reply.objects.get(review__id=review_id)
        except Reply.DoesNotExist:
            reply = 0
        return render(request, 'reply.html', {'review':review, 'reply':reply})


def business_reviews(request, info_user):
    """ generate a list of reviews for the logged in provider left by registered users """
    if request.user.is_authenticated:
        if request.user.is_provider:
            provider = Provider.objects.get(user=info_user) 
            reviews = Review.objects.filter(provider=info_user)
            users = []
            replies = []
            for review in reviews:
                try:
                    reply = Reply.objects.get(review__id=review.id)
                except Reply.DoesNotExist:
                    reply = 0
                try:
                    consumer = Consumer.objects.get(user=review.consumer)
                    name = consumer.first + " " + consumer.last
                except Consumer.DoesNotExist:
                    name = "deleted account"
                users.append(name)
                replies.append(reply)
            data = zip(reviews, users, replies)
            return render(request, 'business_reviews.html', {'data':data, 'provider': provider} ) 
        else:
            messages.success(request, ('You must be logged in as a business'))
            return redirect('login')
    else:
        messages.success(request, ('You must be logged in to get review list'))
        return redirect('login')
    
def user_reviews(request, info_user):
    """ generate a list of reviews created by the logged in consumer for registered providers """
    if request.user.is_authenticated:
        if request.user.is_user:
            consumer = Consumer.objects.get(user=info_user) 
            reviews = Review.objects.filter(consumer=info_user)
            providers = []
            replies = []
            for review in reviews:
                provider = Provider.objects.get(user=review.provider)
                try:
                    reply = Reply.objects.get(review__id=review.id)
                except Reply.DoesNotExist:
                    reply = 0
                name = provider.name
                providers.append(name)
                replies.append(reply)
            data = zip(reviews, providers, replies)
            return render(request, 'user_reviews.html', {'data':data, 'consumer': consumer} ) 
        else:
            messages.success(request, ('You must be logged in as a user'))
            return redirect('login')
    else:
        messages.success(request, ('You must be logged in to get review list'))
        return redirect('login')
    
def quote(request, profile_id):
    """ send an email from the registered user requesting a quote from a registered provider """
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        if request.user.is_user:
            provider = Provider.objects.get(user=profile_id)
            consumer = Consumer.objects.get(email=request.user.email)
            if request.method == "POST":
                form = QuoteForm(request.POST)
                if form.is_valid():
                    try:
                        text = form.cleaned_data.get('text') 
                        msg = text + "\n\n" + consumer.first + " " + consumer.last + "\n" + consumer.email
                        send_mail(
                            "Happy Home Quote Request",
                            msg,
                            'chetley3@yahoo.com',
                            [provider.email],
                            fail_silently=False,
                        )
                        messages.success(request, ('Request sent successfully!'))
                        return redirect(url)
                    except SMTPException:
                        messages.success(request, ('You must be logged in to get review list'))
                        return redirect(url)
                else:
                    messages.success(request, ('Submit failed.  A message to ' + provider.name + ' is required'))
                    return render(request, 'quote.html', {"provider":provider} )
            else:
                return render(request, 'quote.html', {'consumer':consumer, 'provider': provider} )
        else:
            messages.success(request, ('You must be logged in as a user to request a quote'))
            return redirect('login')
    else:
        messages.success(request, ('You must be logged in to request a quote'))
        return redirect('login')

        

"""
if request.user.is_authenticated:
    if request.user.is_user:
        consumer = Consumer.objects.get(user=info_user) #(email=request.user.email)
        reviews = Review.objects.filter(consumer=info_user)
        return render(request, 'user_reviews.html', {'reviews':reviews, 'consumer': consumer} ) # ,'profile_user':profile_user
    else:
        messages.success(request, ('You must be logged in as a user'))
        return redirect('login')
else:
    messages.success(request, ('You must be logged in to get review list'))
    return redirect('login')



if request.user.is_authenticated:
        if request.user.is_provider:
            provider = Provider.objects.get(user=info_user) #(email=request.user.email)
            reviews = Review.objects.filter(provider=info_user)
            return render(request, 'business_reviews.html', {'reviews':reviews, 'provider': provider} ) # ,'profile_user':profile_user
        else:
            messages.success(request, ('You must be logged in as a business'))
            return redirect('login')
    else:
        messages.success(request, ('You must be logged in to get review list'))
        return redirect('login')
"""