from django import forms
from .models import Task, SubDepartment
from .models import KPI

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'department', 'sub_department', 'assigned_to', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class KPIForm(forms.ModelForm):
    class Meta:
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields.values():
                    field.widget.attrs['class'] = 'form-control'
            model = KPI
            fields = ['department', 'metric_name', 'value', 'notes']
            widgets = {
                'notes': forms.Textarea(attrs={'rows': 3}),
                'metric_name': forms.TextInput(attrs={'class': 'form-control'}),
                'value': forms.NumberInput(attrs={'class': 'form-control'}),
         }