from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# -----------------------------
# Role Choices
# -----------------------------
ROLE_CHOICES = [
    ('superadmin', 'Super Admin'),
    ('dept_head', 'Department Head'),
    ('team_member', 'Team Member'),
    ('shariah_verifier', 'Shariah Verifier'),
    ('readonly', 'Read Only'),
]

# -----------------------------
# Department Model
# -----------------------------
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# -----------------------------
# SubDepartment Model (Optional)
# -----------------------------
class SubDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sub_departments')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('department', 'name')

    def __str__(self):
        return f"{self.department.name} – {self.name}"

# -----------------------------
# Custom User Model
# -----------------------------
class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    # -----------------------------
# Task Model
# -----------------------------
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# -----------------------------
# KPI Model
# -----------------------------
class KPI(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    metric_name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.metric_name} - {self.department.name} - {self.value}"

# -----------------------------
# File Uploads
# -----------------------------
class UploadedFile(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
