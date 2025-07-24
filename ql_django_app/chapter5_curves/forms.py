# Fichier : ql_web_app/chapter5_curves/forms.py (VERSION FINALE AVEC VALIDATION)

from django import forms
from datetime import date

class CurveBuilderForm(forms.Form):
    evaluation_dt = forms.DateField(
        label='Evaluation Date', 
        initial=date(2014, 10, 3),
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Change this date to see how a relative curve moves."
    )

    # ==============================================================================
    # LA CORRECTION EST ICI : On ajoute une fonction de validation personnalisée
    # ==============================================================================
    def clean_evaluation_dt(self):
        """
        Custom validation for the evaluation_dt field.
        """
        # On récupère la date que l'utilisateur a saisie
        dt = self.cleaned_data.get('evaluation_dt')

        # On vérifie si la date est dans la plage valide pour QuantLib
        if dt:
            if not (1901 <= dt.year <= 2199):
                # Si l'année est hors limites, on lève une erreur de validation
                raise forms.ValidationError(
                    "Year is out of QuantLib's valid range. Please choose a year between 1901 and 2199."
                )
        
        # Si la date est valide, on la retourne
        return dt