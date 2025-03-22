from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet,
    CustomTokenObtainPairView, CustomTokenRefreshView
)
from djoser.views import UserViewSet

router = DefaultRouter()
router.register(r'v1/posts', PostViewSet, basename='post')
router.register(r'v1/groups', GroupViewSet, basename='group')
router.register(r'v1/follow', FollowViewSet, basename='follow')
router.register(r'v1/users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    # Вложенные маршруты для комментариев
    path('v1/posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comment-list'),
    path('v1/posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'}),
         name='comment-detail'),
]
