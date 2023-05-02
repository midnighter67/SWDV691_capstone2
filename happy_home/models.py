from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Avg

# Create your models here.
class User(AbstractUser):
    is_provider = models.BooleanField('business', default=False)
    is_user = models.BooleanField('user', default=False)


class Provider(models.Model):
    user = models.IntegerField(null=True)
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
    cleaning = models.BooleanField(default=False, blank=True)
    plumbing = models.BooleanField(default=False, blank=True)
    electrical = models.BooleanField(default=False, blank=True)
    improvement = models.BooleanField(default=False, blank=True)
    landscape = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name

    def avgReview(self, userid):
        reviews = Review.objects.filter(provider=userid).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg


class Consumer(models.Model):
    user = models.IntegerField(null=True)
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.first + " " + self.last
    

class Review(models.Model):
    provider = models.IntegerField(null=True)
    consumer = models.IntegerField(null=True)
    title = models.CharField(max_length=30, blank=True)
    rating = models.FloatField(default=1)
    text = models.CharField(max_length=1000, blank=True)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000, default="")

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'



