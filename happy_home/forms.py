from django import forms
from django.forms import ModelForm
from .models import User, Provider, Consumer, Reply, Review
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm




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
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_provider', 'is_user',)

    def get_provider(self):
        return self.is_provider
    
    def get_user(self):
        return self.is_user
        
class UpdatePasswordForm(PasswordChangeForm):
        class Meta:
            model = User
            fields = ('old_password', 'new_password1', 'new_password2')

        def __init__(self, *args, **kwargs):
            super(UpdatePasswordForm, self).__init__(*args, **kwargs)
         
            self.fields['old_password'].widget.attrs['class'] = 'form-control'
            self.fields['old_password'].label = ''
            self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'
            self.fields['old_password'].help_text = ''
                
            self.fields['new_password1'].widget.attrs['class'] = 'form-control'
            self.fields['new_password1'].label = ''
            self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['new_password1'].help_text = ''

            self.fields['new_password2'].widget.attrs['class'] = 'form-control'
            self.fields['new_password2'].label = ''
            self.fields['new_password2'].widget.attrs['placeholder'] = 'Re-enter Password'
            self.fields['new_password2'].help_text = ''

class UserProfileForm(ModelForm):

    class Meta:
        model = Consumer
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

class BusinessProfileForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}))

    class Meta:
        model = Provider
        fields = ('name', 'poc_first', 'poc_last', 'address', 'city', 'state', 'zip', 'email', 'phone', 'url', 'description', 'cleaning', 'plumbing', 'electrical', 'improvement', 'landscape')


    def __init__(self, *args, **kwargs):
        super(BusinessProfileForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].label = 'Business Name'
        self.fields['name'].widget.attrs['placeholder'] = ''
        self.fields['name'].help_text = ''

        self.fields['poc_first'].widget.attrs['class'] = 'form-control'
        self.fields['poc_first'].label = 'First Name - Point of Contact'
        self.fields['poc_first'].widget.attrs['placeholder'] = ''
        self.fields['poc_first'].help_text = ''

        self.fields['poc_last'].widget.attrs['class'] = 'form-control'
        self.fields['poc_last'].label = 'Last Name - Point of Contact'
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

        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['url'].label = 'Url'
        self.fields['url'].widget.attrs['placeholder'] = ''
        self.fields['url'].help_text = ''

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = '5'
        self.fields['description'].label = 'Tell us about your business'
        self.fields['description'].widget.attrs['placeholder'] = ''
        self.fields['description'].help_text = ''

        self.fields['cleaning'].widget.attrs['class'] = 'form-check-input'
        self.fields['plumbing'].widget.attrs['class'] = 'form-check-input'
        self.fields['electrical'].widget.attrs['class'] = 'form-check-input'
        self.fields['improvement'].widget.attrs['class'] = 'form-check-input'
        self.fields['landscape'].widget.attrs['class'] = 'form-check-input'

class PublicProfileForm(forms.Form):
    class Meta:
        fields = ('name')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'text', 'rating')

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('text',)


class QuoteForm(forms.Form):
    text = forms.CharField(
        widget= forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": "5"
            }
        )
    )
    

