from django import forms
import datetime

class CallableBondForm(forms.Form):
    # Paramètres de la courbe de taux et de l'obligation (simplifié)
    evaluation_date = forms.DateField(
        label="Evaluation Date", 
        initial=datetime.date(2016, 8, 16),
        help_text="Date for bond valuation (format: YYYY-MM-DD)"
    )
    yield_curve_rate = forms.FloatField(
        label="Flat Yield Curve Rate", 
        initial=0.035,
        help_text="Risk-free interest rate (e.g., 0.035 = 3.5%)"
    )
    coupon_rate = forms.FloatField(
        label="Bond Coupon Rate", 
        initial=0.025,
        help_text="Annual coupon rate paid by the bond (e.g., 0.025 = 2.5%)"
    )

    # Paramètres du modèle Hull-White
    mean_reversion = forms.FloatField(
        label="Mean Reversion (a)", 
        initial=0.03,
        help_text="Speed of mean reversion (typically 0.01-0.1)"
    )
    volatility = forms.FloatField(
        label="Volatility (sigma)", 
        initial=0.12,
        help_text="Interest rate volatility (typically 0.05-0.3)"
    )
    grid_points = forms.IntegerField(
        label="Grid Points", 
        initial=40,
        help_text="Number of grid points for the tree model (higher = more accurate, slower)"
    )
    
    # Paramètres pour le graphique de sensibilité
    sigma_min = forms.FloatField(
        label="Sigma Min for Chart", 
        initial=0.001,
        help_text="Minimum volatility for sensitivity analysis (e.g., 0.001 = 0.1%)"
    )
    sigma_max = forms.FloatField(
        label="Sigma Max for Chart", 
        initial=0.15,
        help_text="Maximum volatility for sensitivity analysis (e.g., 0.15 = 15%)"
    )
    sigma_step = forms.FloatField(
        label="Sigma Step for Chart", 
        initial=0.001,
        help_text="Step size for volatility increments (smaller = smoother curve)"
    )