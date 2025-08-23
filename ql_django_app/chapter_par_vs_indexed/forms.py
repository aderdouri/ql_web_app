from django import forms

class ConventionChoiceForm(forms.Form):
    CONVENTION_CHOICES = [
        ('Following', 'Following'),
        ('ModifiedFollowing', 'Modified Following'),
        ('Preceding', 'Preceding'),
        ('Unadjusted', 'Unadjusted'),
    ]
    
    business_day_convention = forms.ChoiceField(
        label='Business Day Convention',
        choices=CONVENTION_CHOICES,
        initial='Following',
        help_text="Select a convention to see how it adjusts coupon dates."
    )