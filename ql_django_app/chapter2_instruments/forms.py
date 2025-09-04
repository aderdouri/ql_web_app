from django.forms import Form, ChoiceField, FloatField, DateField, DateInput
import datetime

class OptionPricerForm(Form):
    # ... les autres champs ne changent pas ...
    option_type = ChoiceField(choices=[('Call', 'Call'), ('Put', 'Put')], initial='Call', label="Type d'Option")
    strike_price = FloatField(initial=100.0, label="Prix d'Exercice (Strike)")
    
    # ==========================================================
    # CORRECTION PRINCIPALE : Utiliser des dates logiques
    # ==========================================================
    expiry_date = DateField(
        # Mettre une date d'échéance dans le futur
        initial=datetime.date.today() + datetime.timedelta(days=90), 
        widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label="Date d'Échéance"
    )
    
    underlying_price = FloatField(initial=100.0, label="Prix du Sous-jacent")
    risk_free_rate = FloatField(initial=0.01, label="Taux Sans Risque")
    volatility = FloatField(initial=0.20, label="Volatilité")

    evaluation_date = DateField(
        # La date d'évaluation est aujourd'hui
        initial=datetime.date.today(), 
        widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        label="Date d'Évaluation"
    )