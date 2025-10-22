from django.shortcuts import render

def caps_floors_description_view(request):
    """
    View for the caps and floors description page.
    """
    context = {
        'chapter_title': 'Interest Rate Caps and Floors',
        'chapter_icon': 'bi-shield-check',
        'chapter_description': 'Learn about interest rate caps and floors, essential derivatives for managing interest rate risk.'
    }
    return render(request, 'caps_floors/description.html', context)

def caps_floors_lab_view(request):
    """
    View for the caps and floors interactive lab.
    """
    context = {
        'chapter_title': 'Caps and Floors Laboratory',
        'chapter_icon': 'bi-flask',
        'chapter_description': 'Interactive laboratory for experimenting with cap and floor pricing.'
    }
    return render(request, 'caps_floors/lab.html', context)