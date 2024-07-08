from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class budgetForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'required form-label'})
    )
    description = forms.CharField(
        label='Descripción',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'required form-label'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group  mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group  mb-0'), 
                css_class='form-row' 
            ),
        )
