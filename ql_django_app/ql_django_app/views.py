from django.shortcuts import render

# Cette vue rendra la page d'accueil principale
def home(request):
    return render(request, 'home.html')

# Cette vue rendra la page d'accueil de la catégorie "Produits de Taux"
# Son seul rôle est d'afficher le gabarit "rates_base.html" qui contient la sous-navbar.
def rates_home(request):
    return render(request, 'rates/rates_base.html')

# Vue pour la catégorie "Actions & Options"
def equity_home(request):
    return render(request, 'equity/equity_base.html')

# Vue pour la catégorie "Obligations"
def bonds_home(request):
    return render(request, 'bonds/bonds_base.html')
    
# Vue pour la catégorie "Outils"
def tools_home(request):
    return render(request, 'tools/tools_base.html')