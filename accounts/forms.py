from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, 
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm
)
from accounts.models import CustomUser, Address
from django.contrib.auth import authenticate


class SignupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name','class':'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
    username = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))


    class Meta:
        model = CustomUser
        fields = ['name','username','password']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)  # Use Django's authentication
            if user is None:
                raise forms.ValidationError("Invalid email or password.")  
            elif not user.is_active:
                raise forms.ValidationError("Account not found. Please Create New Account")
        return self.cleaned_data

class MagicLinkLoginForm(forms.Form):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("No user found with this email.")
        return username

class AddressForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'
    }))
    
    address = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Full Address',
        'rows': 3,
        'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'
    }))
    
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'
    }))
    
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'State',
        'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'
    }))
    
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'ZIP Code',
        'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6'
    }))

    class Meta:
        model = Address
        fields = ['phone_number', 'address', 'city', 'state', 'zip_code']
        exclude = ['user']

# class PasswordResetForm(BasePasswordResetForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))

#     class Meta:
#         model = CustomUser
#         fields = ['email']

# class PasswordResetConfirmForm(BaseSetPasswordForm):
#     new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'New Password'}))
#     new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

#     class Meta:
#         model = CustomUser
#         fields = ['new_password1','new_password2']  

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email','name']