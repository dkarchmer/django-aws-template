from captcha.fields import ReCaptchaField

from django import forms as forms
from django.forms import ModelForm

from .models import ContactMessage


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password =  forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':'30'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'size':'20'}))
    password1 =  forms.CharField(widget=forms.PasswordInput)
    password2 =  forms.CharField(widget=forms.PasswordInput)


class ContactPublicForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = ContactMessage
        exclude = ['phone']

    def __init__(self, *args, **kwargs):
        super(ContactPublicForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['class'] = 'custom-form-element custom-textarea'
        self.fields['message'].widget.attrs['size'] = '30'
        self.fields['name'].widget.attrs['class'] = 'custom-form-element custom-input-text'
        self.fields['email'].widget.attrs['class'] = 'custom-form-element custom-input-text'


class ContactPrivateForm(ModelForm):
    class Meta:
        model = ContactMessage
        exclude = ['name', 'phone', 'email']

    def __init__(self, *args, **kwargs):
        super(ContactPrivateForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['class'] = 'custom-form-element custom-textarea'
        self.fields['message'].widget.attrs['size'] = '30'

