# interactive_basics/forms.py

from django import forms
import QuantLib as ql

# --- Choices for dropdowns ---

# CORRECTION : Définir la liste des mois manuellement pour éviter les erreurs d'importation
MONTH_CHOICES = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
]

CALENDAR_CHOICES = [
    ('us', 'United States (GovernmentBond)'),
    ('italy', 'Italy'),
    ('joint', 'Joint (US & Italy)')
]
TENOR_CHOICES = [
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('semiannual', 'Semiannual'),
    ('annual', 'Annual')
]
CONVENTION_CHOICES = [
    ('following', 'Following'),
    ('modified_following', 'Modified Following'),
    ('preceding', 'Preceding')
]
DATE_GEN_CHOICES = [
    ('forward', 'Forward'),
    ('backward', 'Backward')
]
DAY_COUNT_CHOICES = [
    ('actual_actual_isda', 'Actual/Actual (ISDA)'),
    ('thirty_360', '30/360'),
    ('actual_360', 'Actual/360')
]
COMPOUND_CHOICES = [
    ('compounded', 'Compounded'),
    ('simple', 'Simple'),
    ('continuous', 'Continuous')
]
FREQUENCY_CHOICES = [
    ('annual', 'Annual'),
    ('semiannual', 'Semiannual'),
    ('quarterly', 'Quarterly'),
    ('monthly', 'Monthly')
]


class QuantLibBasicsForm(forms.Form):
    # --- Module 1: Date Class ---
    date_day = forms.IntegerField(
        label="Day", 
        initial=31, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    date_month = forms.ChoiceField(
        label="Month", 
        choices=MONTH_CHOICES, 
        initial=3, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_year = forms.IntegerField(
        label="Year", 
        initial=2015, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    # --- Module 2: Calendar Class ---
    calendar_start_date = forms.DateField(
        label="Start Date", 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        initial="2015-03-31", 
        required=False
    )
    calendar_period_days = forms.IntegerField(
        label="Period (in days)", 
        initial=60, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    calendar_choice = forms.ChoiceField(
        label="Calendar", 
        choices=CALENDAR_CHOICES, 
        initial='us', 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # --- Module 3: Schedule Class ---
    schedule_effective_date = forms.DateField(
        label="Effective Date", 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        initial="2015-01-01", 
        required=False
    )
    schedule_termination_date = forms.DateField(
        label="Termination Date", 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        initial="2016-01-01", 
        required=False
    )
    schedule_tenor = forms.ChoiceField(
        label="Tenor", 
        choices=TENOR_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    schedule_calendar = forms.ChoiceField(
        label="Calendar", 
        choices=CALENDAR_CHOICES, 
        initial='us', 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    schedule_convention = forms.ChoiceField(
        label="Business Day Convention", 
        choices=CONVENTION_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    schedule_date_generation = forms.ChoiceField(
        label="Date Generation Rule", 
        choices=DATE_GEN_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    schedule_end_of_month = forms.BooleanField(
        label="End of Month", 
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # --- Module 4: InterestRate Class ---
    ir_annual_rate = forms.FloatField(
        label="Annual Rate (e.g., 0.05)", 
        initial=0.05, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    ir_day_count = forms.ChoiceField(
        label="Day Count Convention", 
        choices=DAY_COUNT_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ir_compound_type = forms.ChoiceField(
        label="Compounding Type", 
        choices=COMPOUND_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ir_frequency = forms.ChoiceField(
        label="Frequency", 
        choices=FREQUENCY_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ir_time_years = forms.FloatField(
        label="Time Period (years)", 
        initial=2.0, 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    ir_new_frequency = forms.ChoiceField(
        label="New Frequency (for conversion)", 
        choices=FREQUENCY_CHOICES, 
        initial='semiannual', 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )