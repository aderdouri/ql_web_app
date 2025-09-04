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
    ('us', 'États-Unis (GovernmentBond)'),
    ('italy', 'Italie'),
    ('joint', 'Joint (US & Italie)')
]
TENOR_CHOICES = [
    ('monthly', 'Mensuel'),
    ('quarterly', 'Trimestriel'),
    ('semiannual', 'Semestriel'),
    ('annual', 'Annuel')
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
    ('annual', 'Annuel'),
    ('semiannual', 'Semestriel'),
    ('quarterly', 'Trimestriel'),
    ('monthly', 'Mensuel')
]


class QuantLibBasicsForm(forms.Form):
    # --- Module 1: Date Class ---
    date_day = forms.IntegerField(label="Jour", initial=31, required=False)
    date_month = forms.ChoiceField(label="Mois", choices=MONTH_CHOICES, initial=3, required=False)
    date_year = forms.IntegerField(label="Année", initial=2015, required=False)
    
    # --- Module 2: Calendar Class ---
    calendar_start_date = forms.DateField(label="Date de départ", widget=forms.DateInput(attrs={'type': 'date'}), initial="2015-03-31", required=False)
    calendar_period_days = forms.IntegerField(label="Période (en jours)", initial=60, required=False)
    calendar_choice = forms.ChoiceField(label="Calendrier", choices=CALENDAR_CHOICES, initial='us', required=False)

    # --- Module 3: Schedule Class ---
    schedule_effective_date = forms.DateField(label="Date de début", widget=forms.DateInput(attrs={'type': 'date'}), initial="2015-01-01", required=False)
    schedule_termination_date = forms.DateField(label="Date de fin", widget=forms.DateInput(attrs={'type': 'date'}), initial="2016-01-01", required=False)
    schedule_tenor = forms.ChoiceField(label="Périodicité", choices=TENOR_CHOICES, required=False)
    schedule_calendar = forms.ChoiceField(label="Calendrier", choices=CALENDAR_CHOICES, initial='us', required=False)
    schedule_convention = forms.ChoiceField(label="Convention Jours Ouvrés", choices=CONVENTION_CHOICES, required=False)
    schedule_date_generation = forms.ChoiceField(label="Règle de Génération", choices=DATE_GEN_CHOICES, required=False)
    schedule_end_of_month = forms.BooleanField(label="Fin de mois", required=False)

    # --- Module 4: InterestRate Class ---
    ir_annual_rate = forms.FloatField(label="Taux Annuel (ex: 0.05)", initial=0.05, required=False)
    ir_day_count = forms.ChoiceField(label="Convention de décompte", choices=DAY_COUNT_CHOICES, required=False)
    ir_compound_type = forms.ChoiceField(label="Type de Composition", choices=COMPOUND_CHOICES, required=False)
    ir_frequency = forms.ChoiceField(label="Fréquence", choices=FREQUENCY_CHOICES, required=False)
    ir_time_years = forms.FloatField(label="Durée (en années)", initial=2.0, required=False)
    ir_new_frequency = forms.ChoiceField(label="Nouvelle Fréquence (pour conversion)", choices=FREQUENCY_CHOICES, initial='semiannual', required=False)