from django.contrib.auth.models import AbstractUser
from django.db import models


class SocialNetworkUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username
    
class Post(models.Model):
    author = models.ForeignKey(SocialNetworkUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    likes = models.ManyToManyField(SocialNetworkUser, through='Like', related_name='liked_posts')
    dislikes = models.ManyToManyField(SocialNetworkUser, through='DisLike', related_name='disliked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Like(models.Model):
    liked_user = models.ForeignKey(SocialNetworkUser, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    
class DisLike(models.Model):
    disliked_user = models.ForeignKey(SocialNetworkUser, on_delete=models.CASCADE)
    disliked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    disliked_at = models.DateTimeField(auto_now_add=True)
    
    
    

