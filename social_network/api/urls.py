from django.urls import path
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('posts', views.PostViewSet)

urlpatterns = [
    path('posts/<int:pk>/like/', views.LikeView.as_view()),
    path('posts/<int:pk>/dislike/', views.DisLikeView.as_view()),
    path('analytics/', views.AnalyticsView.as_view())
]

urlpatterns += router.urls