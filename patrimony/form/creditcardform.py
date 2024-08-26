from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms

class CreditCardForm(forms.Form):
    
    STATUS_CHOICES = [
        ('', '-----------'),
        ('Active', 'Activa'),
        ('Inactive', 'Inactiva'),
        ('Suspended', 'Suspendida'),
        ('Closed', 'Cerrada'),
    ]

    name = forms.CharField(label='Nombre de la Tarjeta', max_length=100)
    balance = forms.DecimalField(label='Saldo Disponible', max_digits=12, decimal_places=2, initial=0.0)
    credit_limit = forms.DecimalField(label='Límite de Crédito', max_digits=12, decimal_places=2)
    cut_off_date = forms.DateField(label='Fecha de Corte', widget=forms.DateInput(attrs={'type': 'date'}))
    handling_fee = forms.DecimalField(label='Cuota de Manejo', max_digits=10, decimal_places=2, initial=0.0)
    interest_rate = forms.DecimalField(label='Porcentaje de Intereses', max_digits=5, decimal_places=2)
    status = forms.ChoiceField(label='Estado', choices=STATUS_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'form_CreditCard'
        self.fields['status'].widget.attrs.update({
            'data-control': 'select2',
            'data-dropdown-parent': '#kt_modal_credit_card',
            'data-hide-search': 'true',
            'class': 'form-select',
        })
        
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('balance', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('credit_limit', css_class='form-group col-md-6 mb-0'),
                Column('cut_off_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('handling_fee', css_class='form-group col-md-6 mb-0'),
                Column('interest_rate', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )
