from django.contrib import admin
from .models import Post, Comment, Group, Follow

# Регистрация моделей в админке
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(Follow)
