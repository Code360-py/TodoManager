from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User, Todo


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('is_active',)


@admin.register(Todo)
class TodoAdmin(ModelAdmin):
    list_display = ('id', 'title', 'user', 'completed', 'created_at')
    search_fields = ('title', 'user__username')
    list_filter = ('completed',)