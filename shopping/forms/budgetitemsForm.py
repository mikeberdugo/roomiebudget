from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from common.models import  Patrimony , BudgetCategory

class  budgetitemsForm(forms.Form):
    
    name = forms.CharField(label='Nombre del items ', max_length=255)
    category = forms.ModelChoiceField(label='Categoria', queryset=BudgetCategory.objects.all())
    description = forms.CharField(label='Descripción',required=False,widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'required form-label'}) )
    amount = forms.DecimalField(label='Precio', max_digits=10, decimal_places=2,required=False,initial=0.0)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
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
