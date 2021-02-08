from django import forms
from .models import PAYMENT_CHOICES, Cart, Point
from django.forms.widgets import RadioSelect


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['first_name', 'last_name', 'email', 'payment_type', 'point', 'notes']

    my_default_errors = {
        'required': 'This field is required',
        'invalid': 'Enter a valid value'
    }

    first_name = forms.CharField(max_length=100, help_text="Enter First Name",
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               "class": "form-control name"}),
                                 error_messages=my_default_errors)
    last_name = forms.CharField(max_length=150, help_text="Enter Last Name",
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              "class": "form-control name"}),
                                error_messages=my_default_errors)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Your E-Mail',
                                                            "class": "form-control email"}),
                             error_messages=my_default_errors)
    notes = forms.CharField(max_length=500, help_text="Enter Yours Order Notes",
                            widget=forms.TextInput(attrs={'placeholder': 'Note about your order. e.g. special '
                                                                         'note for delivery',
                                                          "class": "form-control notes"}),
                            error_messages=my_default_errors, required=False)
    payment_type = forms.IntegerField(
        widget=forms.RadioSelect(choices=PAYMENT_CHOICES), error_messages=my_default_errors
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['point'] = forms.ModelChoiceField(queryset=Point.objects.all(), empty_label="Select pick-up point",
                                                      error_messages=self.my_default_errors)
