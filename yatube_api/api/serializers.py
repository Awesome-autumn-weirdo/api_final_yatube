from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenVerifySerializer,
    TokenRefreshSerializer,
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import AccessToken

from posts.models import Comment, Post, Follow, Group

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data['username'] = self.user.username
            return data
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            access_token = AccessToken(data['access'])
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            data['username'] = user.username
            return data
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            token = attrs['token']
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            data['username'] = user.username
            return data
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password', 'email']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    pub_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ',
                                         read_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                               required=False)

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя."
            )
        return value

    def validate(self, data):
        if 'following' not in data:
            raise serializers.ValidationError(
                {"following": "Это поле обязательно."}
            )
        return data

    class Meta:
        model = Follow
        fields = ['user', 'following']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created']
        read_only_fields = ['author', 'post', 'created']
