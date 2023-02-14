from django.contrib import admin
from .models import SocialNetworkUser, Post, Like, DisLike

admin.site.register(SocialNetworkUser)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(DisLike)

