from django import forms

class InterpolationChoiceForm(forms.Form):
    INTERPOLATION_CHOICES = [
        ('flat_forward', 'Flat Forward (causes glitch)'),
        ('linear_forward', 'Linear Forward (smoother)'),
    ]
    
    interpolation_type = forms.ChoiceField(
        label='Interpolation Method', 
        choices=INTERPOLATION_CHOICES,
        help_text="Select an interpolation to see its effect on the nodes."
    )