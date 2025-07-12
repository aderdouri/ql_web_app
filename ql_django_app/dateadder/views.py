from django.shortcuts import render
from .forms import DateAdderForm
import QuantLib as ql
 
def date_adder_view(request):
    result = None
    if request.method == 'POST':
        form = DateAdderForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data['input_date']
            ql_date = ql.Date(d.day, d.month, d.year)
            new_ql_date = ql_date + 10
            result = f"{new_ql_date.dayOfMonth():02d}/{new_ql_date.month():02d}/{new_ql_date.year()}"
    else:
        form = DateAdderForm()
    return render(request, 'dateadder/date_adder.html', {
        'form': form,
        'result': result
    })