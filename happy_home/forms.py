from django import forms
from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm




class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_provider', 'is_user',)
"""
class RegisterUserForm(UserCreationForm):
    # adding other User fields 
    # email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'is_provider', 'is_user' )

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = ''
        self.fields['first_name'].required = False
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].help_text = ''

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].label = ''
        self.fields['last_name'].required = False
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].help_text = ''

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].help_text = ''
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].help_text = '<small>Your password must contain at least 8 characters</small>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter Password'
        self.fields['password2'].help_text = ''

        self.fields['is_provider'].widget.attrs['class'] = 'form-control'
        self.fields['is_provider'].label = 'provider'
        self.fields['is_provider'].help_text = ''

        self.fields['is_user'].widget.attrs['class'] = 'form-control'
        self.fields['is_user'].label = 'user'
        self.fields['is_user'].help_text = ''

"""
"""       
class EditProfileForm(UserChangeForm):
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'type': 'hidden'})) # hides link django puts on page

    class Meta:
        model = User
        # exclude = (list exclusions) instead of fields = ()
        fields = ('username', 'first_name', 'last_name', 'email', 'password',) # must have password

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].help_text = ''

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        #self.fields['first_name'].help_text = '<small>Your password must contain at least 8 characters</small>'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        #self.fields['last_name'].help_text = '<small>Your password must contain at least 8 characters</small>'
""" 

"""
class UserProfileForm(ModelForm):
    class Meta:
        model = SiteUser
        fields = ('first', 'last', 'address', 'city', 'state', 'zip', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['first'].widget.attrs['class'] = 'form-control'
        self.fields['first'].label = 'First Name'
        self.fields['first'].widget.attrs['placeholder'] = ''
        self.fields['first'].help_text = ''

        self.fields['last'].widget.attrs['class'] = 'form-control'
        self.fields['last'].label = 'Last Name'
        self.fields['last'].widget.attrs['placeholder'] = ''
        self.fields['last'].help_text = ''

        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['address'].label = 'Address'
        self.fields['address'].widget.attrs['placeholder'] = ''
        self.fields['address'].help_text = ''

        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].label = 'City'
        self.fields['city'].widget.attrs['placeholder'] = ''
        self.fields['city'].help_text = ''

        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['state'].label = 'State'
        self.fields['state'].widget.attrs['placeholder'] = ''
        self.fields['state'].help_text = ''

        self.fields['zip'].widget.attrs['class'] = 'form-control'
        self.fields['zip'].label = 'Zip Code'
        self.fields['zip'].widget.attrs['placeholder'] = ''
        self.fields['zip'].help_text = ''

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['email'].label = 'Email Address'
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['email'].help_text = ''

        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['type'] = 'tel'
        self.fields['phone'].label = 'Phone'
        self.fields['phone'].widget.attrs['placeholder'] = ''
        self.fields['phone'].help_text = ''
"""

"""
class BusinessProfileForm(ModelForm):
    class Meta:
        model = Provider
        fields = ('name', 'poc_first', 'poc_last', 'address', 'city', 'state', 'zip', 'email', 'phone', 'description', 'url')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].label = 'First Name'
        self.fields['name'].widget.attrs['placeholder'] = ''
        self.fields['name'].help_text = ''
        
        self.fields['poc_first'].widget.attrs['class'] = 'form-control'
        self.fields['poc_first'].label = 'First Name'
        self.fields['poc_first'].widget.attrs['placeholder'] = ''
        self.fields['poc_first'].help_text = ''

        self.fields['poc_last'].widget.attrs['class'] = 'form-control'
        self.fields['poc_last'].label = 'Last Name'
        self.fields['poc_last'].widget.attrs['placeholder'] = ''
        self.fields['poc_last'].help_text = ''

        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['address'].label = 'Address'
        self.fields['address'].widget.attrs['placeholder'] = ''
        self.fields['address'].help_text = ''

        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].label = 'City'
        self.fields['city'].widget.attrs['placeholder'] = ''
        self.fields['city'].help_text = ''

        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['state'].label = 'State'
        self.fields['state'].widget.attrs['placeholder'] = ''
        self.fields['state'].help_text = ''

        self.fields['zip'].widget.attrs['class'] = 'form-control'
        self.fields['zip'].label = 'Zip Code'
        self.fields['zip'].widget.attrs['placeholder'] = ''
        self.fields['zip'].help_text = ''

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['email'].label = 'Email Address'
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['email'].help_text = ''

        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['type'] = 'tel'
        self.fields['phone'].label = 'Phone'
        self.fields['phone'].widget.attrs['placeholder'] = ''
        self.fields['phone'].help_text = ''

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].label = 'Description'
        self.fields['description'].widget.attrs['placeholder'] = ''
        self.fields['description'].help_text = ''

        self.fields['url'].widget.attrs['class'] = 'form-control-lg'
        self.fields['phone'].widget.attrs['type'] = 'tel'
        self.fields['url'].label = 'Website URL'
        self.fields['url'].widget.attrs['placeholder'] = ''
        self.fields['url'].help_text = ''
"""