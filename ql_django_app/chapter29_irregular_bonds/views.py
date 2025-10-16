from django.shortcuts import render
from django.http import JsonResponse
from .forms import LastCouponGapForm, FixedToFloaterForm, StubCouponForm
from .services import build_bond_with_last_coupon_gap, build_fixed_to_floater_bond, build_bond_with_stub_coupon

def description(request):
    """Chapter 29 description view"""
    context = {
        'chapter_title': '29. Building Irregular Bonds',
        'chapter_icon': 'bi-puzzle',
        'chapter_description': 'Learn advanced techniques for modeling bonds with irregular features using QuantLib, including custom coupon schedules and mixed fixed-floating rate structures.'
    }
    return render(request, 'chapter29_irregular_bonds/description.html', context)

def irregular_lab_view(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        calculation_type = request.POST.get('calculation_type')
        
        try:
            if calculation_type == 'last_coupon_gap':
                form = LastCouponGapForm(request.POST)
                if form.is_valid():
                    results = build_bond_with_last_coupon_gap(**form.cleaned_data)
                    return JsonResponse(results)
            
            elif calculation_type == 'fixed_to_floater':
                form = FixedToFloaterForm(request.POST)
                if form.is_valid():
                    results = build_fixed_to_floater_bond(**form.cleaned_data)
                    return JsonResponse(results)

            elif calculation_type == 'stub_coupon':
                form = StubCouponForm(request.POST)
                if form.is_valid():
                    results = build_bond_with_stub_coupon(**form.cleaned_data)
                    return JsonResponse(results)
            
            if 'form' in locals() and form.errors:
                return JsonResponse({'error': form.errors.as_json()}, status=400)
            else:
                 return JsonResponse({'error': 'Invalid calculation type.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': f"A server error occurred: {str(e)}"}, status=500)

    # Premier chargement (GET)
    context = {
        'form1': LastCouponGapForm(),
        'form2': FixedToFloaterForm(),
        'form3': StubCouponForm(),
    }
    return render(request, 'chapter29_irregular_bonds/irregular_lab.html', context)