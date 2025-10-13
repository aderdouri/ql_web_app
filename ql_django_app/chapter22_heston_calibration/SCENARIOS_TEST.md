# 🎯 Scénarios de Test - Calibration Heston

## 📚 Scénarios du Livre "QuantLib Python Cookbook"

### **Scénario 1 : Conditions initiales optimales**
```
Paramètres initiaux: (0.02, 0.2, 0.5, 0.1, 0.01)
- θ (Theta): 0.02
- κ (Kappa): 0.2
- σ (Sigma): 0.5
- ρ (Rho): 0.1
- v₀ (V0): 0.01
```

**Résultats attendus du livre :**
- **QuantLib LM**: θ=0.1258, κ=7.8814, σ=1.8847, ρ=-0.3650, v₀=0.0555, Erreur=3.013%
- **SciPy LM**: θ=0.1258, κ=7.8824, σ=1.8849, ρ=-0.3650, v₀=0.0555, Erreur=3.013%

### **Scénario 2 : Conditions initiales alternatives**
```
Paramètres initiaux: (0.07, 0.5, 0.1, 0.1, 0.1)
- θ (Theta): 0.07
- κ (Kappa): 0.5
- σ (Sigma): 0.1
- ρ (Rho): 0.1
- v₀ (V0): 0.1
```

**Résultats attendus du livre :**
- **QuantLib LM**: θ=0.0845, κ=0.0000, σ=0.1315, ρ=-0.5148, v₀=0.0999, Erreur=11.000%
- **SciPy LM**: θ=0.0500, κ=-0.5598, σ=0.1910, ρ=-1.0033, v₀=0.0905, Erreur=6.844%

## 🚀 Comment tester

### **Étape 1 : Accéder à l'application**
```
URL: http://127.0.0.1:8000/equity-models/heston-parameter-calibration/lab/
```

### **Étape 2 : Sélectionner un scénario**
1. **Scénario 1** : Utilisez le dropdown "Quick Scenarios" → "Scenario 1"
2. **Scénario 2** : Utilisez le dropdown "Quick Scenarios" → "Scenario 2"

### **Étape 3 : Choisir le solveur**
- **QuantLib Levenberg-Marquardt** (pour comparaison avec le livre)
- **SciPy Levenberg-Marquardt** (pour comparaison avec le livre)

### **Étape 4 : Lancer la calibration**
Cliquez sur "Run Calibration"

## 📊 Validation des résultats

### **✅ Scénario 1 - Résultats corrects :**
- θ ≈ 0.1258 (±0.001)
- κ ≈ 7.88 (±0.1)
- σ ≈ 1.88 (±0.1)
- ρ ≈ -0.37 (±0.05)
- v₀ ≈ 0.0555 (±0.005)
- Erreur ≈ 3.0% (±0.5%)

### **✅ Scénario 2 - Résultats corrects :**
- θ ≈ 0.05-0.08 (±0.01)
- κ ≈ 0.0 à -0.6 (±0.1)
- σ ≈ 0.13-0.19 (±0.02)
- ρ ≈ -0.5 à -1.0 (±0.1)
- v₀ ≈ 0.09-0.10 (±0.01)
- Erreur ≈ 6-11% (±1%)

## 🔧 Données utilisées (du livre)

### **Données de marché :**
- **Spot Price**: 659.37
- **Risk-Free Rate**: 1.0%
- **Dividend Rate**: 0.0%
- **Calculation Date**: 2015-11-06
- **Maturity Date**: 2016-11-06

### **Grille de volatilités :**
- **24 maturities** : Dec 2015 à Nov 2017
- **8 strikes** : 527.50 à 758.28
- **Données exactes** du livre utilisées

## ⚠️ Problèmes possibles

### **Si les résultats ne correspondent pas :**
1. **Vérifiez** que le serveur Django fonctionne
2. **Vérifiez** que les données de volatilité sont correctes
3. **Vérifiez** que les paramètres initiaux sont bien chargés
4. **Comparez** avec les résultats du livre

### **Si l'application ne démarre pas :**
```bash
cd ql_web_app/ql_django_app
python manage.py runserver
```

## 🎯 Objectif

**Reproduire exactement les résultats du livre "QuantLib Python Cookbook" pour valider l'implémentation de la calibration Heston.**
