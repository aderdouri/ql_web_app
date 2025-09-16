from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .forms import LastCouponGapForm, FixedToFloaterForm, StubCouponForm
from .services import build_bond_with_last_coupon_gap, build_fixed_to_floater_bond, build_stub_coupon_bond

def irregular_lab(request):
    """Main view for the irregular bonds lab"""
    form1 = LastCouponGapForm()
    form2 = FixedToFloaterForm()
    form3 = StubCouponForm()
    
    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
    }
    
    return render(request, 'irregular_bonds/irregular_lab.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def calculate_bond(request):
    """AJAX endpoint for bond calculations"""
    try:
        data = json.loads(request.body)
        calculation_type = data.get('type')
        
        if calculation_type == 'last_coupon_gap':
            form = LastCouponGapForm(data)
            if form.is_valid():
                result = build_bond_with_last_coupon_gap(
                    form.cleaned_data['issue_date'],
                    form.cleaned_data['maturity_date'],
                    form.cleaned_data['coupon_rate'],
                    form.cleaned_data['bond_type']
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': 'Invalid form data'}, status=400)
                
        elif calculation_type == 'fixed_to_floater':
            form = FixedToFloaterForm(data)
            if form.is_valid():
                result = build_fixed_to_floater_bond(
                    form.cleaned_data['issue_date'],
                    form.cleaned_data['maturity_date'],
                    form.cleaned_data['fixed_years'],
                    form.cleaned_data['fixed_rate'],
                    form.cleaned_data['float_spread']
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': 'Invalid form data'}, status=400)
                
        elif calculation_type == 'stub_coupon':
            form = StubCouponForm(data)
            if form.is_valid():
                result = build_stub_coupon_bond(
                    form.cleaned_data['start_date'],
                    form.cleaned_data['end_date']
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': 'Invalid form data'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid calculation type'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
