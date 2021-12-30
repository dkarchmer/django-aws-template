import pytz
from captcha.fields import ReCaptchaField

from django import forms as forms
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit

from .models import Account


class TimeZoneFormField(forms.TypedChoiceField):
    def __init__(self, *args, **kwargs):

        def coerce_to_pytz(val):
            try:
                return pytz.timezone(val)
            except pytz.UnknownTimeZoneError:
                raise ValidationError("Unknown time zone: '%s'" % val)

        defaults = {
            'coerce': coerce_to_pytz,
            'choices': [(tz, tz) for tz in pytz.common_timezones],
            'empty_value': None,
        }
        defaults.update(kwargs)
        super(TimeZoneFormField, self).__init__(*args, **defaults)


class AccountUpdateForm(ModelForm):
    time_zone = TimeZoneFormField()
    class Meta:
        model = Account
        fields = ['username', 'name', 'tagline']

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['username'].widget.attrs['class'] = 'custom-form-element custom-input-text'
        self.fields['name'].widget.attrs['class'] = 'custom-form-element custom-input-text'
        self.fields['tagline'].widget.attrs['class'] = 'custom-form-element custom-input-text'
        tz = settings.TIME_ZONE
        if 'instance' in kwargs:
            user = kwargs['instance']
            if user and user.time_zone:
                tz = user.time_zone
        self.initial['time_zone'] = tz
        self.fields['time_zone'].widget.attrs['class'] = 'custom-form-element custom-select'


class AllauthSignupForm(SignupForm):
    """Base form for django-allauth to use, adding a ReCaptcha function"""

    # captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(AllauthSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up', css_class='btn btn-lg btn-success btn-block'))


class AllauthLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(AllauthLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign In', css_class='btn btn-lg btn-success btn-block'))


class AdminUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'email', 'name', 'is_staff', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AdminUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'name', 'is_active', 'is_staff', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]