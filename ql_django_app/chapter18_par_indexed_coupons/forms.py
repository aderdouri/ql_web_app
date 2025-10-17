from django import forms

class SwapAnalysisForm(forms.Form):
    ANALYSIS_TYPE_CHOICES = [
        ('par_coupons', 'Par Coupons Analysis'),
        ('indexed_coupons', 'Indexed Coupons Analysis'),
        ('comparison', 'Comparison Analysis'),
    ]
    
    analysis_type = forms.ChoiceField(
        choices=ANALYSIS_TYPE_CHOICES,
        required=False,
        initial='comparison',
        label="Analysis Type",
        help_text="Choose the type of coupon analysis to perform",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    notional = forms.FloatField(
        initial=1000000,
        label="Notional Amount",
        help_text="Notional amount for the swap (default: 1,000,000)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1000'})
    )
    
    swap_length = forms.FloatField(
        initial=5.0,
        label="Swap Length (Years)",
        help_text="Length of the swap in years (default: 5 years to see more coupons)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1', 'max': '30'})
    )
    
    evaluation_date = forms.DateField(
        initial='2013-01-07',
        label="Evaluation Date",
        help_text="Date for the analysis (default: January 7, 2013)",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    use_par_coupons = forms.BooleanField(
        required=False,
        initial=True,
        label="Use Par Coupons",
        help_text="Calculate using par coupon method (rate over coupon period)",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    use_indexed_coupons = forms.BooleanField(
        required=False,
        initial=True,
        label="Use Indexed Coupons",
        help_text="Calculate using indexed coupon method (rate over LIBOR tenor)",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

