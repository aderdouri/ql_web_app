from django import forms
import QuantLib as ql

class BondForm(forms.Form):
    face = forms.FloatField(label='Face Value', initial=100)
    coupon_rate = forms.FloatField(label='Coupon Rate (%)', initial=5.0)
    maturity_years = forms.IntegerField(label='Maturity (Years)', initial=5)

    COUPON_FREQUENCY_CHOICES = [
        ('Annual', 'Annual'),
        ('Semiannual', 'Semiannual'),
        ('Quarterly', 'Quarterly'),
        ('Monthly', 'Monthly'),
    ]
        
    coupon_frequency = forms.ChoiceField(label='Coupon Frequency', 
                                           choices=COUPON_FREQUENCY_CHOICES, initial='Quarterly')
            
    yield_rate = forms.FloatField(label='Yield Rate (%)', initial=5.0)