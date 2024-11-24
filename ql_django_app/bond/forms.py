from django import forms
import QuantLib as ql

class BondForm(forms.Form):
    face = forms.FloatField(label='Face Value', initial=1000)
    coupon_rate = forms.FloatField(label='Coupon Rate (%)', initial=5.0)
    maturity_years = forms.IntegerField(label='Maturity (Years)', initial=5)
    frequency = forms.ChoiceField(label='Coupon Frequency',
                                  choices=[(ql.Annual, 'Annual'),
                                           (ql.Semiannual, 'Semiannual'),
                                           (ql.Quarterly, 'Quarterly')])
    yield_rate = forms.FloatField(label='Yield Rate (%)', initial=5.0)