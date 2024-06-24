from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class AccountForm(forms.Form):
    CURRENCY_CHOICES = [
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
        ('Cuenta Corriente', 'Cuenta Corriente'),
        ('Cuenta de Ahorros', 'Cuenta de Ahorros'),
        ('Tarjeta de Crédito', 'Tarjeta de Crédito'),
        ('Billetera digital', 'Billetera digital'),
        ('Efectivo', 'Efectivo'),
        ('Otro', 'Otro'),
    ]

    STATUS_CHOICES = [
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Cerrada', 'Cerrada'),
        ('Bloqueada', 'Bloqueada'),
    ]

    name = forms.CharField(label='Nombre de la cuenta', max_length=100)
    balance = forms.DecimalField(label='Saldo', max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(label='Moneda', choices=CURRENCY_CHOICES)
    account_type = forms.ChoiceField(label='Tipo de cuenta', choices=ACCOUNT_TYPE_CHOICES)
    status = forms.ChoiceField(label='Estado', choices=STATUS_CHOICES)
    #board = forms.ModelChoiceField(queryset=Board.objects.all(), label='Tablero asociado')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('balance', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('currency', css_class='form-group col-md-6 mb-0'),
                Column('account_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('board', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar')
        )
