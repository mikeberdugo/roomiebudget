from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms

class userboardForm(forms.Form):
    name = forms.CharField(label='Nombre tablero', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre tablero'}))
    description = forms.CharField(label='Descripción', required=True, widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    

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
                css_class='row'
            )
        )
