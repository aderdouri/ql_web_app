from django import forms
import QuantLib as ql

class SwapForm(forms.Form):
    FACE_CHOICES = [
        (1000000, '1,000,000'),
        (500000, '500,000'),
        (100000, '100,000'),
    ]

    FREQUENCY_CHOICES = [
        ('Annual', 'Annual'),
        ('Semiannual', 'Semiannual'),
        ('Quarterly', 'Quarterly'),
        ('Monthly', 'Monthly'),
    ]

    face = forms.ChoiceField(label='Face Value', choices=FACE_CHOICES, initial=1000000)
    fixed_rate = forms.FloatField(label='Fixed Rate (%)', initial=5.0)
    floating_rate = forms.FloatField(label='Floating Rate (%)', initial=5.0)
    maturity_years = forms.IntegerField(label='Maturity (Years)', initial=5)
    fixed_frequency = forms.ChoiceField(label='Fixed Leg Payment Frequency', choices=FREQUENCY_CHOICES, initial='Annual')
    floating_frequency = forms.ChoiceField(label='Floating Leg Payment Frequency', choices=FREQUENCY_CHOICES, initial='Semiannual')