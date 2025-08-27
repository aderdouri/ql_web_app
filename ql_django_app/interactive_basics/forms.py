# File: ql_web_app/interactive_basics/forms.py
from django import forms
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

# --- Form for Experience 1: Creating a `ql.Date` object ---
class CreateDateForm(forms.Form):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    # ==============================================================================
    # LA CORRECTION EST ICI : On ajoute une liste de validateurs
    # ==============================================================================
    day = forms.IntegerField(
        label="Day", 
        initial=31, 
        # Cette liste garantit que la valeur est entre 1 et 31
        validators=[MinValueValidator(1), MaxValueValidator(31)] 
    )
    month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES, initial=3)
    year = forms.IntegerField(label="Year", initial=2015)

# --- Form for Experience 2: Date Arithmetic with `ql.Period` ---
class AddPeriodForm(forms.Form):
    start_date = forms.DateField(label="Start Date", initial=date.today(), widget=forms.DateInput(attrs={'type':'date'}))
    quantity = forms.IntegerField(label="Add Quantity", initial=6)
    unit = forms.ChoiceField(label="Unit", choices=[('Days', 'Days'), ('Weeks', 'Weeks'), ('Months', 'Months'), ('Years', 'Years')], initial='Months')

# --- Form for Experience 3: Business Days with `ql.Calendar` ---
class AdvanceBusinessDaysForm(forms.Form):
    start_date_cal = forms.DateField(label="Start Date", initial=date(2015, 3, 31), widget=forms.DateInput(attrs={'type':'date'}))
    period_days = forms.IntegerField(label="Period (in days)", initial=60)
    calendar = forms.ChoiceField(label="Calendar", choices=[('UnitedStates','United States'), ('Italy','Italy'), ('TARGET', 'TARGET (Europe)')])

# --- Form for Experience 4: Creating a `ql.Schedule` ---
class ScheduleForm(forms.Form):
    effective_date = forms.DateField(label="Effective Date", initial=date(2023, 1, 15), widget=forms.DateInput(attrs={'type':'date'}))
    termination_date = forms.DateField(label="Termination Date", initial=date(2025, 1, 15), widget=forms.DateInput(attrs={'type':'date'}))
    tenor = forms.ChoiceField(label="Tenor", choices=[('3M','3 Months'), ('6M','6 Months'), ('1Y','1 Year')])
    calendar_sched = forms.ChoiceField(label="Calendar", choices=[('UnitedStates','United States'), ('TARGET','TARGET (Europe)')])

# --- Form for Experience 5: Creating a `ql.InterestRate` ---
class InterestRateForm(forms.Form):
    rate = forms.FloatField(label="Annual Rate (%)", initial=5.0)
    day_counter = forms.ChoiceField(label="Day Count", choices=[('ActualActual','Actual/Actual (ISDA)'), ('Thirty360','Thirty/360 (Bond Basis)')])
    compounding = forms.ChoiceField(label="Compounding", choices=[('Compounded','Compounded'), ('Simple','Simple')])
    frequency = forms.ChoiceField(label="Frequency", choices=[('Annual','Annual'), ('Semiannual','Semiannual')])