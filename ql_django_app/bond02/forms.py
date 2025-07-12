# your_app/forms.py

from django import forms

class BondPricingForm(forms.Form):
    # Dictionnaires pour les choix
    FREQ_CHOICES = [
        ('Semiannual', 'Semestrielle'),
        ('Annual', 'Annuelle'),
        ('Quarterly', 'Trimestrielle'),
    ]
    
    DAY_COUNT_CHOICES = [
        ('Thirty360.USA', '30/360 (Bond Basis)'),
        ('ActualActual.ISMA', 'Actual/Actual (ISMA)'),
        ('Actual360', 'Actual/360'),
        ('Actual365Fixed', 'Actual/365 (Fixed)'),
    ]

    # Champs du formulaire
    evaluation_date = forms.DateField(
        label="Date d'évaluation", 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    issue_date = forms.DateField(
        label="Date d'émission", 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    maturity_date = forms.DateField(
        label="Date de maturité", 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    coupon_rate = forms.FloatField(
        label="Taux de coupon (ex: 5 pour 5%)",
        min_value=0
    )
    market_yield = forms.FloatField(
        label="Rendement de marché (ex: 4.5 pour 4.5%)",
        min_value=0
    )
    face_amount = forms.FloatField(
        label="Valeur faciale",
        min_value=0,
        initial=100000
    )
    frequency = forms.ChoiceField(
        label="Fréquence des coupons", 
        choices=FREQ_CHOICES
    )
    day_count_convention = forms.ChoiceField(
        label="Convention de décompte des jours", 
        choices=DAY_COUNT_CHOICES
    )