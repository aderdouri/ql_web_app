# chapter2_instruments/services.py (VERSION FINALE ET PARFAITE)

import QuantLib as ql
import numpy as np
import datetime

def calculate_option_values(data):
    """
    Calcule la NPV, les Greeks et les données du graphique.
    Version de production finale, optimisée et robuste.
    """
    try:
        # 1. Valider et configurer les dates
        eval_date = data['evaluation_date']
        exp_date = data['expiry_date']

        if not isinstance(eval_date, datetime.date) or not isinstance(exp_date, datetime.date):
            return {'error': 'Invalid date object provided'}

        ql_evaluation_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = ql_evaluation_date
        
        ql_expiry_date = ql.Date(exp_date.day, exp_date.month, exp_date.year)

        if ql_expiry_date < ql_evaluation_date:
            return {'error': "La date d'échéance doit être après la date d'évaluation."}

        # 2. Valider et configurer les paramètres numériques
        strike = float(data['strike_price'])
        underlying_price = float(data['underlying_price'])
        risk_free_rate = float(data['risk_free_rate'])
        volatility = float(data['volatility'])
        option_type = ql.Option.Call if data['option_type'] == 'Call' else ql.Option.Put
        
        # 3. Construire l'instrument (l'option)
        payoff = ql.PlainVanillaPayoff(option_type, strike)
        exercise = ql.EuropeanExercise(ql_expiry_date)
        option = ql.EuropeanOption(payoff, exercise)

        # 4. Construire les objets de marché
        underlying_quote = ql.SimpleQuote(underlying_price)
        u_handle = ql.QuoteHandle(underlying_quote)
        r_handle = ql.YieldTermStructureHandle(ql.FlatForward(ql_evaluation_date, risk_free_rate, ql.Actual365Fixed()))
        sigma_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(ql_evaluation_date, ql.TARGET(), volatility, ql.Actual365Fixed()))
        
        # 5. Construire et attacher le moteur de pricing
        process = ql.BlackScholesProcess(u_handle, r_handle, sigma_handle)
        engine = ql.AnalyticEuropeanEngine(process)
        option.setPricingEngine(engine)

        # 6. Effectuer les calculs
        results = {
            'npv': option.NPV(), 'delta': option.delta(),
            'gamma': option.gamma(), 'vega': option.vega()
        }

        # 7. Générer les données pour le graphique interactif
        chart_data = {'x_values': [], 'y_values': []}
        
        xs = np.linspace(strike * 0.8, strike * 1.2, 100)
        for x in xs:
            underlying_quote.setValue(x) # On modifie la quote pour chaque point du graphique
            chart_data['x_values'].append(x)
            chart_data['y_values'].append(option.NPV())
        
        underlying_quote.setValue(underlying_price) # Important: On remet la valeur d'origine
        
        results['chart_data'] = chart_data
        
        return results

    except Exception as e:
        # En cas d'erreur de calcul, on l'affiche dans la console du serveur
        print(f"ERREUR QUANTLIB: {e}")
        return {'error': str(e)}