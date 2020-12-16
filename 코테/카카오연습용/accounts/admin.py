from django.contrib import admin
from .models import Post, Profile,Event,Notice,Comment,Recomment

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Notice)

admin.site.register(Comment)
admin.site.register(Recomment)

