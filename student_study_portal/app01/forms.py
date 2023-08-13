# we have to create a fomr which contains details
# about models


from dataclasses import field, fields
from tkinter import Widget
from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm

# install pip django-crispy-forms library for beautiful forms


class NotesForm(forms.ModelForm):
    # meta me jo model ka form banana hai wo likhe aur jo field
    # chahiye wo bhi likhna hai
    class Meta:
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'desc', 'due', 'is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=200)


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']


class regForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',  'password1', 'password2']
