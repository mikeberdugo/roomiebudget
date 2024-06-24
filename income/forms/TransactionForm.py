from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from common.models import Account, Labels


class TransactionForm(forms.Form):
    TIPO_CHOICES = [
        ('ingreso', 'Entrante'),
        ('egreso', 'Saliente')
    ]
    
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de Crédito', 'Tarjeta de Crédito'),
        ('Transferencia Bancaria', 'Transferencia Bancaria'),
        ('PayPal', 'PayPal'),
        ('Criptomoneda', 'Criptomoneda'),
        ('Cheque', 'Cheque'),
        ('Otro', 'Otro')
    ]
    
    ESTADO_CHOICES =[
        ('0', 'Programada'),
        ('1', 'Pagada'),
        ('2', 'En Espera'),
        ('3', 'Realizada'),
    ]

    ETIQUETAS_CHOICES = [
        ('1', 'Pago de Deuda'),
        ('2', 'Sueldo o Salario'),
        ('3', 'Retiro por Fiesta'),
        ('4', 'Alquiler o Hipoteca'),
        ('5', 'Compras'),
        ('6', 'Facturas de Servicios'),
        ('7', 'Transporte'),
        ('8', 'Ocio y Entretenimiento'),
        ('9', 'Educación'),
        ('10', 'Salud'),
        ('11', 'Ahorros e Inversiones'),
        ('12', 'Impuestos'),
    ]

    
    typet = forms.ChoiceField(label='Tipo de transacción', choices=TIPO_CHOICES)
    Account = forms.ModelChoiceField(label='Cuenta', queryset=Account.objects.all())
    status = forms.ChoiceField(label='Estado', choices=ESTADO_CHOICES)
    date = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'type': 'date'}))
    amount = forms.DecimalField(label='Monto', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'id': 'amount-input'}))
    description = forms.CharField(label='Descripción', required=False, widget=forms.Textarea(attrs={'rows': 3}))
    payment_method = forms.ChoiceField(label='Método de pago', choices=METODO_PAGO_CHOICES)
    addressee_sender = forms.CharField(label='Destinatario/Remitente', max_length=100)
    labels = forms.ChoiceField(label='Etiquetas', choices=ETIQUETAS_CHOICES,required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('typet', css_class='form-group col-md-6 mb-0'),
                Column('Account', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('amount', css_class='form-group col-md-6 mb-0'),
                Column('payment_method', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('labels', css_class='form-group col-md-6 mb-0'),
                Column('addressee_sender', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )
        
        