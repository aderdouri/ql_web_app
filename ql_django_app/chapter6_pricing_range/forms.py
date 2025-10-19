from django import forms
import datetime

class PriceHistoryForm(forms.Form):
    start_date = forms.DateField(
        label="Simulation Start Date", 
        initial=datetime.date(2017, 5, 1),  # 1er mai 2017 (bien avant la fin)
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'style': 'border-radius: 8px; border: 2px solid #e9ecef;'
        })
    )
    end_date = forms.DateField(
        label="Simulation End Date", 
        initial=datetime.date(2018, 5, 9),  # 9 mai 2018 (comme dans le livre)
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'style': 'border-radius: 8px; border: 2px solid #e9ecef;'
        })
    )
    
    simulation_method = forms.ChoiceField(
        label="Simulation Method",
        choices=[
            ('rebuild_curve', 'Rebuild Curve (Slower)'),
            ('update_quotes', 'Update Quotes (Faster)'),
        ],
        initial='rebuild_curve',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'border-radius: 8px; border: 2px solid #e9ecef;'
        })
    )

    noise_level = forms.FloatField(
        label="Market Noise Level (Scale)",
        initial=0.005,  # Exactement comme dans le livre: scale=0.005
        help_text="Controls the randomness of daily rate changes (book default: 0.005).",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'min': '0',
            'max': '0.1',
            'style': 'border-radius: 8px; border: 2px solid #e9ecef;'
        })
    )