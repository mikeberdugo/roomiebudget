from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms

class userboardForm(forms.Form):
    email_or_id = forms.CharField(label='Correo electrónico o ID de 7 caracteres', required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Ingrese correo o ID'}))

    def clean_email_or_id(self):
        data = self.cleaned_data['email_or_id']
        
        # Validar si es un correo electrónico
        if '@' in data:
            # Validar el correo electrónico con un regex o simplemente retornar el valor
            return data
        else:
            # Validar si es un ID de 7 caracteres
            if len(data) == 7:
                # Validar que sean caracteres alfanuméricos
                if data.isalnum():
                    return data
                else:
                    raise forms.ValidationError("El ID debe ser alfanumérico.")
            else:
                raise forms.ValidationError("El campo debe ser un correo electrónico o un ID de 7 caracteres.")

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email_or_id', css_class='form-group mb-0'),
                css_class='row'
            ),
            Row(
                Column(Submit('submit', 'Enviar'), css_class='form-group mb-0'),
                css_class='row'
            )
        )