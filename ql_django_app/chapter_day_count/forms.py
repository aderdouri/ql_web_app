from django import forms
from datetime import date

class DayCountForm(forms.Form):
    CONVENTION_CHOICES = [
        ('Actual365', 'Actual/365 Fixed'),
        ('Thirty360', 'Thirty/360 (USA)'),
        ('ActualActual', 'Actual/Actual (ISMA)'),
    ]
    
    convention = forms.ChoiceField(label='Day-Count Convention', choices=CONVENTION_CHOICES)
    start_date = forms.DateField(label='Start Date', initial=date(2018, 1, 1), widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', initial=date(2018, 1, 31), widget=forms.DateInput(attrs={'type': 'date'}))