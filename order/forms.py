from django.forms import ModelForm
from order.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state',
                  'city', 'order_note']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field != 'address_line_2' and field != 'order_note':
                self.fields[field].widget.attrs['required'] = True
            if field == 'order_note':
                self.fields[field].widget.attrs['rows'] = 5
