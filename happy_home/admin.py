from django.contrib import admin
from .models import User, Provider, Consumer, Category, Rating, Classification


# Register your models here.
admin.site.register(User)
admin.site.register(Provider)
admin.site.register(Consumer)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Classification)
