from rest_framework import viewsets, status, permissions
from users.models import User, Todo, Post, Comment, Album, Photo, Address, Company, Geo
from .serializers import LoginSerializer, AdminUserSerializer, PermissionSerializer, UserSerializer, TodoSerializer, PostSerializer, CommentSerializer, AlbumSerializer, PhotoSerializer, AddressSerializer, CompanySerializer, GeoSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from users.api.pagination import Pagination
from django.contrib.auth.models import User as AdminUser, Permission
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
import json
# from users.api.permissions import IsAdminUserOrReadOnly
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    @action(detail=False, methods=['get'], url_path='check_permission')
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if request.user.has_perm(permission):
            return Response({'has_permission': True})
        return Response({'has_permission': False})


class LoginViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    # authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['POST'],    permission_classes=[permissions.AllowAny]
            )
    def custom_login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            request.session['logged_in_message'] = 'User logged in successfully'

            return Response({
                'message': 'logged in',
                'access': access_token,
                'refresh': refresh_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'could not log in'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'],    permission_classes=[DjangoModelPermissions]
            )
    def add_admin(self, request):
        data = request.data
        admins_created = []

        try:
            with transaction.atomic():
                for admin_data in data:
                    if isinstance(admin_data, str):
                        admin_data = json.loads(admin_data)

                    serializer = AdminUserSerializer(data=admin_data)
                    if serializer.is_valid():
                        serializer.save()
                        admins_created.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'created_admins': admins_created})
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='check_permission',    permission_classes=[permissions.AllowAny]
            )
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if request.user.has_perm(permission):
            return Response({'has_permission': True})
        return Response({'has_permission': False})

    @action(detail=True, methods=['put'], url_path='update_permissions', permission_classes=[DjangoModelPermissions])
    def update_permissions(self, request, pk=None):
        try:
            user = AdminUser.objects.get(pk=pk)
        except AdminUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        permission_ids = request.data.get('user_permissions', [])
        permissions = Permission.objects.filter(id__in=permission_ids)
        user.user_permissions.set(permissions)
        return Response({'status': 'Permissions updated successfully'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    # parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]
    pagination_class = Pagination

    @action(detail=False, methods=['get', 'post', 'put'])
    def multiple(self, request):
        data = request.data
        users_created = []

        try:
            with transaction.atomic():
                for user_data in data:
                    if isinstance(user_data, str):
                        user_data = json.loads(user_data)

                    address_data = user_data.pop('address', None)
                    company_data = user_data.pop('company', None)
                    geo_data = None

                    if address_data:
                        geo_data = address_data.pop('geo', None)

                    geo_instance = None
                    if geo_data:
                        geo_instance = Geo.objects.create(**geo_data)

                    address_instance = None
                    if address_data:
                        address_instance = Address.objects.create(
                            geo=geo_instance, **address_data)

                    company_instance = None
                    if company_data:
                        company_instance = Company.objects.create(
                            **company_data)

                    user = User.objects.create(
                        name=user_data['name'],
                        username=user_data.get('username', ''),
                        email=user_data['email'],
                        website=user_data['website'],
                        phone=user_data['phone'],
                        address=address_instance,
                        company=company_instance,
                    )

                    users_created.append(user.id)

            return Response({'created_user_ids': users_created})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=True, methods=['post', 'get'], name='Upload Image', url_path='upload-image')
    def upload_image(self, request, pk=None):
        parser_classes = (MultiPartParser, FormParser)
        user = self.get_object()
        image_file = request.data.get('image')
        if image_file:
            user.image_file = image_file
            user.save()
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': 'Image file not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='check_permission')
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if request.user.has_perm(permission):
            return Response({'has_permission': True})
        return Response({'has_permission': False})


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data
        addresses_created = []

        for item in data:
            geo_data = item.pop('geo', None)

            geo_instance = None
            if geo_data:
                geo_instance = Geo.objects.create(**geo_data)

            address_instance = Address.objects.create(geo=geo_instance, **item)
            addresses_created.append(address_instance.id)

        return Response('added')


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data
        companies_created = []

        for item in data:
            company = Company.objects.create(
                name=item['name'],
                catchPhrase=item['catchPhrase'],
                bs=item['bs'],
            )
            companies_created.append(company.id)

        return Response('added')


class GeoViewSet(viewsets.ModelViewSet):
    queryset = Geo.objects.all()
    serializer_class = GeoSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data
        geos_created = []

        for item in data:
            geo = Geo.objects.create(
                lat=item['lat'],
                lng=item['lng'],
            )
            geos_created.append(geo.id)

        return Response('added')


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('id')
    serializer_class = TodoSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data

        for item in data:
            todo = Todo.objects.create(
                user_id=item['userId'],
                title=item['title'],
                completed=item['completed'],
            )

        return Response('added')

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_todos_by_user(self, request, user_id=None):
        queryset = Todo.objects.filter(user_id=user_id).order_by('id')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='check_permission')
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if request.user.has_perm(permission):
            return Response({'has_permission': True})
        return Response({'has_permission': False})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data

        for item in data:
            post = Post.objects.create(
                user_id=item['userId'],
                title=item['title'],
                body=item['body'],
            )

        return Response('added')

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_posts_by_user(self, request, user_id=None):
        queryset = Post.objects.filter(user_id=user_id).order_by('id')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='check_permission')
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if request.user.has_perm(permission):
            return Response({'has_permission': True})
        return Response({'has_permission': False})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data

        for item in data:
            image_file = request.FILES.get('image_file')
            comment = Comment.objects.create(
                post_id=item['postId'],
                name=item['name'],
                email=item['email'],
                body=item['body'],
                image_file=image_file
            )

        return Response('added')

    @action(detail=False, methods=['get'], url_path='post/(?P<post_id>[^/.]+)')
    def list_comments_by_post(self, request, post_id=None):
        queryset = Comment.objects.filter(post_id=post_id).order_by('id')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['post', 'get'], url_path='upload-comment-image')
    def upload_comment_image(self, request):
        if request.method == 'POST':
            image_file = request.data.get('image')
            post_id = request.data.get('post_id')
            name = request.data.get('name')
            email = request.data.get('email')
            body = request.data.get('body')

            if image_file and post_id and name and email and body:
                new_comment = Comment.objects.create(
                    post_id=post_id,
                    name=name,
                    email=email,
                    body=body,
                    image_file=image_file
                )
                serializer = self.get_serializer(new_comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='check_permission')
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if request.user.has_perm(permission):
            return Response({'has_permission': True})
        return Response({'has_permission': False})


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('id')
    serializer_class = AlbumSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data

        for item in data:
            album = Album.objects.create(
                user_id=item['userId'],
                title=item['title'],
            )

        return Response('added')

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def list_albums_by_user(self, request, user_id=None):
        queryset = Album.objects.filter(user_id=user_id).order_by('id')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='check_permission')
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if request.user.has_perm(permission):
            return Response({'has_permission': True})
        return Response({'has_permission': False})


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by('id')
    serializer_class = PhotoSerializer
    # pagination_class = Pagination
    parser_classes = (MultiPartParser, FormParser)
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions]

    @action(detail=False, methods=['post'])
    def multiple(self, request):
        data = request.data

        for item in data:
            image_file = request.FILES.get('image_file')
            photo = Photo.objects.create(
                album_id=item['albumId'],
                title=item['title'],
                url=item['url'],
                thumbnail_url=item['thumbnailUrl'],
                image_file=image_file
            )

        return Response('added')

    @action(detail=False, methods=['get'], url_path='album/(?P<album_id>[^/.]+)')
    def list_photos_by_album(self, request, album_id=None):

        queryset = Photo.objects.filter(album_id=album_id).order_by('id')
        params = request.query_params
        print('ksdldkos', params)
        if 'page' in params:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'get'])
    def upload_photo(self, request):
        parser_classes = (MultiPartParser, FormParser)
        image_file = request.data.get('image')
        title = request.data.get('title')
        # Assuming you pass album_id in the request
        album_id = request.data.get('album_id')

        if image_file and album_id:
            # Create a new Photo instance associated with the specified album
            try:
                album = Album.objects.get(id=album_id)
                new_photo = Photo.objects.create(
                    image_file=image_file, title=title, album=album)
                serializer = self.get_serializer(new_photo)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Album.DoesNotExist:
                return Response({'error': 'Album does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Image file or album_id not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='check_permission')
    def check_permission(self, request):
        permission = request.query_params.get('permission')
        if not permission:
            return Response({'error': 'Permission parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.has_perm(permission):
            return Response({'has_permission': True}, status=status.HTTP_200_OK)
        else:
            return Response({'has_permission': False}, status=status.HTTP_403_FORBIDDEN)
