from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class  ListItemForm(forms.Form):
    name = forms.CharField(label='Nombre del Producto ', max_length=255)
    price = forms.DecimalField(label='Precio', max_digits=10, decimal_places=2)
    purchased = forms.BooleanField(label='Comprado', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('price', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('purchased', css_class='form-group mb-0'), 
                css_class='form-row' 
            ),
        )
