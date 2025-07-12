from django.shortcuts import render
from .forms import BondPricingForm
from .bond_pricer import price_fixed_rate_bond
import QuantLib as ql
 
 
def price_bond(request):
    results = None
    
    if request.method == 'POST':
        form = BondPricingForm(request.POST)
        if form.is_valid():
            # Convert form data to QuantLib objects
            evaluation_date = ql.Date(form.cleaned_data['evaluation_date'].day,
                                    form.cleaned_data['evaluation_date'].month,
                                    form.cleaned_data['evaluation_date'].year)
            
            issue_date = ql.Date(form.cleaned_data['issue_date'].day,
                               form.cleaned_data['issue_date'].month,
                               form.cleaned_data['issue_date'].year)
            
            maturity_date = ql.Date(form.cleaned_data['maturity_date'].day,
                                  form.cleaned_data['maturity_date'].month,
                                  form.cleaned_data['maturity_date'].year)
            
            coupon_rate = form.cleaned_data['coupon_rate'] / 100
            market_yield = form.cleaned_data['market_yield'] / 100
            face_amount = form.cleaned_data['face_amount']
            
            # Convert frequency
            frequency_map = {
                'Annual': ql.Annual,
                'Semiannual': ql.Semiannual,
                'Quarterly': ql.Quarterly,
            }
            frequency = frequency_map[form.cleaned_data['frequency']]
            
            # Convert day count convention
            day_count_map = {
                'Thirty360.USA': ql.Thirty360(ql.Thirty360.USA),
                'ActualActual.ISMA': ql.ActualActual(ql.ActualActual.ISMA),
                'Actual360': ql.Actual360(),
                'Actual365Fixed': ql.Actual365Fixed(),
            }
            day_count_convention = day_count_map[form.cleaned_data['day_count_convention']]
            
            # Price the bond
            results = price_fixed_rate_bond(
                evaluation_date=evaluation_date,
                issue_date=issue_date,
                maturity_date=maturity_date,
                coupon_rate=coupon_rate,
                face_amount=face_amount,
                market_yield=market_yield,
                frequency=frequency,
                day_count_convention=day_count_convention
            )
            
            # Add calculated fields for template
            if results['status'] == 'success':
                results['dirty_price_total'] = results['dirty_price'] * face_amount / 100
                results['yield_percent'] = results['yield'] * 100
    else:
        form = BondPricingForm()
    
    return render(request, 'bond02/bond_price.html', {
        'form': form,
        'results': results
    })
 
 