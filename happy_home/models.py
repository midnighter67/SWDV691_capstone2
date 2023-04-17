from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    is_provider = models.BooleanField('business', default=False)
    is_user = models.BooleanField('user', default=False)

"""
class Provider(models.Model):
    # provider_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    poc_first = models.CharField(max_length=50, blank=True)
    poc_last = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    url = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=5000, blank=True)

class Consumer(models.Model):
    # user_id = models.BigAutoField(primary_key=True)
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
"""



"""
class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Classification(models.Model):
    provider_id = models.ForeignKey(Provider, default=-1, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, default=-1, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_id
    
class Review(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    provider_id = models.ForeignKey(Provider, default=-1, on_delete=models.CASCADE)
    user_id = models.ForeignKey(SiteUser, default=-1, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    text = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return "For " + self.provider_id + " from " + self.user_id
    
class Reply(models.Model):
    reply_id = models.BigAutoField(primary_key=True)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, default="")

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self): 
        return "For review: " + self.review_id
"""