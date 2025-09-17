from django.urls import path, include
from users.api.views import PermissionViewSet, LoginViewSet, UserViewSet, TodoViewSet, PostViewSet, CommentViewSet, AlbumViewSet, PhotoViewSet, AddressViewSet, CompanyViewSet, GeoViewSet
from rest_framework import routers, serializers, viewsets
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'todos', TodoViewSet, basename='todos')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'albums', AlbumViewSet, basename='albums')
router.register(r'photos', PhotoViewSet, basename='photos')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'geo', GeoViewSet, basename='geo')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'permissions', PermissionViewSet, basename='permissions')

urlpatterns = [
    path('', include(router.urls)),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
]


# urlpatterns = [
#     path('users/',
#          UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
#     path('users/<int:pk>/', UserViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),

#     path('todos/',
#          TodoViewSet.as_view({'get': 'list', 'post': 'create'}), name='todo-list'),
         
#     path('todos/<int:pk>/', TodoViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='todo-detail'),
#     path('todos/user/<int:user_id>/', TodoViewSet.as_view(
#         {'get': 'list_todos_by_user'}), name='todo-user'),


#     path('posts/',
#          PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
#     path('posts/<int:pk>/', PostViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='post-detail'),
#     # path('posts/user/<int:user_id>/', PostViewSet.as_view(
#     #     {'get': 'list_posts_by_user'}), name='post-user'),  
#     path('posts/multiple/', PostViewSet.as_view(
#         {'post': 'multiple'}), name='post-multiple'),  

#     path('comments/',
#          CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
#     path('comments/<int:pk>/', CommentViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-detail'),

#     path('albums/',
#          AlbumViewSet.as_view({'get': 'list', 'post': 'create'}), name='album-list'),
#     path('albums/<int:pk>/', AlbumViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='album-detail'),

#     path('photos/',
#          PhotoViewSet.as_view({'get': 'list', 'post': 'create'}), name='photo-list'),
#     path('photos/<int:pk>/', PhotoViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='photo-detail'),

#     path('address/',
#         AddressViewSet.as_view({'get': 'list', 'post': 'create'}), name='address-list'),
#     path('address/<int:pk>/', AddressViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='address-detail'),
    
#     path('company/',
#          CompanyViewSet.as_view({'get': 'list', 'post': 'create'}), name='company-list'),
#     path('company/<int:pk>/', CompanyViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='company-detail'),

#     path('geo/',
#          GeoViewSet.as_view({'get': 'list', 'post': 'create'}), name='geo-list'),
#     path('geo/<int:pk>/', GeoViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='geo-detail'),
# ]
