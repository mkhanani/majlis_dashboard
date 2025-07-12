from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, SubDepartment
from .models import Task, KPI, UploadedFile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'role', 'department', 'sub_department', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'department', 'sub_department')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(SubDepartment)
admin.site.register(Task)
admin.site.register(KPI)
admin.site.register(UploadedFile)
