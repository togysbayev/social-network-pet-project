from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import Post, Like, DisLike
from .serializers import PostSerializer, LikeSerializer, DisLikeSerializer, AnalyticsSerializer
from .permissions import IsOwnerOfPost
from .filters import LikeFilter


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['head', 'options', 'get', 'post', 'put']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method in ['PUT', 'DELETE']:
            return [IsOwnerOfPost()]
        return [AllowAny()]
  

class LikeView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    
class DisLikeView(CreateAPIView):
    queryset = DisLike.objects.all()
    serializer_class = DisLikeSerializer
    permission_classes = [IsAuthenticated]
    
class AnalyticsView(ListAPIView):
    serializer_class = AnalyticsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikeFilter
        
    def get_queryset(self):
        return Like.objects.extra(select={'date':"to_char(api_like.liked_at, 'YYYY-MM-DD')"}).values('date').annotate(likes=Count('liked_user'))
        
    



    
   