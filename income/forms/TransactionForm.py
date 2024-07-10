from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from common.models import Patrimony , Category


class TransactionForm(forms.Form):
    TIPO_CHOICES = [
        ('', '-----------'),
        ('ingreso', 'Entrante'),
        ('egreso', 'Saliente')
    ]
    
    METODO_PAGO_CHOICES = [
        ('', '-----------'),
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de Crédito', 'Tarjeta de Crédito'),
        ('Transferencia Bancaria', 'Transferencia Bancaria'),
        ('PayPal', 'PayPal'),
        ('Criptomoneda', 'Criptomoneda'),
        ('Cheque', 'Cheque'),
        ('Otro', 'Otro')
    ]
    
    ESTADO_CHOICES =[
        ('', '-----------'),
        ('0', 'Programada'),
        ('1', 'Pagada'),
        ('2', 'En Espera'),
    ]
    

    ## choice temporal remplazar 
    ADDRESSEE_SENDER_CHOICES = [
        ('', '-----------'),
        ('mi', 'Mi'),
        ('nomina', 'Nómina'),
        ('tarjeta', 'Tarjeta'),
        ('seguro', 'Seguro'),
        ('amigo', 'Amigo'),
        ('jefe', 'Jefe'),
        ('familia', 'Familia'),
        ('proveedor', 'Proveedor'),
        ('colega', 'Colega'),
        ('cliente', 'Cliente'),
    ]
    
    
    

    typet = forms.ChoiceField(label='Tipo de transacción', choices=TIPO_CHOICES)
    patrimony = forms.ModelChoiceField(label='Patrimonio', queryset=Patrimony.objects.all())
    status = forms.ChoiceField(label='Estado', choices=ESTADO_CHOICES)
    date = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'type': 'date'}))
    amount = forms.DecimalField(label='Monto', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'id': 'amount-input'}))
    description = forms.CharField(label='Descripción',widget=forms.Textarea(attrs={'rows': 3}))
    payment_method = forms.ChoiceField(label='Método de pago', choices=METODO_PAGO_CHOICES)
    #addressee_sender = forms.CharField(label='Destinatario/Remitente', max_length=100)
    addressee = forms.ChoiceField(label='Destinatario',choices=ADDRESSEE_SENDER_CHOICES )
    sender = forms.ChoiceField(label='Remitente', choices=ADDRESSEE_SENDER_CHOICES)
    category = forms.ModelChoiceField(label='Categorias', queryset=Category.objects.all())

    tex1 = forms.CharField(label='->', max_length=100, required=False,widget=forms.TextInput(attrs={'placeholder': 'De'}) )
    #tex1 = forms.CharField(label='->', widget=forms.TextInput(attrs={'placeholder': '->'}), max_length=150)
    tex2 = forms.CharField(label='->', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Para'}))
    def __init__(self, *args,slug=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tex1'].widget.attrs['disabled'] = True
        self.fields['tex2'].widget.attrs['disabled'] = True
        
        if slug:
            self.fields['patrimony'].queryset = Patrimony.objects.filter(board__slug=slug)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('typet', css_class='form-group col-md-6 mb-0'),
                Column('patrimony', css_class='form-group col-md-6 mb-0'),
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
                Column('tex1', css_class='form-group col-md-2 mb-0'),
                Column('addressee', css_class='form-group col-md-4 mb-0'),
                Column('tex2', css_class='form-group col-md-2 mb-0'),
                Column('sender', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            
        )
        
        