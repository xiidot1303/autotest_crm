from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from app.models import *
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'address', 'age', 'phone', 'password']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}), 
            'address': forms.TextInput(attrs={"class": "form-control"}), 
            'age': forms.NumberInput(attrs={"class": "form-control"}), 
            'phone': PhoneNumberPrefixWidget(initial='UZ', attrs={"class": "form-control"}),
            'password': forms.PasswordInput(attrs={"class": "form-control"})
        }
    field_order = ['name', 'address', 'age', 'phone', 'password']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'lessons', 'price']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control", "style": "width: 500px; height: 200px;"}),
            'lessons': forms.NumberInput(attrs={"class": "form-control"}),
            'price': forms.NumberInput(attrs={"class": "form-control"}),
        }
    field_order = ['title', 'lessons', 'price', 'description']

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'user', 'specialty', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'user': forms.Select(attrs={"class": "form-control choicesjs"}),
            'specialty': forms.TextInput(attrs={"class": "form-control"}),
            'phone': PhoneNumberPrefixWidget(initial='UZ', attrs={"class": "form-control"})
        }
    field_order = ['name', 'user', 'specialty', 'phone']

class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = ['teacher', 'weekdays', 'title', 'course', 'start_date', 'start_time', 'end_time']
        widgets = {
            # 'students': forms.SelectMultiple(attrs={"class": "form-control"}),
            'teacher': forms.Select(attrs={"class": "form-control choicesjs"}), 
            'weekdays': forms.CheckboxSelectMultiple(attrs={"class": "ml-3"}),
            'title': forms.TextInput(attrs={"class": "form-control"}), 
            'course': forms.Select(attrs={"class": "form-control choicesjs"}), 
            'start_time': forms.TimeInput(attrs={"class": "form-control", "type": "time"}), 
            'end_time': forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            'start_date': forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }

    field_order = ['title', 'course', 'teacher', 'start_date', 'start_time', 'end_time', 'weekdays']

class Adding_student_to_groupForm(forms.Form):
    student = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control choicesjs"}),
        )
    payment_method = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control choicesjs"}), disabled=True
        )
    discount = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class": "form-control", "aria-label": "notification", 
            "aria-describedby": "percent-icon", "value": 0, "max": 100
            }),
        )

class Setting_student_to_groupForm(forms.Form):
    student = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control choicesjs"}),
        )
    discount = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class": "form-control", "aria-label": "notification", 
            "aria-describedby": "percent-icon", "value": 0, "max": 100
            }),
        )
    teacher = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control choicesjs"}),
    )
    course = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control choicesjs"}),
    )

class PayForm(forms.Form):
    # student = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={"class": "form-control choicesjs", "hidden": True}),
    # )
    # group = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={"class": "form-control choicesjs", "hidden": True}),
    # )
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control choicesjs"}),
    )

class UserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    groups = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={"class": "form-control choicesjs"})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "type": "email"}),
        required=False
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False
    )
