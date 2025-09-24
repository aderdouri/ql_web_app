from django import forms
import json

class TermStructureForm(forms.Form):
    """Form for Term Structures and their Reference Dates"""
    
    EVALUATION_DATE_CHOICES = [
        ('2014-10-03', '2014-10-03 (Notebook default)'),
        ('2014-09-19', '2014-09-19 (Alternative)'),
        ('2024-01-01', '2024-01-01'),
    ]
    
    CURVE_TYPE_CHOICES = [
        ('both', 'Both Curves (PiecewiseFlatForward + ForwardCurve)'),
        ('piecewise', 'PiecewiseFlatForward only'),
        ('forward', 'ForwardCurve only'),
    ]
    
    DAY_COUNT_CHOICES = [
        ('Actual360', 'Actual/360 (as in notebook)'),
        ('Actual365', 'Actual/365'),
        ('Thirty360', '30/360'),
        ('ActualActual', 'Actual/Actual'),
    ]
    
    CALENDAR_CHOICES = [
        ('TARGET', 'TARGET (as in notebook)'),
        ('UnitedStates', 'United States'),
        ('UnitedKingdom', 'United Kingdom'),
    ]
    
    evaluation_date = forms.ChoiceField(
        label='Evaluation Date',
        choices=EVALUATION_DATE_CHOICES,
        initial='2014-10-03'
    )
    
    # Market data fields for swap rates
    tenor_2y = forms.FloatField(
        label='2Y Rate (%)',
        initial=0.201,
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'step': '0.001'})
    )
    
    tenor_3y = forms.FloatField(
        label='3Y Rate (%)',
        initial=0.258,
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'step': '0.001'})
    )
    
    tenor_5y = forms.FloatField(
        label='5Y Rate (%)',
        initial=0.464,
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'step': '0.001'})
    )
    
    tenor_10y = forms.FloatField(
        label='10Y Rate (%)',
        initial=1.151,
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'step': '0.001'})
    )
    
    tenor_15y = forms.FloatField(
        label='15Y Rate (%)',
        initial=1.588,
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'step': '0.001'})
    )
    
    # Query parameters
    zero_rate_time = forms.FloatField(
        label='Zero Rate Query - Time (years)',
        initial=5.0,
        required=False,
        min_value=0,
        max_value=30,
        widget=forms.NumberInput(attrs={'step': '0.1', 'value': '5.0'})
    )
    
    zero_rate_date = forms.DateField(
        label='Zero Rate Query - Date',
        initial='2019-09-07',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    # Evaluation date shift
    new_evaluation_date = forms.DateField(
        label='New Evaluation Date (for comparison)',
        initial='2014-09-19',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    curve_type = forms.ChoiceField(
        label='Curve Type',
        choices=CURVE_TYPE_CHOICES,
        initial='both'
    )
    
    day_count = forms.ChoiceField(
        label='Day Count Convention',
        choices=DAY_COUNT_CHOICES,
        initial='Actual360'
    )
    
    calendar = forms.ChoiceField(
        label='Calendar',
        choices=CALENDAR_CHOICES,
        initial='TARGET'
    )
    
    def get_market_data(self):
        """Convert form data to market data format"""
        if self.is_valid():
            return [
                {'tenor_years': 2, 'rate': float(self.cleaned_data.get('tenor_2y', 0.201) or 0.201)},
                {'tenor_years': 3, 'rate': float(self.cleaned_data.get('tenor_3y', 0.258) or 0.258)},
                {'tenor_years': 5, 'rate': float(self.cleaned_data.get('tenor_5y', 0.464) or 0.464)},
                {'tenor_years': 10, 'rate': float(self.cleaned_data.get('tenor_10y', 1.151) or 1.151)},
                {'tenor_years': 15, 'rate': float(self.cleaned_data.get('tenor_15y', 1.588) or 1.588)},
            ]
        return [
            {'tenor_years': 2, 'rate': 0.201},
            {'tenor_years': 3, 'rate': 0.258},
            {'tenor_years': 5, 'rate': 0.464},
            {'tenor_years': 10, 'rate': 1.151},
            {'tenor_years': 15, 'rate': 1.588},
        ]