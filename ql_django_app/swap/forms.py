from django import forms
import QuantLib as ql

class SwapForm(forms.Form):
    FACE_CHOICES = [
        (10000000, '10,000,000'),
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

    notional = forms.ChoiceField(label='Notional', choices=FACE_CHOICES, initial=10_000_000)
    fixed_rate = forms.FloatField(label='Fixed Rate (%)', initial=2.5)
    floating_rate = forms.FloatField(label='Floating Rate (%)', initial=2.0)
    maturity_years = forms.IntegerField(label='Maturity (Years)', initial=10)
    fixed_frequency = forms.ChoiceField(label='Fixed Leg Payment Frequency', 
                                        choices=FREQUENCY_CHOICES, initial='Semiannual')
    floating_frequency = forms.ChoiceField(label='Floating Leg Payment Frequency', 
                                           choices=FREQUENCY_CHOICES, initial='Quarterly')