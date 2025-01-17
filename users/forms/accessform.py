from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    email = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Email')}),
        max_length=150
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group mb-0'),
                css_class='row'
            ),
            Row(
                Column('password', css_class='form-group mb-0'),
                css_class='row'
            ),
            Submit('submit', _('Login2'), css_class='btn btn-light-success w-100')
        )


class SignupForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group mb-0'),
                css_class='row'
            ),
            Row(
                Column('password1', css_class='form-group mb-0'),
                css_class='row'
            ),
            Row(
                Column('password2', css_class='form-group mb-0'),
                css_class='row'
            ),
            
            Submit('submit', 'Registrarse', css_class='btn btn-light-success w-100')
        )
