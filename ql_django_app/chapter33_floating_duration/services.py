import QuantLib as ql
import datetime

def analyze_frn_duration(data):
    """
    Reproduces the analysis from Chapter 33 with robust handling of index fixings.
    """
    try:
        # 1. Setup from form data
        eval_date = data['evaluation_date']
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = today

        forecast_rate = data['forecast_rate']
        yield_rate = data['yield_rate']
        dy = data['dy']

        # 2. Construction de l'obligation et des courbes
        forecast_curve = ql.RelinkableYieldTermStructureHandle()
        forecast_curve.linkTo(ql.FlatForward(today, forecast_rate, ql.Actual360(), ql.Compounded, ql.Semiannual))
        
        index = ql.Euribor6M(forecast_curve)
        
        # ==============================================================================
        # CORRECTION : On ajoute une série de fixings historiques pour rendre le calcul robuste
        # ==============================================================================
        # On nettoie les anciens fixings pour éviter les conflits
        ql.IndexManager.instance().clearHistories()
        
        # Validation des dates
        issue_date = ql.Date(8, 8, 2014)
        maturity_date = ql.Date(8, 8, 2019)
        
        if today < issue_date:
            return {'error': 'Evaluation date cannot be before the bond issue date.'}
        if today > maturity_date:
            return {'error': 'Evaluation date cannot be after the bond maturity date.'}
        
        # On ajoute des fixings pour chaque jour sur une période passée
        target_calendar = ql.TARGET()
        past_date = today - ql.Period(2, ql.Years)  # On remonte 2 ans en arrière
        while past_date <= today:
            if target_calendar.isBusinessDay(past_date):
                index.addFixing(past_date, 0.002)
            past_date += ql.Period(1, ql.Days)

        schedule = ql.Schedule(issue_date, maturity_date, ql.Period(ql.Semiannual), ql.TARGET(),
                               ql.Following, ql.Following, ql.DateGeneration.Backward, False)
        
        bond = ql.FloatingRateBond(3, 100.0, schedule, index, ql.Actual360())

        # 3. Calcul INCORRECT de la duration
        y_incorrect = ql.InterestRate(yield_rate, ql.Actual360(), ql.Compounded, ql.Semiannual)
        duration_incorrect = ql.BondFunctions.duration(bond, y_incorrect, ql.Duration.Modified)
        
        y_quote_incorrect = ql.SimpleQuote(yield_rate)
        yield_curve_incorrect = ql.FlatForward(bond.settlementDate(), ql.QuoteHandle(y_quote_incorrect),
                                               ql.Actual360(), ql.Compounded, ql.Semiannual)
        bond.setPricingEngine(ql.DiscountingBondEngine(ql.YieldTermStructureHandle(yield_curve_incorrect)))
        P_incorrect = bond.dirtyPrice()
        
        # Calcul avec yield + dy (P+)
        y_quote_incorrect.setValue(yield_rate + dy)
        P_p_incorrect = bond.dirtyPrice()
        # Récupérer les cashflows et discounts pour P+
        cfs_p_incorrect = []
        discounts_p_incorrect = []
        for cf in bond.cashflows():
            cfs_p_incorrect.append(cf.amount())
            discounts_p_incorrect.append(yield_curve_incorrect.discount(cf.date()))
        
        # Calcul avec yield - dy (P-)
        y_quote_incorrect.setValue(yield_rate - dy)
        P_m_incorrect = bond.dirtyPrice()
        # Récupérer les cashflows et discounts pour P-
        cfs_m_incorrect = []
        discounts_m_incorrect = []
        for cf in bond.cashflows():
            cfs_m_incorrect.append(cf.amount())
            discounts_m_incorrect.append(yield_curve_incorrect.discount(cf.date()))
        
        y_quote_incorrect.setValue(yield_rate)
        duration_numeric_incorrect = -(1 / P_incorrect) * (P_p_incorrect - P_m_incorrect) / (2 * dy)
        
        # 4. La SOLUTION : lier la courbe de prévision
        y_quote_correct = ql.SimpleQuote(yield_rate)
        yield_curve_correct = ql.FlatForward(bond.settlementDate(), ql.QuoteHandle(y_quote_correct),
                                             ql.Actual360(), ql.Compounded, ql.Semiannual)
        forecast_curve.linkTo(yield_curve_correct)
        bond.setPricingEngine(ql.DiscountingBondEngine(ql.YieldTermStructureHandle(yield_curve_correct)))
        P_correct = bond.dirtyPrice()
        
        # Calcul avec yield + dy (P+) - CORRECT
        y_quote_correct.setValue(yield_rate + dy)
        P_p_correct = bond.dirtyPrice()
        # Récupérer les cashflows et discounts pour P+ (correct)
        cfs_p_correct = []
        discounts_p_correct = []
        for cf in bond.cashflows():
            cfs_p_correct.append(cf.amount())
            discounts_p_correct.append(yield_curve_correct.discount(cf.date()))
        
        # Calcul avec yield - dy (P-) - CORRECT
        y_quote_correct.setValue(yield_rate - dy)
        P_m_correct = bond.dirtyPrice()
        # Récupérer les cashflows et discounts pour P- (correct)
        cfs_m_correct = []
        discounts_m_correct = []
        for cf in bond.cashflows():
            cfs_m_correct.append(cf.amount())
            discounts_m_correct.append(yield_curve_correct.discount(cf.date()))
        
        y_quote_correct.setValue(yield_rate)
        duration_correct = -(1 / P_correct) * (P_p_correct - P_m_correct) / (2 * dy)

        # Récupérer les cashflows de base (avec yield normal)
        y_quote_correct.setValue(yield_rate)
        base_cashflows = []
        base_discounts = []
        for cf in bond.cashflows():
            base_cashflows.append(cf.amount())
            base_discounts.append(yield_curve_correct.discount(cf.date()))

        return {
            'duration_incorrect': duration_incorrect,
            'duration_numeric_incorrect': duration_numeric_incorrect,
            'analysis': {
                'P_p_incorrect': P_p_incorrect, 
                'P_m_incorrect': P_m_incorrect,
                'cfs_p_incorrect': cfs_p_incorrect,
                'discounts_p_incorrect': discounts_p_incorrect,
                'cfs_m_incorrect': cfs_m_incorrect,
                'discounts_m_incorrect': discounts_m_incorrect
            },
            'duration_correct': duration_correct,
            'analysis_correct': {
                'P_p_correct': P_p_correct, 
                'P_m_correct': P_m_correct,
                'cfs_p_correct': cfs_p_correct,
                'discounts_p_correct': discounts_p_correct,
                'cfs_m_correct': cfs_m_correct,
                'discounts_m_correct': discounts_m_correct
            },
            'cashflows': [{'date': cf.date().ISO(), 'amount': cf.amount()} for cf in bond.cashflows()],
            'base_cashflows': base_cashflows,
            'base_discounts': base_discounts
        }

    except Exception as e:
        return {'error': str(e)}