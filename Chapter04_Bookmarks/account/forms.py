from django import forms
from django.contrib.auth.models import User
from .models import Profile



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())



class UserAccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = ['username','first_name', 'email']


    def clean_password2(self):
        data = self.cleaned_data
    
        if data['password2'] != data['password']:
            raise forms.ValidationError("Passwords don't match!")

        return data['password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError(f"{email} already exists!")
        else:
            return email
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id = self.instance.id).filter(email = email).exists():
            raise forms.ValidationError(f"{email} already exists!")
        else:
            return email


class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={
        'type':'date'
    }))
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']