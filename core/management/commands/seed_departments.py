from django.core.management.base import BaseCommand
from core.models import Department, SubDepartment

class Command(BaseCommand):
    help = 'Seed the departments and sub-departments'

    def handle(self, *args, **kwargs):
        departments = [
            "Finance",
            "Admin",
            "Content",
            "Promotional Marketing",
            "Social Media",
            "HR",
            "IT",
            "Overseas",
            "Production"
        ]

        sub_departments = {
            "Social Media": ["Edit", "Graphics", "Ads", "Shariah Compliance"]
        }

        for dept_name in departments:
            dept, created = Department.objects.get_or_create(name=dept_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created department: {dept_name}"))
            else:
                self.stdout.write(f"Department already exists: {dept_name}")

            if dept_name in sub_departments:
                for sub in sub_departments[dept_name]:
                    sub_dept, sub_created = SubDepartment.objects.get_or_create(department=dept, name=sub)
                    if sub_created:
                        self.stdout.write(self.style.SUCCESS(f"  └─ Created sub-department: {sub}"))
                    else:
                        self.stdout.write(f"  └─ Sub-department already exists: {sub}")
