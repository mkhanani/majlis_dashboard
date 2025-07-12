from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import KPI, Task, UploadedFile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from .forms import KPIForm
from .models import KPI

@login_required
def dashboard_view(request):
    user = request.user

    # Filter based on role
    if user.role == 'superadmin':
        kpis = KPI.objects.all()
        tasks = Task.objects.all()
        files = UploadedFile.objects.all()
    else:
        kpis = KPI.objects.filter(department=user.department)
        tasks = Task.objects.filter(department=user.department)
        files = UploadedFile.objects.filter(department=user.department)

    context = {
        'kpi_count': kpis.count(),
        'task_count': tasks.count(),
        'file_count': files.count(),

        # 🔁 FIXED: Use actual field names that exist in your models
        'recent_kpis': kpis.order_by('-date')[:5],
        'recent_tasks': tasks.order_by('-created_at')[:5],  # Assuming Task has created_at
        'recent_files': files.order_by('-uploaded_at')[:5],  # Assuming UploadedFile has uploaded_at
    }

    return render(request, 'core/dashboard.html', context)

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

def is_admin_or_head(user):
    return user.role in ['superadmin', 'dept_head']

@login_required
@user_passes_test(is_admin_or_head)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'core/create_task.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_head)
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'core/create_task.html', {'form': form})

@login_required
def submit_kpi_view(request):
    if request.method == 'POST':
        form = KPIForm(request.POST)
        if form.is_valid():
            kpi = form.save(commit=False)
            kpi.submitted_by = request.user
            kpi.department = request.user.department  # auto-assign
            kpi.save()
            return redirect('dashboard')
    else:
        form = KPIForm()

    return render(request, 'core/submit_kpi.html', {'form': form})

@login_required
def task_list_view(request):
    user = request.user

    if user.role == 'superadmin':
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(department=user.department)

    return render(request, 'core/task_list.html', {'tasks': tasks})

