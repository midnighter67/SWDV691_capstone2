from django.contrib import admin
from .models import User, Provider, Consumer, Review, Reply


# Register your models here. They are viewable and editable on the admin page.
admin.site.register(User)
admin.site.register(Provider)
admin.site.register(Consumer)
admin.site.register(Review)
admin.site.register(Reply)