from django import forms

class SensitivityForm(forms.Form):
    SHOCK_CHOICES = [
        ('parallel', 'Parallel Shift'),
        ('tilt', 'Tilt / Rotation'),
    ]
    
    shock_type = forms.ChoiceField(label='Shock Type', choices=SHOCK_CHOICES)
    shock_size_bps = forms.FloatField(label='Shock Size (bps)', initial=10.0, help_text="e.g., 10 for a 10 basis point shock.")