from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # 👤 AUTH
    # ==========================
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ==========================
    # 📊 DASHBOARD
    # ==========================
    path('', views.dashboard, name='dashboard'),

    # ==========================
    # ✅ TODO CRUD
    # ==========================
    path('add/', views.add_todo, name='add_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]