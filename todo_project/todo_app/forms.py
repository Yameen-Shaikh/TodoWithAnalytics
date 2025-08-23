from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, Task, Activity

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'time_of_day', 'due_date']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'time_of_day', 'parent_activity']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ActivityForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['parent_activity'].queryset = Activity.objects.filter(user=user, parent_activity__isnull=True)