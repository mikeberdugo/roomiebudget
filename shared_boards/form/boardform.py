from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class BoardForm(forms.Form):
    OPCIONES_CATEGORIA = (
        ('', '----------'),
        ('opcion1', 'Opción 1'),
        ('opcion2', 'Opción 2'),
        ('opcion3', 'Opción 3'),
    )

    name = forms.CharField(label='Nombre tablero', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre tablero'}))
    description = forms.CharField(label='Descripción', required=True, widget=forms.TextInput(attrs={'placeholder': 'Descripción'}))
    categories = forms.ChoiceField(label='Categoría', choices=OPCIONES_CATEGORIA, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group mb-0'),
                css_class='row'
            ),
            Row(
                Column('description', css_class='form-group mb-0'),
                Column('categories', css_class='form-group mb-0'),
                css_class='row'
            ),
            Submit('submit', 'Generar', css_class='btn btn-primary')
        )
