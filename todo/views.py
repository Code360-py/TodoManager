from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from functools import wraps
from .models import User, Todo


# ==============================
# 🔐 AUTH DECORATOR
# ==============================
def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        user = User.objects.filter(id=user_id).first()
        if not user:
            request.session.flush()
            return JsonResponse({"error": "Invalid session"}, status=401)

        request.user_obj = user
        return view_func(request, *args, **kwargs)

    return wrapper


# ==============================
# 👤 AUTH (UNCHANGED - still template based)
# ==============================

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "All fields are required")
            return redirect("login")

        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            messages.error(request, "Invalid credentials")
            return redirect("login")

        request.session["user_id"] = user.id
        request.session.set_expiry(3600)

        messages.success(request, "Logged in successfully")
        return redirect("dashboard")

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect("login")


# ==============================
# 📊 DASHBOARD
# ==============================
@login_required_custom
def dashboard(request):
    todos = Todo.objects.filter(user=request.user_obj).order_by("-id")
    return render(request, "dashboard.html", {
        "todos": todos,
        "user": request.user_obj
    })


# ==============================
# ➕ CREATE TODO (AJAX)
# ==============================
@login_required_custom
def add_todo(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        todo = Todo.objects.create(
            user=request.user_obj,
            title=title,
            description=description
        )

        return JsonResponse({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.strftime("%b %d, %Y %H:%M")
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


# ==============================
# ✏️ EDIT TODO (AJAX)
# ==============================
@login_required_custom
def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user_obj)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if not title:
            return JsonResponse({"error": "Title required"}, status=400)

        todo.title = title
        todo.description = description
        todo.save()

        return JsonResponse({
            "success": True,
            "title": todo.title,
            "description": todo.description
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


# ==============================
# ✅ TOGGLE COMPLETE (AJAX)
# ==============================
@login_required_custom
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user_obj)

    todo.completed = not todo.completed
    todo.save()

    return JsonResponse({
        "success": True,
        "completed": todo.completed
    })


# ==============================
# ❌ DELETE TODO (AJAX)
# ==============================
@login_required_custom
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user_obj)
    todo.delete()

    return JsonResponse({"success": True})