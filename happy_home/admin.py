from django.contrib import admin
from .models import User, Provider, Consumer, Review


# Register your models here.
admin.site.register(User)
admin.site.register(Provider)
admin.site.register(Consumer)
admin.site.register(Review)
