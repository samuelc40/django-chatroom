from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile
from .models import ChatMessage

class UserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'profile_picture']

class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "msger-input", "rows": 1, "placeholder": "Type message here"}))
    class Meta:
        model = ChatMessage
        fields = ["body",]