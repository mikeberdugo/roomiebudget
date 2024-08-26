from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms

class passivesform(forms.Form):
    
    CURRENCY_CHOICES = [
        ('', '-----------'),
        ('COP', 'Peso Colombiano - COP'),
        ('USD', 'Dólar estadounidense - USD'),
        ('EUR', 'Euro - EUR'),
        ('MXN', 'Peso mexicano - MXN'),
        ('GBP', 'Libra esterlina - GBP'),
        ('JPY', 'Yen japonés - JPY'),
        ('CAD', 'Dólar canadiense - CAD'),
        ('AUD', 'Dólar australiano - AUD'),
        ('CNY', 'Yuan chino - CNY'),
        ('CHF', 'Franco suizo - CHF'),
        ('SEK', 'Corona sueca - SEK'),
        ('NZD', 'Dólar neozelandés - NZD'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('', '-----------'),
        ('Deuda a Banco', 'Deuda a Banco'),
        ('Deuda a Billetera Digital', 'Deuda a Billetera Digital'),
        ('Deuda en Efectivo', 'Deuda en Efectivo'),
        ('Deuda con Proveedores', 'Deuda con Proveedores'),
        ('Deuda a Instituciones Financieras', 'Deuda a Instituciones Financieras'),
        ('Deuda de Hipoteca', 'Deuda de Hipoteca'),
        ('Deuda por Servicios', 'Deuda por Servicios'),
        ('Otro', 'Otro'),
    ]

    STATUS_CHOICES  = [
        ('', '-----------'),
        ('Adeudo', 'Adeudo'),
        ('Cancelado', 'Cancelado'),
    ]
    
    """ 
    STATUS_CHOICES_PASIVOS = [
        ('', '-----------'),
        ('Adeudo', 'Adeudo'),
        ('En deuda', 'En deuda'),
        ('Pago pendiente', 'Pago pendiente'),
        ('Pagado', 'Pagado'),
        ('Cancelado', 'Cancelado'),
    ]
    
    """
    
    
    name = forms.CharField(label='Nombre de Pasivo', max_length=100)
    balance = forms.DecimalField(label='Saldo', max_digits=10, decimal_places=2, initial=0.0)
    currency = forms.ChoiceField(label='Moneda', choices=CURRENCY_CHOICES)
    patrimony_type = forms.ChoiceField(label='Tipo de Pasivo', choices=ACCOUNT_TYPE_CHOICES)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'form_passives'
        self.fields['currency'].widget.attrs.update({
            'data-control': 'select2',
            'data-tags':'true',
            'data-dropdown-parent': '#kt_modal_pasivo',
            'data-hide-search': 'true' ,
            'class': 'form-select',
            
        })
        
        self.fields['patrimony_type'].widget.attrs.update({
            'data-control': 'select2',
            'data-tags':'true',
            'data-dropdown-parent': '#kt_modal_pasivo',
            'data-hide-search': 'true' ,
            'class': 'form-select',
            
        })
        
        
        
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('balance', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('currency', css_class='form-group col-md-6 mb-0'),
                Column('patrimony_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )
        