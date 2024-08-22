from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ServiceForm(forms.Form):
    name = forms.CharField(label='Nombre del Servicio', max_length=100)
    cost = forms.DecimalField(label='Valor a pagar', max_digits=10, decimal_places=2)
    start_date = forms.DateField(label='Fecha inicio corte', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Fecha Fin corte', widget=forms.DateInput(attrs={'type': 'date'}))
    payment_date = forms.DateField(label='Fecha de pago', widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('cost', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='form-group col-md-4 mb-0'),
                Column('end_date', css_class='form-group col-md-4 mb-0'),
                Column('payment_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )