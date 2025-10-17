from django.db import models
from django.utils import timezone

class CalibrationResult(models.Model):
    """Model to store calibration results for analysis and comparison"""
    
    MODEL_CHOICES = [
        ('HullWhite', 'Hull-White 1-Factor'),
        ('BlackKarasinski', 'Black-Karasinski'),
        ('G2', 'G2++ 2-Factor'),
    ]
    
    CALIBRATION_TYPE_CHOICES = [
        ('standard', 'Standard Calibration'),
        ('constrained', 'Constrained Calibration'),
        ('normal_vol', 'Normal Volatility Calibration'),
    ]
    
    # Basic information
    model_name = models.CharField(max_length=20, choices=MODEL_CHOICES)
    calibration_type = models.CharField(max_length=20, choices=CALIBRATION_TYPE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Calibration parameters (stored as JSON-like strings for flexibility)
    parameters = models.JSONField(help_text="Calibrated model parameters")
    param_string = models.TextField(help_text="Human-readable parameter string")
    
    # Performance metrics
    rmse_price_error = models.FloatField(help_text="Root mean square error for prices")
    rmse_vol_error = models.FloatField(help_text="Root mean square error for volatilities")
    
    # Market data used (for reference)
    market_data = models.JSONField(help_text="Market data used for calibration")
    
    # Detailed results
    calibration_report = models.JSONField(help_text="Detailed calibration report data")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Calibration Result'
        verbose_name_plural = 'Calibration Results'
    
    def __str__(self):
        return f"{self.get_model_name_display()} - {self.get_calibration_type_display()} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
    @property
    def is_good_fit(self):
        """Determine if the calibration is considered a good fit"""
        return self.rmse_price_error < 0.10
    
    @property
    def fit_quality(self):
        """Get a human-readable fit quality assessment"""
        if self.rmse_price_error < 0.05:
            return "Excellent"
        elif self.rmse_price_error < 0.10:
            return "Good"
        elif self.rmse_price_error < 0.20:
            return "Fair"
        else:
            return "Poor"
