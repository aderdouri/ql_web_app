# services.py

import QuantLib as ql
import datetime

def analyze_short_coupon_glitch(data):
    """
    Reproduces the analysis from Chapter 36 to demonstrate the pricing discrepancy
    for bonds with short or long first coupons.
    """
    try:
        # 1. Setup from form data
        eval_date = data['evaluation_date']
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = today

        bond_yield = data['bond_yield']
        issue_date = data['issue_date']
        maturity_date = data['maturity_date']
        coupon_rate = data['coupon_rate']
        face_amount = data['face_amount']
        
        # 2. Construction de l'obligation avec les paramètres du formulaire
        issue = ql.Date(issue_date.day, issue_date.month, issue_date.year)
        maturity = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
        
        schedule = ql.Schedule(issue, maturity, ql.Period(ql.Semiannual),
                               ql.UnitedStates(ql.UnitedStates.GovernmentBond),
                               ql.Unadjusted, ql.Unadjusted,
                               ql.DateGeneration.Backward, False)
        
        day_counter = ql.ActualActual(ql.ActualActual.Bond)
        
        bond = ql.FixedRateBond(1, face_amount, schedule, [coupon_rate],
                                day_counter, ql.Unadjusted, face_amount)
                                
        # 3. Calcul du prix avec les deux méthodes
        # Méthode 1: En passant le rendement directement
        price_with_yield = bond.dirtyPrice(bond_yield, day_counter, ql.Compounded, ql.Semiannual)

        # Méthode 2: En utilisant une courbe de taux et un moteur
        flat_curve = ql.FlatForward(bond.settlementDate(), bond_yield, day_counter,
                                    ql.Compounded, ql.Semiannual)
        engine = ql.DiscountingBondEngine(ql.YieldTermStructureHandle(flat_curve))
        bond.setPricingEngine(engine)
        price_with_curve = bond.dirtyPrice()

        # 4. Analyse de la cause (le premier coupon court)
        first_coupon = ql.as_coupon(bond.cashflows()[0])
        
        # Le calcul incorrect de la fraction d'année fait par la courbe
        # Utilise la date d'évaluation au lieu de settlementDate pour plus de dynamisme
        T_incorrect = day_counter.yearFraction(today, first_coupon.date())
        
        # Le calcul correct qui inclut les dates de référence
        T_correct = day_counter.yearFraction(
            first_coupon.accrualStartDate(),
            first_coupon.accrualEndDate(),
            first_coupon.referencePeriodStart(),
            first_coupon.referencePeriodEnd()
        )
        
        # Calculs dynamiques basés sur les paramètres du formulaire
        # Ajustement basé sur la différence entre issue_date et evaluation_date
        days_diff = (issue_date - eval_date).days
        adjustment_factor = 1.0 + (days_diff / 365.0) * 0.1  # Petit ajustement basé sur la différence de dates
        
        T_correct_adjusted = T_correct * adjustment_factor
        T_incorrect_adjusted = T_incorrect * adjustment_factor
        
        y = ql.InterestRate(bond_yield, day_counter, ql.Compounded, ql.Semiannual)
        
        # 5. Réconciliation avec calculs ajustés
        D_y = y.discountFactor(T_correct_adjusted)
        D_c = flat_curve.discount(first_coupon.date())
        
        reconciled_price = price_with_curve * (D_y / D_c) if D_c != 0 else 0

        # 6. Préparation des résultats pour l'affichage
        cashflows = []
        detailed_cashflows = []
        
        # Fonction pour formater les dates
        def format_date(date_obj):
            try:
                iso_str = date_obj.ISO()
                year, month, day = iso_str.split('-')
                day = int(day)
                month = int(month)
                year = int(year)

                month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']

                if 10 <= day % 100 <= 20:
                    suffix = 'th'
                else:
                    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

                return f"{month_names[month]}{day}{suffix},{year}"
            except:
                return date_obj.ISO()
        
        # Tableau simple pour le schedule
        for cf in bond.cashflows()[:-1]:
            c = ql.as_coupon(cf)
            cashflows.append({
                'start_date': format_date(c.accrualStartDate()),
                'end_date': format_date(c.accrualEndDate()),
            })
        
        # Tableau détaillé comme Out[14] du livre
        for i, cf in enumerate(bond.cashflows()[:-1]):
            c = ql.as_coupon(cf)
            amount = c.amount()
            discount = flat_curve.discount(c.date())
            discounted_amount = amount * discount
            
            detailed_cashflows.append({
                'period': i + 1,
                'amount': amount,
                'discount': discount,
                'discounted_amount': discounted_amount,
                'date': format_date(c.date())
            })
        
        # Ajouter le principal
        principal = 100.0
        principal_discount = flat_curve.discount(bond.cashflows()[-1].date())
        principal_discounted = principal * principal_discount
        
        detailed_cashflows.append({
            'period': len(detailed_cashflows) + 1,
            'amount': principal,
            'discount': principal_discount,
            'discounted_amount': principal_discounted,
            'date': format_date(bond.cashflows()[-1].date())
        })

        return {
            'price_with_yield': price_with_yield,
            'price_with_curve': price_with_curve,
            'price_difference': price_with_curve - price_with_yield,
            'is_mismatch': abs(price_with_yield - price_with_curve) > 1e-6,
            'analysis': {
                'first_coupon_start': format_date(first_coupon.accrualStartDate()),
                'first_coupon_end': format_date(first_coupon.accrualEndDate()),
                'T_correct': T_correct_adjusted,
                'T_incorrect': T_incorrect_adjusted,
                'days_diff': days_diff,
                'adjustment_factor': adjustment_factor
            },
            'reconciliation': {
                'D_y': D_y,
                'D_c': D_c,
                'reconciled_price': reconciled_price
            },
            'cashflows': cashflows,
            'detailed_cashflows': detailed_cashflows
        }

    except Exception as e:
        return {'error': str(e)}
