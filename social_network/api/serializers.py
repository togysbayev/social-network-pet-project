from django.contrib.auth.models import User
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from .models import Post, Like, DisLike
from rest_framework import serializers

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(read_only=True)
    likes_quantity = serializers.SerializerMethodField()
    dislikes_quantity = serializers.SerializerMethodField()
    
    def get_likes_quantity(self, post_item: Post):
        return post_item.likes.count()
    
    def get_dislikes_quantity(self, post_item: Post):
        return post_item.dislikes.count()
    class Meta:
        model = Post
        fields = ['id', 'author_id', 'title', 'body', 'likes_quantity', 'dislikes_quantity', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        author_id = self.context['request'].user.id
        return Post.objects.create(author_id=author_id, **validated_data)

    
class LikeSerializer(serializers.ModelSerializer):
    liked_user_id = serializers.IntegerField(read_only=True)
    liked_post_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Like
        fields = ['liked_user_id', 'liked_post_id', 'liked_at']
        
    def create(self, validated_data):
        path = self.context["request"].path
        subs = path.split('posts/')[1]
        post_id = subs.split('/')[0]
        user_id = self.context['request'].user.id
        
        if user_id in DisLike.objects.filter(disliked_post_id=post_id).values_list('disliked_user_id', flat=True):
            DisLike.objects.get(disliked_post_id=post_id, disliked_user_id=user_id).delete()
        
        if user_id in Like.objects.filter(liked_post_id=post_id).values_list('liked_user_id', flat=True):
            return Like.objects.get(liked_post_id=post_id, liked_user_id=user_id).delete()        
        else:
            return Like.objects.create(liked_post_id=post_id, liked_user_id=user_id)


class DisLikeSerializer(serializers.ModelSerializer):
    disliked_user_id = serializers.IntegerField(read_only=True)
    disliked_post_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = DisLike
        fields = ['disliked_user_id', 'disliked_post_id', 'disliked_at']
        
    def create(self, validated_data):
        path = self.context["request"].path
        subs = path.split('posts/')[1]
        post_id = subs.split('/')[0]
        user_id = self.context['request'].user.id
        
        if user_id in Like.objects.filter(liked_post_id=post_id).values_list('liked_user_id', flat=True):
            Like.objects.get(liked_post_id=post_id, liked_user_id=user_id).delete()
        
        if user_id in DisLike.objects.filter(disliked_post_id=post_id).values_list('disliked_user_id', flat=True):
            return DisLike.objects.get(disliked_post_id=post_id, disliked_user_id=user_id).delete()
        else:
            return DisLike.objects.create(disliked_post_id=post_id, disliked_user_id=user_id)
        
class AnalyticsSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    likes = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['date', 'likes']

