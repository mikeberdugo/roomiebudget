from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from common.models import Roomie , AstradUser



class GuestForm(forms.Form):
    name = forms.CharField(label='Nombre de visitante', max_length=100)
    arrival_date = forms.DateField(label='Fecha llegada', widget=forms.DateInput(attrs={'type': 'date'}))
    departure_date = forms.DateField(label='Fecha salida', widget=forms.DateInput(attrs={'type': 'date'}))
    
    
    def __init__(self, *args, **kwargs):      
        
        # Extraer el id del argumento kwargs si existe
        custom_id = kwargs.pop('custom_id', None)
        super().__init__(*args, **kwargs)
        
        if custom_id is not None:
            user = AstradUser.objects.filter(id=custom_id).first()
            self.fields['roomie'] = forms.ChoiceField(
                choices=[('', '----------')] + [(data.id, data.name) for data in Roomie.objects.filter(user=user)],
                label='Responsable',
            )
        else:
            self.fields['roomie'] = forms.ChoiceField(
                choices=[('', '----------')] + [(data.id, data.name) for data in Roomie.objects.all()],
                label='Responsable',
            )
        
        
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'Filto_Guest'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group mb-0'),
                Column('roomie', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('arrival_date', css_class='form-group mb-0'),
                Column('departure_date', css_class='form-group mb-0'),
                css_class='form-row'
            ),
        )