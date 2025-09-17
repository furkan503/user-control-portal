from rest_framework import serializers
from users.models import  Geo, Address, Company, User, Todo, Post, Comment, Album, Photo
from django.contrib.auth.models import User as AdminUser, Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields='__all__'


class AdminUserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, write_only=True)
    id = serializers.IntegerField(read_only=True)
    user_permissions = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    class Meta:
        model = AdminUser
        fields='__all__'
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', False)
        user_permissions = validated_data.pop('user_permissions', [])

        
        user = AdminUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.is_staff = is_staff
        user.is_superuser = False
        user.save()

        if user_permissions:
            permissions_qs = Permission.objects.filter(id__in=user_permissions)
            user.user_permissions.set(permissions_qs)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # def create(self,validated_data):
    #     return AdminUser.objects.create(**validated_data)

class GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geo
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    geo = GeoSerializer(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    todo = TodoSerializer(many=True, read_only=True)
    post = PostSerializer(many=True, read_only=True)
    album = AlbumSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
