from django import forms

class FixedRateBondForm(forms.Form):
    # Basic Bond Parameters (from the chapter example)
    face_value = forms.FloatField(
        label='Face Value (Par Value)',
        initial=100.0,
        min_value=1.0,
        max_value=10000.0,
        help_text='The principal amount of the bond that will be repaid at maturity.',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    coupon_rate = forms.FloatField(
        label='Coupon Rate (%)',
        initial=6.0,
        min_value=0.0,
        max_value=50.0,
        help_text='The annual interest rate paid by the bond, expressed as a percentage.',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    issue_date = forms.DateField(
        label='Issue Date',
        initial='2015-01-15',
        help_text='The date when the bond is issued and starts earning interest.',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    maturity_date = forms.DateField(
        label='Maturity Date',
        initial='2016-01-15',
        help_text='The date when the bond matures and the principal is repaid.',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # Yield Curve Parameters
    spot_rate_6m = forms.FloatField(
        label='6-Month Spot Rate (%)',
        initial=0.5,
        min_value=0.0,
        max_value=20.0,
        help_text='The annualized interest rate for 6-month treasury bonds. Used to discount the first coupon payment.',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    spot_rate_1y = forms.FloatField(
        label='1-Year Spot Rate (%)',
        initial=0.7,
        min_value=0.0,
        max_value=20.0,
        help_text='The annualized interest rate for 1-year treasury bonds. Used to discount the final payment (principal + coupon).',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    # Advanced Parameters (from QuantLib implementation)
    settlement_days = forms.IntegerField(
        label='Settlement Days',
        initial=0,
        min_value=0,
        max_value=10,
        help_text='Number of business days between trade date and settlement date.',
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Day Count Convention
    DAY_COUNT_CHOICES = [
        ('Thirty360', '30/360 (Bond Basis)'),
        ('Actual360', 'Actual/360'),
        ('Actual365', 'Actual/365 Fixed'),
    ]
    
    day_count = forms.ChoiceField(
        label='Day Count Convention',
        choices=DAY_COUNT_CHOICES,
        initial='Thirty360',
        help_text='Method used to calculate the number of days between two dates for interest accrual.',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Calendar
    CALENDAR_CHOICES = [
        ('UnitedStates', 'United States (Government Bond)'),
        ('UnitedKingdom', 'United Kingdom'),
        ('TARGET', 'TARGET'),
    ]
    
    calendar = forms.ChoiceField(
        label='Calendar',
        choices=CALENDAR_CHOICES,
        initial='UnitedStates',
        help_text='Business day calendar used to determine holidays and business days.',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Interpolation Method
    INTERPOLATION_CHOICES = [
        ('Linear', 'Linear'),
        ('LogLinear', 'Log Linear'),
        ('Cubic', 'Cubic'),
    ]
    
    interpolation = forms.ChoiceField(
        label='Interpolation Method',
        choices=INTERPOLATION_CHOICES,
        initial='Linear',
        help_text='Method used to interpolate between known points on the yield curve.',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Compounding
    COMPOUNDING_CHOICES = [
        ('Simple', 'Simple'),
        ('Compounded', 'Compounded'),
        ('Continuous', 'Continuous'),
    ]
    
    compounding = forms.ChoiceField(
        label='Compounding',
        choices=COMPOUNDING_CHOICES,
        initial='Compounded',
        help_text='How interest is compounded over time (Simple, Compounded, or Continuous).',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Compounding Frequency
    FREQUENCY_CHOICES = [
        ('NoFrequency', 'No Frequency'),
        ('Once', 'Once'),
        ('Annual', 'Annual'),
        ('Semiannual', 'Semi-Annual'),
        ('EveryFourthMonth', 'Every Fourth Month'),
        ('Quarterly', 'Quarterly'),
        ('Bimonthly', 'Bimonthly'),
        ('Monthly', 'Monthly'),
        ('EveryFourthWeek', 'Every Fourth Week'),
        ('Biweekly', 'Biweekly'),
        ('Weekly', 'Weekly'),
        ('Daily', 'Daily'),
    ]
    
    compounding_frequency = forms.ChoiceField(
        label='Compounding Frequency',
        choices=FREQUENCY_CHOICES,
        initial='Annual',
        help_text='How often interest is compounded within a year (Annual, Semi-Annual, Quarterly, etc.).',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Business Day Convention
    CONVENTION_CHOICES = [
        ('Following', 'Following'),
        ('ModifiedFollowing', 'Modified Following'),
        ('Preceding', 'Preceding'),
        ('ModifiedPreceding', 'Modified Preceding'),
        ('Unadjusted', 'Unadjusted'),
    ]
    
    business_convention = forms.ChoiceField(
        label='Business Day Convention',
        choices=CONVENTION_CHOICES,
        initial='Unadjusted',
        help_text='How to handle payment dates that fall on weekends or holidays.',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Date Generation
    DATE_GENERATION_CHOICES = [
        ('Backward', 'Backward'),
        ('Forward', 'Forward'),
        ('Zero', 'Zero'),
        ('ThirdWednesday', 'Third Wednesday'),
        ('Twentieth', 'Twentieth'),
        ('TwentiethIMM', 'Twentieth IMM'),
        ('OldCDS', 'Old CDS'),
        ('CDS', 'CDS'),
        ('CDS2015', 'CDS 2015'),
    ]
    
    date_generation = forms.ChoiceField(
        label='Date Generation',
        choices=DATE_GENERATION_CHOICES,
        initial='Backward',
        help_text='Method for generating payment dates (Backward: from maturity to issue, Forward: from issue to maturity).',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Month End
    month_end = forms.BooleanField(
        label='Month End',
        initial=False,
        required=False,
        help_text='Whether to adjust payment dates to the end of the month.',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )