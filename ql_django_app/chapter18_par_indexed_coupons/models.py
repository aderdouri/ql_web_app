from django.db import models
from django.utils import timezone

class SwapAnalysisResult(models.Model):
    ANALYSIS_TYPE_CHOICES = [
        ('par_coupons', 'Par Coupons Analysis'),
        ('indexed_coupons', 'Indexed Coupons Analysis'),
        ('comparison', 'Comparison Analysis'),
    ]
    
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Swap parameters
    notional = models.FloatField(help_text="Notional amount")
    swap_length = models.FloatField(help_text="Swap length in years")
    evaluation_date = models.DateField(help_text="Evaluation date")
    
    # Results
    coupon_data = models.JSONField(help_text="Detailed coupon calculations")
    par_coupon_amounts = models.JSONField(help_text="Par coupon amounts")
    indexed_coupon_amounts = models.JSONField(help_text="Indexed coupon amounts")
    difference_analysis = models.JSONField(help_text="Difference analysis between methods")
    
    # Summary statistics
    total_par_amount = models.FloatField(help_text="Total par coupon amount")
    total_indexed_amount = models.FloatField(help_text="Total indexed coupon amount")
    difference_amount = models.FloatField(help_text="Difference between methods")
    max_rate_difference = models.FloatField(help_text="Maximum rate difference")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Swap Analysis Result'
        verbose_name_plural = 'Swap Analysis Results'

    def __str__(self):
        return f"Swap Analysis - {self.get_analysis_type_display()} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def has_significant_difference(self):
        return abs(self.difference_amount) > 0.01

    @property
    def difference_percentage(self):
        if self.total_par_amount != 0:
            return (self.difference_amount / self.total_par_amount) * 100
        return 0

















