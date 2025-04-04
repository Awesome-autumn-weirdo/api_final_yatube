from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Post, Follow, Group

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    pub_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ',
                                         read_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                               required=False)

    class Meta:
        model = Post
        fields = '__all__'
        ordering = ['-pub_date']

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
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
