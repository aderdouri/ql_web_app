from django.shortcuts import render
from django.http import JsonResponse
from .forms import SwapAnalysisForm
from .services import analyze_swap_coupons, get_analysis_descriptions
from .models import SwapAnalysisResult

def par_indexed_coupons_description_view(request):
    """Description page for Chapter 18"""
    model_descriptions = get_analysis_descriptions()
    
    context = {
        'chapter_title': 'Chapter 18: Par vs Indexed Coupons',
        'chapter_icon': 'bi-calculator',
        'chapter_description': 'Interactive laboratory to analyze the differences between par coupons and indexed coupons in interest rate swap calculations.',
        'model_descriptions': model_descriptions,
    }
    return render(request, 'chapter_par_indexed_coupons/description.html', context)

def par_indexed_coupons_lab_view(request):
    """Interactive lab for swap coupon analysis"""
    if request.method == 'POST':
        form = SwapAnalysisForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                notional = form.cleaned_data['notional']
                swap_length = form.cleaned_data['swap_length']
                evaluation_date = form.cleaned_data['evaluation_date']
                use_par = form.cleaned_data['use_par_coupons']
                use_indexed = form.cleaned_data['use_indexed_coupons']
                
                # Perform analysis
                results = analyze_swap_coupons(
                    notional=notional,
                    swap_length=swap_length,
                    evaluation_date=evaluation_date,
                    use_par=use_par,
                    use_indexed=use_indexed
                )
                
                if results['success']:
                    # Save results to database
                    analysis_result = SwapAnalysisResult.objects.create(
                        analysis_type='comparison' if (use_par and use_indexed) else ('par_coupons' if use_par else 'indexed_coupons'),
                        notional=notional,
                        swap_length=swap_length,
                        evaluation_date=evaluation_date,
                        coupon_data=results.get('par_coupons', {}).get('data', []) + results.get('indexed_coupons', {}).get('data', []),
                        par_coupon_amounts=results.get('par_coupons', {}).get('data', []),
                        indexed_coupon_amounts=results.get('indexed_coupons', {}).get('data', []),
                        difference_analysis=results.get('comparison', {}).get('data', []),
                        total_par_amount=results.get('par_coupons', {}).get('total_amount', 0),
                        total_indexed_amount=results.get('indexed_coupons', {}).get('total_amount', 0),
                        difference_amount=results.get('comparison', {}).get('total_amount_difference', 0),
                        max_rate_difference=results.get('comparison', {}).get('max_rate_difference', 0)
                    )
                    
                    context = {
                        'form': form,
                        'results': results,
                        'analysis_result': analysis_result
                    }
                else:
                    context = {
                        'form': form,
                        'error_message': results['error']
                    }
            except Exception as e:
                context = {
                    'form': form,
                    'error_message': f"Une erreur s'est produite lors de l'analyse: {str(e)}"
                }
        else:
            context = {
                'form': form,
                'error_message': "Veuillez corriger les erreurs dans le formulaire."
            }
    else:
        # Initial page load (GET) - No automatic results
        form = SwapAnalysisForm()
        context = {
            'form': form
        }
    
    return render(request, 'chapter_par_indexed_coupons/par_indexed_coupons_lab_professional.html', context)

