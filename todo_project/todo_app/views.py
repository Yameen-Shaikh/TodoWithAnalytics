from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CategoryForm, TaskForm, ActivityForm
from .models import Category, Task, Activity, ActivityLog
import json
from datetime import date


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def home_view(request):
    categories = Category.objects.filter(user=request.user)
    backlog_tasks = Task.objects.filter(user=request.user, is_backlog=True)
    today_tasks = Task.objects.filter(user=request.user, due_date=date.today(), is_backlog=False, completed=False)

    today_tasks_grouped = {
        'Morning': [task for task in today_tasks if task.time_of_day == 'Morning'],
        'Afternoon': [task for task in today_tasks if task.time_of_day == 'Afternoon'],
        'Evening': [task for task in today_tasks if task.time_of_day == 'Evening'],
        'Night': [task for task in today_tasks if task.time_of_day == 'Night'],
    }

    activities = Activity.objects.filter(user=request.user, parent_activity__isnull=True)
    activity_logs = ActivityLog.objects.filter(activity__user=request.user)
    
    activity_logs_json = json.dumps([
        {'date': log.date.strftime('%Y-%m-%d'), 'completed': log.completed}
        for log in activity_logs
    ])

    context = {
        'categories': categories,
        'backlog_tasks': backlog_tasks,
        'today_tasks_grouped': today_tasks_grouped,
        'activities': activities,
        'activity_logs': activity_logs,
        'activity_logs_json': activity_logs_json,
        'category_form': CategoryForm(),
        'task_form': TaskForm(),
        'activity_form': ActivityForm(user=request.user),
    }
    return render(request, 'home.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
    return redirect('home')

@login_required
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'update_category.html', {'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    return redirect('home')

@login_required
def add_task(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.category = category
            task.save()
    return redirect('home')

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'update_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('home')



@login_required
def move_to_today(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_backlog = False
    task.due_date = date.today()
    task.save()
    return redirect('home')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('home')

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, user=request.user)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
    return redirect('home')

@login_required
def update_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ActivityForm(instance=activity, user=request.user)
    return render(request, 'update_activity.html', {'form': form})

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    activity.delete()
    return redirect('home')

@login_required
def log_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    log, created = ActivityLog.objects.get_or_create(activity=activity, date=date.today())
    log.completed = not log.completed
    log.save()
    return redirect('home')