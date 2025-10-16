from django import forms
from django.core.exceptions import ValidationError
import datetime
import QuantLib as ql

class DiscountMarginForm(forms.Form):
    # Basic Bond Parameters
    evaluation_date = forms.DateField(
        label="Evaluation Date",
        initial=datetime.date(2014, 10, 8),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Date for bond valuation (format: YYYY-MM-DD). Must be a business day in TARGET calendar."
    )
    issue_date = forms.DateField(
        label="Issue Date",
        initial=datetime.date(2014, 10, 7),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Date when the bond was issued (must be before evaluation date)"
    )
    maturity_date = forms.DateField(
        label="Maturity Date",
        initial=datetime.date(2024, 10, 13),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Date when the bond matures"
    )
    face_amount = forms.FloatField(
        label="Face Amount",
        initial=100.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="Principal amount of the bond (e.g., 100.0)"
    )
    forecast_rate = forms.FloatField(
        label="Forecast Rate (Euribor)",
        initial=0.002,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
        help_text="Base interest rate for forecasting (e.g., 0.002 = 0.2%)"
    )

    # Target Price and Solver Parameters
    target_price = forms.FloatField(
        label="Target Bond Price",
        initial=99.6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        help_text="The bond price for which to calculate the discount margin"
    )
    solver_accuracy = forms.ChoiceField(
        label="Calculation Precision",
        choices=[
            ('1e-6', 'Standard (1e-6) - Fast calculation'),
            ('1e-8', 'High (1e-8) - Recommended for most cases'),
            ('1e-10', 'Very High (1e-10) - Maximum precision, slower'),
        ],
        initial='1e-8',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose calculation precision: Standard for quick results, High for accuracy, Very High for maximum precision"
    )
    margin_range = forms.ChoiceField(
        label="Expected Margin Range",
        choices=[
            ('conservative', 'Conservative (-1% to +2%) - For high-quality bonds'),
            ('moderate', 'Moderate (-2% to +5%) - For typical corporate bonds'),
            ('wide', 'Wide (-5% to +10%) - For distressed or high-risk bonds'),
            ('custom', 'Custom Range - Specify your own bounds'),
        ],
        initial='moderate',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the expected range for discount margin based on bond quality and market conditions"
    )
    min_margin = forms.FloatField(
        label="Minimum Margin (%)",
        initial=-0.02,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '-0.1', 'max': '0.1'}),
        help_text="Minimum expected discount margin in percentage (e.g., -2.0 for -2%)",
        required=False
    )
    max_margin = forms.FloatField(
        label="Maximum Margin (%)",
        initial=0.05,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'max': '0.2'}),
        help_text="Maximum expected discount margin in percentage (e.g., 5.0 for 5%)",
        required=False
    )
    
    def clean_evaluation_date(self):
        eval_date = self.cleaned_data.get('evaluation_date')
        if eval_date:
            # Vérifier que la date d'évaluation est un jour ouvrable TARGET
            ql_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
            target_calendar = ql.TARGET()
            if not target_calendar.isBusinessDay(ql_date):
                # Trouver le prochain jour ouvrable
                next_business_day = target_calendar.adjust(ql_date, ql.Following)
                next_business_day_str = next_business_day.ISO()
                
                raise ValidationError(
                    f"The selected evaluation date ({eval_date}) falls on a holiday or weekend. "
                    f"Please select a business day such as {next_business_day_str} or any other weekday "
                    f"(Monday through Friday) that is not a TARGET calendar holiday."
                )
        return eval_date
    
    def clean(self):
        cleaned_data = super().clean()
        margin_range = cleaned_data.get('margin_range')
        min_margin = cleaned_data.get('min_margin')
        max_margin = cleaned_data.get('max_margin')
        eval_date = cleaned_data.get('evaluation_date')
        issue_date = cleaned_data.get('issue_date')
        
        # Gestion des choix prédéfinis pour les marges
        if margin_range and margin_range != 'custom':
            if margin_range == 'conservative':
                cleaned_data['min_margin'] = -0.01  # -1%
                cleaned_data['max_margin'] = 0.02   # +2%
            elif margin_range == 'moderate':
                cleaned_data['min_margin'] = -0.02  # -2%
                cleaned_data['max_margin'] = 0.05   # +5%
            elif margin_range == 'wide':
                cleaned_data['min_margin'] = -0.05  # -5%
                cleaned_data['max_margin'] = 0.10   # +10%
        
        # Mise à jour des valeurs après traitement des choix prédéfinis
        min_margin = cleaned_data.get('min_margin')
        max_margin = cleaned_data.get('max_margin')
        
        # Validation des bornes min/max
        if min_margin is not None and max_margin is not None:
            if min_margin >= max_margin:
                raise ValidationError(
                    f"Invalid margin bounds: The minimum margin ({min_margin:.2f}%) must be strictly less than "
                    f"the maximum margin ({max_margin:.2f}%). Please adjust the values to create a valid search range."
                )
        
        # Validation des dates
        if eval_date and issue_date:
            if issue_date >= eval_date:
                raise ValidationError(
                    f"Invalid date sequence: The issue date ({issue_date}) must be before the evaluation date ({eval_date}). "
                    f"Please ensure the bond was issued before the valuation date."
                )
        
        return cleaned_data