from django.shortcuts import render
from . import services

def glitch_lab_view(request):
    """
    Manages the "A Glitch in Forward-Rate Curves" lab page.
    """
    
    # 1. On appelle le service pour obtenir les données
    analysis_data = services.analyze_forward_curve_glitch()
    
    # 2. On prépare le contexte
    context = {
        'analysis_data': analysis_data
    }
    
    # ==============================================================================
    # 3. LA LIGNE RETURN EST BIEN À LA FIN DE LA FONCTION, SANS INDENTATION
    # ==============================================================================
    return render(request, 'chapter_glitch_curve/glitch_lab.html', context)