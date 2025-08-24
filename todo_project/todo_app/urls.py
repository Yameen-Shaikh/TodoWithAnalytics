from django.urls import path
from .views import signup_view, CustomLoginView, home_view, history_view, add_category, update_category, delete_category, add_task, update_task, delete_task, move_to_today, complete_task, add_activity, update_activity, delete_activity, log_activity

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', home_view, name='home'),
    path('history/', history_view, name='history'),
    path('category/add/', add_category, name='add_category'),
    path('category/<int:category_id>/update/', update_category, name='update_category'),
    path('category/<int:category_id>/delete/', delete_category, name='delete_category'),
    path('category/<int:category_id>/add_task/', add_task, name='add_task'),
    path('task/<int:task_id>/update/', update_task, name='update_task'),
    path('task/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('task/<int:task_id>/move_to_today/', move_to_today, name='move_to_today'),
    path('task/<int:task_id>/complete/', complete_task, name='complete_task'),
    path('activity/add/', add_activity, name='add_activity'),
    path('activity/<int:activity_id>/update/', update_activity, name='update_activity'),
    path('activity/<int:activity_id>/delete/', delete_activity, name='delete_activity'),
    path('activity/<int:activity_id>/log/', log_activity, name='log_activity'),
]
