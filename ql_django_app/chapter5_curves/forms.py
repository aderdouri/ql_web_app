from django import forms
import json

class TermStructureForm(forms.Form):
    """Form for Term Structures and their Reference Dates - Essential fields only"""
    
    CURVE_TYPE_CHOICES = [
        ('both', 'Both Curve Types'),
        ('piecewise', 'Relative Date Curve'),
        ('forward', 'Fixed Date Curve'),
    ]
    
    DAY_COUNT_CHOICES = [
        ('Actual360', 'Actual/360 (Standard)'),
        ('Actual365', 'Actual/365 (Full Year)'),
        ('Thirty360', '30/360 (30-Day Month)'),
        ('ActualActual', 'Actual/Actual (Precise)'),
    ]
    
    CALENDAR_CHOICES = [
        ('TARGET', 'TARGET (Europe)'),
        ('UnitedStates', 'United States'),
        ('UnitedKingdom', 'United Kingdom'),
    ]
    
    # Essential fields only
    evaluation_date = forms.DateField(
        label='Evaluation Date',
        initial='2014-10-03',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'title': 'Reference date for all calculations'
        })
    )
    
    curve_type = forms.ChoiceField(
        label='Curve Type',
        choices=CURVE_TYPE_CHOICES,
        initial='both',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': 'Choose the type of curve to build'
        })
    )
    
    day_count = forms.ChoiceField(
        label='Day Count Convention',
        choices=DAY_COUNT_CHOICES,
        initial='Actual360',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': 'Method for calculating days between two dates'
        })
    )
    
    calendar = forms.ChoiceField(
        label='Calendar',
        choices=CALENDAR_CHOICES,
        initial='TARGET',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': 'Calendar to determine business days'
        })
    )
    
    # Market data fields for swap rates (essential for curve building)
    tenor_2y = forms.FloatField(
        label='2Y Rate (%)',
        initial=0.201,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.201',
            'title': 'Swap rate for 2 years'
        })
    )
    
    tenor_3y = forms.FloatField(
        label='3Y Rate (%)',
        initial=0.258,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.258',
            'title': 'Swap rate for 3 years'
        })
    )
    
    tenor_5y = forms.FloatField(
        label='5Y Rate (%)',
        initial=0.464,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '0.464',
            'title': 'Swap rate for 5 years'
        })
    )
    
    tenor_10y = forms.FloatField(
        label='10Y Rate (%)',
        initial=1.151,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '1.151',
            'title': 'Swap rate for 10 years'
        })
    )
    
    tenor_15y = forms.FloatField(
        label='15Y Rate (%)',
        initial=1.588,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': '1.588',
            'title': 'Swap rate for 15 years'
        })
    )
    
    def get_market_data(self):
        """Convert form data to market data format"""
        if self.is_valid():
            return [
                {'tenor_years': 2, 'rate': float(self.cleaned_data.get('tenor_2y', 0.201))},
                {'tenor_years': 3, 'rate': float(self.cleaned_data.get('tenor_3y', 0.258))},
                {'tenor_years': 5, 'rate': float(self.cleaned_data.get('tenor_5y', 0.464))},
                {'tenor_years': 10, 'rate': float(self.cleaned_data.get('tenor_10y', 1.151))},
                {'tenor_years': 15, 'rate': float(self.cleaned_data.get('tenor_15y', 1.588))},
            ]
        return [
            {'tenor_years': 2, 'rate': 0.201},
            {'tenor_years': 3, 'rate': 0.258},
            {'tenor_years': 5, 'rate': 0.464},
            {'tenor_years': 10, 'rate': 1.151},
            {'tenor_years': 15, 'rate': 1.588},
        ]