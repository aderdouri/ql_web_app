# File: ql_web_app/chapter4_quotes/forms.py
from django import forms

class NelsonSiegelForm(forms.Form):
    """
    A form for the interactive Nelson-Siegel Curve Builder Lab.
    """
    # Parameters for the Nelson-Siegel model
    beta0 = forms.FloatField(
        label="Beta 0 (Level)", 
        initial=0.03,
        help_text="Controls the long-term level of interest rates."
    )
    beta1 = forms.FloatField(
        label="Beta 1 (Slope)", 
        initial=-0.02,
        help_text="Controls the short-term slope of the curve."
    )
    beta2 = forms.FloatField(
        label="Beta 2 (Curvature)", 
        initial=0.01,
        help_text="Controls the medium-term curvature component."
    )
    tau = forms.FloatField(
        label="Tau (Decay Factor)", 
        initial=1.5,
        help_text="Controls how fast the curve decays to the long-term level."
    )
    
    # Parameters for the bond to be priced
    bond_maturity_years = forms.IntegerField(
        label="Bond Maturity (Years)", 
        initial=10,
        min_value=1
    )
    bond_coupon_rate = forms.FloatField(
        label="Bond Coupon Rate (%)", 
        initial=4.0
    )