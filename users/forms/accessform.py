from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}), max_length=150)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group mb-0'),
                css_class='row'
            ),
            Row(
                Column('password', css_class='form-group mb-0'),
                css_class='row'
            ),
            Submit('submit', 'Ingresar', css_class='btn btn-light-success w-100')
        )


class SignupForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}), max_length=150)
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group mb-0'),
                css_class='row'
            ),
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
