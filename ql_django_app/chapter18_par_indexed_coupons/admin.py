from django.contrib import admin
from .models import SwapAnalysisResult

@admin.register(SwapAnalysisResult)
class SwapAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['analysis_type', 'notional', 'swap_length', 'evaluation_date', 'created_at']
    list_filter = ['analysis_type', 'created_at']
    search_fields = ['analysis_type']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Analysis Info', {
            'fields': ('analysis_type', 'created_at')
        }),
        ('Swap Parameters', {
            'fields': ('notional', 'swap_length', 'evaluation_date')
        }),
        ('Results', {
            'fields': ('total_par_amount', 'total_indexed_amount', 'difference_amount', 'max_rate_difference')
        }),
        ('Detailed Data', {
            'fields': ('coupon_data', 'par_coupon_amounts', 'indexed_coupon_amounts', 'difference_analysis'),
            'classes': ('collapse',)
        })
    )

