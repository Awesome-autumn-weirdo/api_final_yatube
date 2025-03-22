from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Comment, Post, Follow, Group

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

User = get_user_model()


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
    user = serializers.SlugRelatedField(slug_field='username',
                                        read_only=True)
    following = serializers.SlugRelatedField(slug_field='username',
                                             read_only=True)

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
