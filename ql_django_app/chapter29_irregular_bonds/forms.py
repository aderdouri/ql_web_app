# irregular_bonds/forms.py (VERSION FINALE CORRIGÉE)

from django import forms
import datetime

class LastCouponGapForm(forms.Form):
    issue_date = forms.DateField(label="Issue Date", initial=datetime.date(2014, 10, 15), widget=forms.DateInput(attrs={'type':'date'}))
    maturity_date = forms.DateField(label="Maturity Date", initial=datetime.date(2024, 10, 15), widget=forms.DateInput(attrs={'type':'date'}))
    coupon_rate = forms.FloatField(label="Coupon Rate (%)", initial=2.0)
    bond_type = forms.ChoiceField(label="Bond Type", choices=[('Fixed', 'Fixed'), ('Floating', 'Floating')])

class FixedToFloaterForm(forms.Form):
    issue_date = forms.DateField(label="Issue Date", initial=datetime.date(2014, 10, 15), widget=forms.DateInput(attrs={'type':'date'}))
    maturity_date = forms.DateField(label="Maturity Date", initial=datetime.date(2024, 10, 15), widget=forms.DateInput(attrs={'type':'date'}))
    fixed_years = forms.IntegerField(label="Number of Fixed-Rate Years", initial=3)
    fixed_rate = forms.FloatField(label="Fixed Coupon Rate (%)", initial=2.0)
    float_spread = forms.FloatField(label="Floating Spread (%)", initial=0.1)

class StubCouponForm(forms.Form):
    # CORRECTION : On utilise la même logique que le livre
    start_date = forms.DateField(label="Start Date", initial=datetime.date(2014, 10, 15), widget=forms.DateInput(attrs={'type':'date'}))
    stub_months = forms.IntegerField(label="Stub Duration (Months)", initial=3)
    total_years = forms.IntegerField(label="Additional Duration (Years)", initial=5)