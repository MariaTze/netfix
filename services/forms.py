from django import forms
from .models import Service


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_per_hour = forms.DecimalField(
        decimal_places=2, max_digits=7, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Set field choices based on company type
        if company:
            if company.field_of_work == "All in One":
                # All fields except "All in One"
                self.fields['field'].choices = [
                    (c[0], c[1]) for c in Service.FIELD_CHOICES
                ]
            else:
                self.fields['field'].choices = [
                    (company.field_of_work, company.field_of_work)
                ]
        # placeholders
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_per_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['name'].widget.attrs['autocomplete'] = 'on'


class RequestServiceForm(forms.Form):
    address = forms.CharField(max_length=255, label='Service Address')
    hours = forms.IntegerField(min_value=1, label='Service Duration (hours)')


class RateServiceForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Rate this service"
    )
