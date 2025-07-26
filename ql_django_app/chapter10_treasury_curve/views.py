from django.shortcuts import render
from datetime import date
from . import services # Assurez-vous d'avoir aussi créé le fichier services.py

def curve_lab_view(request):
    """
    Cette vue gère le laboratoire du Chapitre 10 : Construire une courbe du Trésor.
    """
    # On utilise une date fixe pour cet exemple, comme dans le Cookbook
    eval_date = date(2004, 5, 15)
    
    # On appelle le service pour faire le calcul et récupérer les points du graphique
    plot_points = services.build_treasury_curve(eval_date)
    
    # On prépare les données à envoyer au template
    context = {
        'plot_points': plot_points, 
        'eval_date': eval_date.isoformat()
    }
    
    # On affiche le template HTML avec les données
    return render(request, 'chapter10_treasury_curve/curve_lab.html', context)