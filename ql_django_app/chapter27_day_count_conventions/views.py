from django.shortcuts import render
from .forms import DayCountForm
from .services import analyze_day_count_glitch

def day_count_conventions_description_view(request):
    context = {
        'chapter_title': 'Chapter 27: Using Curves with Different Day-Count Conventions',
        'chapter_description': 'Understanding the glitch in QuantLib when using curves with different day-count conventions and its impact on option pricing engines.',
        'chapter_icon': 'bi bi-calendar3'
    }
    return render(request, 'chapter27_day_count_conventions/day_count_conventions_description.html', context)

def day_count_conventions_chapter_view(request):
    context = {
        'chapter_title': 'Chapter 27: Using Curves with Different Day-Count Conventions',
        'chapter_description': 'Understanding the glitch in QuantLib when using curves with different day-count conventions and its impact on option pricing engines.',
        'chapter_icon': 'bi bi-calendar3'
    }
    
    if request.method == 'POST':
        form = DayCountForm(request.POST)
        if form.is_valid():
            # Get form data
            form_data = form.cleaned_data
            
            # Perform analysis
            results = analyze_day_count_glitch(form_data)
            context['form'] = form
            context['results'] = results
        else:
            context['form'] = form
    else:
        context['form'] = DayCountForm()
    
    return render(request, 'chapter27_day_count_conventions/day_count_conventions_chapter.html', context)
