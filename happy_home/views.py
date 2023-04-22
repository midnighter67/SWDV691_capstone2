from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
# from django.http import HttpResponse
# from django.http import HttpRequest
from .models import Provider, Consumer, Rating, Review
from .forms import LoginForm, SignUpForm, UserProfileForm, BusinessProfileForm, UpdatePasswordForm, ReviewForm, RatingForm
from django.contrib import messages
import math
# import json

# Create your views here.

def home(request):
    """ Initial landing page that also hosts the search funtion """
    """
    if request.method == 'GET':
        message = "Hello World"
    else:
        message = "Hello World!"
    """
    print("home")
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
          msg = 'invalid credentials'
      else:
        msg = 'invalid form'
    return render(request, 'login.html', {'form':form, 'msg':msg})

def logout_user(request):
    """ Logout registered authenticated users and businesses """
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')

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
                messages.success(request, ('Your account has been registered.  Please login.'))
            else:
                messages.success(request, ('Please select only one account, business or user.'))
                return redirect('createAccount')
            return redirect('login')
        else:
            messages.success(request, ('Form invalid.  Must be business or user.'))
    else:
        form = SignUpForm()
    return render(request,'create_account.html', {'form': form})

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
        context = {'business_profile_form': form}
        route = 'business_profile.html'
    else:
        context = {'user_profile_form': form}
        route = 'user_profile.html'
    return render(request, route, context) # {'info': info, 'form': form}

def search_results(request):
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
    
def public_profile(request, result_user): #result_id
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
    if (.7 > average - floor < floor + 1):
        floor = floor + 1
        half = 0
    elif (.3 >= average - floor <= .7):
        half = 1
    stats['average'] = average
    stats['floor'] = floor
    stats['half'] = half
    stats['index'] = index + 1
    
    return render(request, 'public_profile.html', {'profile':profile, 'stats':stats})

def review(request, profile_user):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        current = Consumer.objects.get(email=request.user.email)
        if request.method == "POST":
            try:
                reviews = Review.objects.get(consumer=current.user, provider=profile_user)
                form = ReviewForm(request.POST, instance=reviews)
                form.save()
                messages.success(request, ('Review updated'))
                return redirect('home')
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
                    return redirect('login')
        else:
            profile = Provider.objects.get(user=profile_user)
            return render(request, 'review.html', {'profile':profile})
    else:
        print("oops")
        messages.success(request, ('You must be logged in to leave a review'))
        profile = Provider.objects.get(user=profile_user)
        return render(request, 'public_profile.html', {'profile':profile} )
    


"""
if request.method == "POST":
            if request.user.is_authenticated:
                profile = Provider.objects.get(pk=profile_id)
                return render(request, 'review.html', {'profile':profile})
        else:
            return render(request, 'review.html', {'profile':profile})
"""



"""   
def user_reviews(request):
    if request.method == "POST":
        mymethod = "post"
    elif request.method == "GET":
        mymethod = "get"
    else:
        mymethod = "neither post nor get"
    return render(request, 'user_reviews.html', {'mymethod':mymethod})

"""