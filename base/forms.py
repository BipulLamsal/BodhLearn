from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Question,Profile

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=75, required=True)
    last_name = forms.CharField(max_length=75, required=True)
    email = forms.CharField(max_length=75, required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ['host']
class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img','cover_img']
    

class UserProfileMain(ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']


