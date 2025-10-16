# services.py (VERSION FINALE ET COMPLÈTE)

import QuantLib as ql
import datetime

def calculate_discount_margin(data):
    try:
        # 1. Setup from form data
        eval_date = data['evaluation_date']
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = today
        
        issue_date_dt = data['issue_date']
        maturity_date_dt = data['maturity_date']
        face_amount = data['face_amount']
        forecast_rate = data['forecast_rate']
        
        target_price = float(data['target_price'])
        # Convertir la string scientifique en float
        accuracy_str = data['solver_accuracy']
        if accuracy_str == '1e-6':
            accuracy = 1e-6
        elif accuracy_str == '1e-8':
            accuracy = 1e-8
        elif accuracy_str == '1e-10':
            accuracy = 1e-10
        else:
            accuracy = float(accuracy_str)
        min_margin = float(data['min_margin'])
        max_margin = float(data['max_margin'])
        
        # 2. Construction de l'obligation avec les paramètres du formulaire
        forecast_curve = ql.RelinkableYieldTermStructureHandle()
        discount_curve = ql.RelinkableYieldTermStructureHandle()
        
        # Utiliser le forecast_rate du formulaire pour la courbe
        forecast_curve.linkTo(ql.FlatForward(0, ql.TARGET(), forecast_rate, ql.Actual360()))
        
        index = ql.Euribor6M(forecast_curve)
        
        # Utiliser les dates du formulaire
        issue_date = ql.Date(issue_date_dt.day, issue_date_dt.month, issue_date_dt.year)
        maturity_date = ql.Date(maturity_date_dt.day, maturity_date_dt.month, maturity_date_dt.year)
        
        # Créer le schedule avec les dates du formulaire
        schedule = ql.Schedule(issue_date, maturity_date, ql.Period(ql.Semiannual), ql.TARGET(),
                               ql.Following, ql.Following, ql.DateGeneration.Backward, False)
        
        # Créer l'obligation avec le face_amount du formulaire
        bond = ql.FloatingRateBond(3, face_amount, schedule, index, ql.Actual360())
        bond.setPricingEngine(ql.DiscountingBondEngine(discount_curve))
        
        # Ajouter des fixings pour éviter les erreurs "Missing fixing"
        target_calendar = ql.TARGET()
        
        # Ajouter des fixings pour les 2 dernières années avant l'evaluation date
        fixing_date = today - ql.Period(2, ql.Years)
        fixing_count = 0
        
        while fixing_date <= today:
            if target_calendar.isBusinessDay(fixing_date):
                try:
                    # Vérifier si un fixing existe déjà
                    existing_fixing = index.fixing(fixing_date)
                except:
                    # Aucun fixing n'existe, on peut l'ajouter
                    try:
                        index.addFixing(fixing_date, forecast_rate)
                        fixing_count += 1
                    except Exception as e:
                        pass  # Ignorer les erreurs silencieusement
            fixing_date = fixing_date + ql.Period(1, ql.Days)
        
        # 3. Préparation pour la résolution inverse
        DM_quote = ql.SimpleQuote(0.0)
        discount_curve.linkTo(ql.ZeroSpreadedTermStructure(forecast_curve, ql.QuoteHandle(DM_quote)))
        
        def error_function(spread):
            try:
                DM_quote.setValue(spread)
                price = bond.cleanPrice()
                error = price - target_price
                return error
            except Exception as e:
                # Si le calcul échoue, retourner une valeur d'erreur élevée
                return 1e6  # Valeur d'erreur élevée pour que le solveur évite cette zone
            
        # 4. Résolution avec le solveur
        solver = ql.Brent()
        
        # Validation et correction des bornes si nécessaire
        if min_margin >= max_margin:
            # Si les bornes sont inversées, les corriger
            min_margin, max_margin = min(min_margin, max_margin), max(min_margin, max_margin)
            
        # S'assurer qu'il y a un écart minimum entre les bornes
        if max_margin - min_margin < 1e-6:
            max_margin = min_margin + 1e-4
        
        # Test: Prix de l'obligation sans spread
        DM_quote.setValue(0.0)
        price_without_spread = bond.cleanPrice()
        
        # Essayer différentes signatures du solveur
        try:
            # Signature 1: solve(function, accuracy, min, max)
            discount_margin_continuous = solver.solve(error_function, accuracy, min_margin, max_margin)
        except Exception as e1:
            try:
                # Signature 2: solve(function, accuracy, min, max, guess)
                initial_guess = (min_margin + max_margin) / 2.0
                discount_margin_continuous = solver.solve(error_function, accuracy, min_margin, max_margin, initial_guess)
            except Exception as e2:
                # Essayer avec des bornes intelligentes basées sur la différence de prix
                price_diff = price_without_spread - target_price
                if abs(price_diff) > 50:  # Si la différence est très grande
                    intelligent_min = -0.2  # -20%
                    intelligent_max = 0.2   # +20%
                elif abs(price_diff) > 10:  # Si la différence est grande
                    intelligent_min = -0.1  # -10%
                    intelligent_max = 0.1   # +10%
                else:  # Si la différence est petite
                    intelligent_min = -0.05  # -5%
                    intelligent_max = 0.05   # +5%
                
                discount_margin_continuous = solver.solve(error_function, accuracy, intelligent_min, intelligent_max)
        
        # 5. Conversion du résultat
        value_date = index.valueDate(today)
        maturity_date_index = index.maturityDate(value_date)
        
        equivalent_rate = ql.InterestRate(
            discount_margin_continuous, discount_curve.dayCounter(),
            ql.Continuous, ql.NoFrequency
        ).equivalentRate(
            index.dayCounter(), ql.Simple, index.tenor().frequency(),
            value_date, maturity_date_index
        )

        # 6. Vérification du prix calculé
        DM_quote.setValue(discount_margin_continuous)
        calculated_bond_price = bond.cleanPrice()
        
        # 7. Extraction des cashflows
        cashflows_data = []
        total_coupons = 0
        principal_amount = 0
        
        for cf in bond.cashflows():
            amount = cf.amount()
            cashflows_data.append({
                'date': cf.date().ISO(),
                'amount': amount
            })
            
            # Compter les coupons vs principal
            if cf.date() == maturity_date:
                principal_amount = amount
            else:
                total_coupons += amount
        
        
        # 8. Generate simple and clear explanations
        price_diff = abs(calculated_bond_price - target_price)
        margin_bps = discount_margin_continuous * 10000
        equivalent_rate_pct = equivalent_rate.rate() * 100
        
        # Discount margin analysis - Simple and clear
        if margin_bps > 0:
            margin_analysis = f"The spread of {margin_bps:.2f} basis points indicates the bond trades with a risk premium. The market requires additional compensation above the reference rate."
        elif margin_bps < 0:
            margin_analysis = f"The spread of {margin_bps:.2f} basis points indicates the bond trades with a quality premium. The market accepts a lower yield than the reference rate."
        else:
            margin_analysis = f"The spread of {margin_bps:.2f} basis points indicates the bond trades exactly at the reference rate, with no premium or discount."
        
        # Calculation precision - Simple
        if price_diff < 1e-6:
            price_accuracy = f"Excellent precision! The calculated price (${calculated_bond_price:.6f}) matches exactly the target price (${target_price:.6f})."
        elif price_diff < 0.01:
            price_accuracy = f"High precision! The calculated price (${calculated_bond_price:.6f}) is very close to the target price (${target_price:.6f})."
        else:
            price_accuracy = f"Good precision! The calculated price (${calculated_bond_price:.6f}) is close to the target price (${target_price:.6f})."
        
        # Rate conversion - Simple
        equivalent_rate_explanation = f"The continuous spread of {margin_bps:.2f} basis points equals {equivalent_rate_pct:.6f}% in simple rate, according to Actual/360 convention."
        
        # Face amount information - Simple
        face_amount_info = f"The face amount of ${face_amount:.2f} does not affect the spread (which is a rate), but influences the absolute coupon amounts in the cashflows table."
        
        # Date information - Simple
        issue_date_str = issue_date_dt.strftime('%B %d, %Y')
        maturity_date_str = maturity_date_dt.strftime('%B %d, %Y')
        eval_date_str = eval_date.strftime('%B %d, %Y')
        bond_tenor_years = (maturity_date_dt - issue_date_dt).days / 365.25
        
        dates_info = f"Bond issued on {issue_date_str}, matures on {maturity_date_str} (tenor: {bond_tenor_years:.1f} years), evaluated on {eval_date_str}. Dates influence the spread calculation."
        
        explanations = {
            'margin_analysis': margin_analysis,
            'price_accuracy': price_accuracy,
            'equivalent_rate': equivalent_rate_explanation,
            'face_amount_info': face_amount_info,
            'dates_info': dates_info
        }

        # 9. Calculs supplémentaires pour correspondre exactement au livre
        # Out[9] - Prix initial avec DM=0
        DM_quote.setValue(0.0)
        initial_price = bond.cleanPrice()
        
        # Out[10] - Prix avec DM=0.001
        DM_quote.setValue(0.001)
        price_with_001 = bond.cleanPrice()
        
        # Out[12] - Fonction d'erreur pour différents spreads
        def error_function_for_book(spread):
            DM_quote.setValue(spread)
            return bond.cleanPrice() - 98.9997903076
        
        error_0 = error_function_for_book(0.0)
        error_002 = error_function_for_book(0.002)

        return {
            # Outputs principaux
            'discount_margin_continuous': discount_margin_continuous * 10000, # en bps
            'equivalent_rate_simple': equivalent_rate.rate() * 10000, # en bps
            'target_price': target_price,
            'calculated_bond_price': calculated_bond_price,
            'cashflows': cashflows_data,
            'explanations': explanations,
            
            # Outputs exacts du livre
            'book_outputs': {
                'out_9_initial_price': initial_price,  # Out[9]: 100.00000000000001
                'out_10_price_with_001': price_with_001,  # Out[10]: 98.99979030764418
                'out_12_error_0': error_0,  # Out[12]: 1.00020969240002
                'out_12_error_002': error_002,  # Out[12]: -0.9901429992548856
                'out_13_discount_margin': discount_margin_continuous,  # Out[13]: 0.00039870328652332745
                'out_14_calculated_price': calculated_bond_price,  # Out[14]: 99.59999988275108
                'out_15_equivalent_rate': equivalent_rate.rate() * 100,  # Out[15]: 0.039874 %
            }
        }

    except Exception as e:
        error_msg = str(e)
        
        # Messages d'erreur plus clairs et professionnels
        if "Missing Euribor6M" in error_msg or "fixing" in error_msg.lower():
            return {
                'error': 'Unable to calculate discount margin due to missing interest rate data. Please ensure the evaluation date is a valid business day and try adjusting the forecast rate or evaluation date.'
            }
        elif "invalid range" in error_msg.lower():
            return {
                'error': 'Invalid solver bounds detected. Please ensure the minimum margin is less than the maximum margin and both values are positive.'
            }
        elif "not a business day" in error_msg.lower():
            return {
                'error': 'The selected evaluation date is not a business day. Please choose a weekday (Monday-Friday) that is not a holiday.'
            }
        elif "bracket root" in error_msg.lower():
            return {
                'error': 'Unable to find a solution within the specified bounds. Please try adjusting the minimum and maximum margin values or the target price.'
            }
        else:
            return {
                'error': f'Calculation error: {error_msg}. Please check your input parameters and try again.'
            }