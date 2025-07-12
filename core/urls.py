from django.urls import path
from .views import dashboard_view
from .views import dashboard_view, CustomLoginView, CustomLogoutView
from .views import create_task, edit_task
from . import views

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('task/create/', create_task, name='create_task'),
    path('task/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('kpi/submit/', views.submit_kpi_view, name='submit_kpi'),
    path('tasks/', views.task_list_view, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
]
