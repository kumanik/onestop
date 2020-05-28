from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms import ModelForm
from .models import *

User = get_user_model()


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=20, label='Username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("User doesn't exist")
            if not user.check_password(password):
                raise forms.ValidationError("Wrong password")


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Enter a username', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'USERNAME'
        self.fields['password'].label = 'PASSWORD'
        self.fields['password1'].label = 'CONFIRM PASSWORD'

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password1',
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError("Passwords must match")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("Username is already taken")
        return super(UserRegisterForm, self).clean(*args, **kwargs)
