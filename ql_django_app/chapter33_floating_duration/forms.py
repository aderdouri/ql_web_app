from django import forms
import datetime

class DurationFRNForm(forms.Form):
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2014, 10, 8),
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="Date on which the bond is evaluated (must be between 2014-08-08 and 2019-08-08 for exact book results)"
    )
    forecast_rate = forms.FloatField(
        label="Forecast Rate", 
        initial=0.002,
        help_text="Rate used to forecast future coupon payments"
    )
    yield_rate = forms.FloatField(
        label="Interest Rate", 
        initial=0.002,
        help_text="Bond's interest rate for duration calculation"
    )
    dy = forms.FloatField(
        label="Interest Rate Change", 
        initial=1e-5,
        help_text="Small change in interest rate to test bond sensitivity. Recommended: 1e-05 (0.00001 = 0.001%) for precise calculation, 1e-04 (0.0001 = 0.01%) for standard analysis, or 1e-03 (0.001 = 0.1%) for larger changes."
    )
    
    def clean_evaluation_date(self):
        evaluation_date = self.cleaned_data.get('evaluation_date')
        if evaluation_date:
            # Validation très permissive pour éviter les erreurs
            min_date = datetime.date(2000, 1, 1)
            max_date = datetime.date(2050, 12, 31)
            
            if evaluation_date < min_date:
                raise forms.ValidationError(f"Evaluation date must be after {min_date}.")
            
            if evaluation_date > max_date:
                raise forms.ValidationError(f"Evaluation date must be before {max_date}.")
        
        return evaluation_date
