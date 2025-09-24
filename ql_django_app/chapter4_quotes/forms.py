from django import forms
from datetime import date
import json

class BondCurveForm(forms.Form):
    """
    Form for bond curve construction with Nelson-Siegel fitting.
    Includes evaluation date, coupon matrix, bond quotes, and advanced options.
    """
    
    # Default coupon data as specified
    DEFAULT_COUPON_DATA = [
        (2, 0.02), (4, 0.0225), (6, 0.025), (8, 0.0275),
        (10, 0.03), (12, 0.0325), (14, 0.035), (16, 0.0375),
        (18, 0.04), (20, 0.0425), (22, 0.045), (24, 0.0475),
        (26, 0.05), (28, 0.0525), (30, 0.055)
    ]
    
    # Evaluation date
    evaluation_date = forms.DateField(
        label='Evaluation Date',
        initial=date(2016, 10, 17),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Reference date for curve construction"
    )
    
    # Coupon matrix as JSON string (will be handled by JavaScript)
    coupon_matrix = forms.CharField(
        label='Coupon Matrix',
        widget=forms.HiddenInput(),
        initial=json.dumps(DEFAULT_COUPON_DATA)
    )
    
    # Bond quotes as JSON string (will be handled by JavaScript)
    bond_quotes = forms.CharField(
        label='Bond Quotes',
        widget=forms.HiddenInput(),
        initial=json.dumps([100.0] * len(DEFAULT_COUPON_DATA))
    )
    
    # Advanced options
    enable_observer = forms.BooleanField(
        label='Enable Observer',
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Automatically recalculate when quotes change"
    )
    
    is_frozen = forms.BooleanField(
        label='Freeze Calculations',
        initial=False,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Prevent automatic recalculation until unfrozen"
    )
    
    def clean_coupon_matrix(self):
        """Validate and parse coupon matrix JSON"""
        data = self.cleaned_data['coupon_matrix']
        try:
            parsed = json.loads(data)
            if not isinstance(parsed, list):
                raise forms.ValidationError("Coupon matrix must be a list")
            for item in parsed:
                if not isinstance(item, (list, tuple)) or len(item) != 2:
                    raise forms.ValidationError("Each coupon item must be [maturity, rate]")
                if not isinstance(item[0], (int, float)) or not isinstance(item[1], (int, float)):
                    raise forms.ValidationError("Maturity and rate must be numbers")
            return parsed
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format for coupon matrix")
    
    def clean_bond_quotes(self):
        """Validate and parse bond quotes JSON"""
        data = self.cleaned_data['bond_quotes']
        try:
            parsed = json.loads(data)
            if not isinstance(parsed, list):
                raise forms.ValidationError("Bond quotes must be a list")
            for quote in parsed:
                if not isinstance(quote, (int, float)):
                    raise forms.ValidationError("All quotes must be numbers")
                if quote <= 0:
                    raise forms.ValidationError("All quotes must be positive")
            return parsed
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format for bond quotes")