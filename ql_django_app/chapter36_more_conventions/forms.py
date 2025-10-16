# short_coupon_glitch/forms.py (VERSION FINALE ET COMPLÈTE)

from django import forms
import datetime

class ShortCouponForm(forms.Form):
    # On inclut tous les paramètres du livre
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2011, 1, 27),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Date on which the bond pricing analysis is performed"
    )
    
    issue_date = forms.DateField(
        label="Issue Date", 
        initial=datetime.date(2011, 1, 28),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Date when the bond is issued (affects first coupon period)"
    )

    maturity_date = forms.DateField(
        label="Maturity Date", 
        initial=datetime.date(2020, 8, 31),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Date when the bond matures and principal is repaid"
    )

    coupon_rate = forms.FloatField(
        label="Coupon Rate", 
        initial=0.03625,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
        help_text="Annual coupon rate as decimal (3.625% = 0.03625)"
    )

    bond_yield = forms.FloatField(
        label="Bond Yield", 
        initial=0.034921,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
        help_text="Yield to maturity for pricing (3.4921% = 0.034921)"
    )
    
    face_amount = forms.FloatField(
        label="Face Amount", 
        initial=100.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Principal amount of the bond"
    )
