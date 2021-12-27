from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from main.models import Author 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        # label="Email",
        required=True,
        widget=forms.EmailInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"})    
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email')
 
        widgets = {
                'username': forms.TextInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
                # 'first_name': forms.TextInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
                # 'last_name': forms.TextInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
                # 'email': forms.EmailInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
                # 'username': forms.TextInput(attrs={'class': 'form-control'}),
                # 'email': forms.EmailInput(attrs={'class': 'form-control'}),   
                # 'password1': forms.PasswordInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),   
                # 'password2': forms.PasswordInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),            
            }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
                'first_name': forms.TextInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
                'last_name': forms.TextInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),
                'email': forms.EmailInput(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),          
            }

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Author 
        fields = ['bio', 'profile_pic']

        widgets = {
            # 'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class':"form-control bg-dark text-light", 'style': "border-color: gray;"}),                        
        }


