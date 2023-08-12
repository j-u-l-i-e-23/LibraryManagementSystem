
from django import forms
from . import models
from django.forms import ModelForm
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .models import Book,Student,IssuedBook
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Bookform(forms.ModelForm):
    class Meta:
        model=Book
        fields='__all__'
        
class Studentform(forms.ModelForm):
    class Meta:
        model=Student
        fields='__all__'

class IssueBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name [ISBN] [id]", to_field_name="isbn", label="Book (Name and ISBN)")
    name2 = forms.ModelChoiceField(queryset=models.Student.objects.all(), empty_label="Name [Branch] [Class] [Roll No]", to_field_name="user", label="Student Details")
    
    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})
