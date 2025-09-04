# chapter3_greeks/services.py (VERSION FINALE ET LA PLUS ROBUSTE)

import QuantLib as ql
import numpy as np
import datetime

def calculate_numerical_greeks(data):
    try:
        # --- 1. CONFIGURATION ---
        eval_date = data['evaluation_date']
        ql.Settings.instance().evaluationDate = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        expiry_date = data['expiry_date']

        barrier_types = {'UpIn': ql.Barrier.UpIn, 'UpOut': ql.Barrier.UpOut, 'DownIn': ql.Barrier.DownIn, 'DownOut': ql.Barrier.DownOut}
        option_types = {'Call': ql.Option.Call, 'Put': ql.Option.Put}

        underlying_price = float(data['underlying_price'])
        strike_price = float(data['strike_price'])
        barrier_level = float(data['barrier_level'])
        
        if underlying_price == barrier_level:
            return {'error': "Le prix du sous-jacent ne peut pas être égal au niveau de la barrière."}

        # --- 2. CRÉATION DE L'OPTION ET DU MOTEUR ---
        payoff = ql.PlainVanillaPayoff(option_types.get(data['option_type']), strike_price)
        exercise = ql.EuropeanExercise(ql.Date(expiry_date.day, expiry_date.month, expiry_date.year))
        option = ql.BarrierOption(barrier_types.get(data['barrier_type']), barrier_level, float(data['rebate']), payoff, exercise)

        u_quote = ql.SimpleQuote(underlying_price)
        r_quote = ql.SimpleQuote(float(data['risk_free_rate']))
        sigma_quote = ql.SimpleQuote(float(data['volatility']))

        risk_free_curve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r_quote), ql.Actual360())
        volatility_curve = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma_quote), ql.Actual360())
        process = ql.BlackScholesProcess(ql.QuoteHandle(u_quote), ql.YieldTermStructureHandle(risk_free_curve), ql.BlackVolTermStructureHandle(volatility_curve))
        option.setPricingEngine(ql.AnalyticBarrierEngine(process))

        # --- 3. CALCUL DES GREEKS NUMÉRIQUES ---
        # Cette partie peut encore échouer si les paramètres de base sont incohérents, c'est normal.
        results = {}
        P0 = option.NPV()
        results['p0'] = P0

        h_u = float(data['h_underlying'])
        u_quote.setValue(underlying_price + h_u); p_plus_u = option.NPV(); results['p_plus_u'] = p_plus_u
        u_quote.setValue(underlying_price - h_u); p_minus_u = option.NPV(); results['p_minus_u'] = p_minus_u
        u_quote.setValue(underlying_price)
        results['delta'] = (p_plus_u - p_minus_u) / (2 * h_u) if h_u != 0 else 0
        results['gamma'] = (p_plus_u - 2 * P0 + p_minus_u) / (h_u * h_u) if h_u != 0 else 0

        r0 = r_quote.value(); h_r = float(data['h_rate']); r_quote.setValue(r0 + h_r); p_plus_r = option.NPV(); r_quote.setValue(r0)
        results['rho'] = (p_plus_r - P0) / h_r if h_r != 0 else 0

        sigma0 = sigma_quote.value(); h_sigma = float(data['h_vol']); sigma_quote.setValue(sigma0 + h_sigma); p_plus_sigma = option.NPV(); sigma_quote.setValue(sigma0)
        results['vega'] = (p_plus_sigma - P0) / h_sigma if h_sigma != 0 else 0

        today = ql.Settings.instance().evaluationDate; ql.Settings.instance().evaluationDate = today + 1; p1 = option.NPV(); ql.Settings.instance().evaluationDate = today
        results['theta'] = (p1 - P0) / (1.0 / 365.0)

        # --- 4. GÉNÉRATION DES DONNÉES POUR LE GRAPHIQUE ---
        chart_data = {'curve': {'x': [], 'y': []}, 'tangent': {'x': [], 'y': []}}
        x_values = np.linspace(strike_price * 0.8, strike_price * 1.2, 100)
        
        for x in x_values:
            u_quote.setValue(x)
            chart_data['curve']['x'].append(x)
            try:
                # =========================================================================
                # CORRECTION : On gère l'erreur pour chaque point du graphique
                # =========================================================================
                chart_data['curve']['y'].append(option.NPV())
            except RuntimeError as e:
                if 'barrier touched' in str(e):
                    # Si la barrière est touchée, on met un "trou" dans les données
                    chart_data['curve']['y'].append(None) 
                else:
                    raise # On relève les autres erreurs inattendues
        
        delta_val = results['delta']
        for x in x_values:
             chart_data['tangent']['x'].append(x)
             chart_data['tangent']['y'].append(delta_val * (x - underlying_price) + P0)

        u_quote.setValue(underlying_price) # Reset final
        results['chart_data'] = chart_data

        return results

    except Exception as e:
        return {'error': str(e)}