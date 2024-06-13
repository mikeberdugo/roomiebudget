from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ShoppingListForm(forms.Form):
    name = forms.CharField(max_length=255, label='Name')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}), required=False, label='Description')

    def __init__(self, *args, **kwargs):
        super(ShoppingListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )

class ListItemForm(forms.Form):
    name = forms.CharField(max_length=255, label='Name')
    quantity = forms.IntegerField(initial=1, label='Quantity')
    unit_of_measure = forms.CharField(max_length=50, required=False, label='Unit of Measure')
    purchased = forms.BooleanField(initial=False, required=False, label='Purchased')
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Price')

    def __init__(self, *args, **kwargs):
        super(ListItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('quantity', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('unit_of_measure', css_class='form-group col-md-6 mb-0'),
                Column('purchased', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('price', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
