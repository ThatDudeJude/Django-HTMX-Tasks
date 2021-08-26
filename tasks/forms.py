from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "body", "is_priority")        

    def customSave(self, commit=False, creator=None):
        form = self
        if commit:
            task = form.save(commit=False)
            task.creator = creator
            task.save()
        else:
            task = form.save()
        return task
