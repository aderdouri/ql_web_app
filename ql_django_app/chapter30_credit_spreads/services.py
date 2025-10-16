import QuantLib as ql
import datetime

def setup_bond_and_curve(data):
    """
    Construit la courbe de taux de base et l'obligation.
    Appelé une seule fois au chargement de la page.
    """
    try:
        # 1. Configuration initiale
        eval_date = data['evaluation_date']
        calc_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = calc_date

        # 2. Création de la courbe de base (Flat Treasury Yield Curve)
        flat_rate = ql.SimpleQuote(data['base_rate'] / 100.0)
        rate_handle = ql.QuoteHandle(flat_rate)
        day_count = ql.Actual360()
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        ts_yield = ql.FlatForward(calc_date, rate_handle, day_count)
        ts_handle = ql.YieldTermStructureHandle(ts_yield)

        # 3. Création de l'obligation
        issue_date = ql.Date(data['issue_date'].day, data['issue_date'].month, data['issue_date'].year)
        maturity_date = ql.Date(data['maturity_date'].day, data['maturity_date'].month, data['maturity_date'].year)
        tenor = ql.Period(ql.Semiannual)
        
        schedule = ql.Schedule(issue_date, maturity_date, tenor, calendar,
                               ql.Unadjusted, ql.Unadjusted,
                               ql.DateGeneration.Backward, False)
        
        coupons = [data['coupon_rate'] / 100.0]
        bond_day_count = ql.Thirty360(ql.Thirty360.BondBasis)
        
        fixed_rate_bond = ql.FixedRateBond(0, 100.0, schedule, coupons, bond_day_count)

        # 4. Calcul du prix initial (sans spread)
        bond_engine = ql.DiscountingBondEngine(ts_handle)
        fixed_rate_bond.setPricingEngine(bond_engine)
        initial_npv = fixed_rate_bond.NPV()

        # On retourne les objets QuantLib nécessaires pour les calculs suivants
        return {
            'initial_npv': initial_npv,
            'quantlib_objects': {
                'bond': fixed_rate_bond,
                'base_curve_handle': ts_handle,
                'flat_rate_quote': flat_rate,
                'calendar': calendar
            }
        }
    except Exception as e:
        return {'error': str(e)}


def price_bond_with_spread(ql_objects, data):
    """
    Re-price l'obligation en utilisant la méthode de spread choisie.
    """
    try:
        calendar = ql_objects['calendar']
        spread_method = data['spread_method']
        
        # 1. Configuration initiale avec les nouveaux paramètres
        eval_date = data['evaluation_date']
        calc_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = calc_date

        # 2. Création de la courbe de base avec le nouveau taux
        flat_rate = ql.SimpleQuote(data['base_rate'] / 100.0)
        rate_handle = ql.QuoteHandle(flat_rate)
        day_count = ql.Actual360()
        ts_yield = ql.FlatForward(calc_date, rate_handle, day_count)
        ts_handle = ql.YieldTermStructureHandle(ts_yield)

        # 3. Création de l'obligation avec les nouveaux paramètres
        issue_date = ql.Date(data['issue_date'].day, data['issue_date'].month, data['issue_date'].year)
        maturity_date = ql.Date(data['maturity_date'].day, data['maturity_date'].month, data['maturity_date'].year)
        tenor = ql.Period(ql.Semiannual)
        
        schedule = ql.Schedule(issue_date, maturity_date, tenor, calendar,
                               ql.Unadjusted, ql.Unadjusted,
                               ql.DateGeneration.Backward, False)
        
        coupons = [data['coupon_rate'] / 100.0]
        bond_day_count = ql.Thirty360(ql.Thirty360.BondBasis)
        
        fixed_rate_bond = ql.FixedRateBond(0, 100.0, schedule, coupons, bond_day_count)

        # 4. Calcul du prix initial (sans spread) avec les nouveaux paramètres
        bond_engine = ql.DiscountingBondEngine(ts_handle)
        fixed_rate_bond.setPricingEngine(bond_engine)
        initial_npv = fixed_rate_bond.NPV()

        if spread_method == 'direct_shock':
            # Méthode 1: Choc direct sur la courbe plate
            spread_bps = data['spread1']
            print(f"Direct Shock: Adding {spread_bps} bps to base rate {data['base_rate']}%")
            flat_rate.setValue(flat_rate.value() + spread_bps / 10000.0)
            # Le prix est automatiquement mis à jour par l'observer
            npv = fixed_rate_bond.NPV()
            print(f"Direct Shock NPV: {npv}")

        elif spread_method == 'parallel_shift':
            # Méthode 2: Décalage parallèle avec ZeroSpreadedTermStructure
            spread_bps = data['spread1']
            print(f"Parallel Shift: Applying {spread_bps} bps spread to entire curve")
            spread_quote = ql.SimpleQuote(spread_bps / 10000.0)
            spread_handle = ql.QuoteHandle(spread_quote)
            spreaded_curve_handle = ql.YieldTermStructureHandle(
                ql.ZeroSpreadedTermStructure(ts_handle, spread_handle)
            )
            bond_engine = ql.DiscountingBondEngine(spreaded_curve_handle)
            fixed_rate_bond.setPricingEngine(bond_engine)
            npv = fixed_rate_bond.NPV()
            print(f"Parallel Shift NPV: {npv}")

        elif spread_method == 'non_parallel_shift':
            # Méthode 3: Décalage non parallèle
            spread1_bps = data['spread1']
            spread2_bps = data['spread2']
            print(f"Non-Parallel Shift: {spread1_bps} bps to {spread2_bps} bps across maturities")
            
            spread_quote1 = ql.SimpleQuote(spread1_bps / 10000.0)
            spread_quote2 = ql.SimpleQuote(spread2_bps / 10000.0)
            
            calc_date = ql.Settings.instance().evaluationDate
            end_date = calendar.advance(calc_date, ql.Period(50, ql.Years)) # Très longue date
            
            spreaded_curve = ql.SpreadedLinearZeroInterpolatedTermStructure(
                ts_handle,
                [ql.QuoteHandle(spread_quote1), ql.QuoteHandle(spread_quote2)],
                [calc_date, end_date]
            )
            spreaded_curve_handle = ql.YieldTermStructureHandle(spreaded_curve)
            bond_engine = ql.DiscountingBondEngine(spreaded_curve_handle)
            fixed_rate_bond.setPricingEngine(bond_engine)
            npv = fixed_rate_bond.NPV()
            print(f"Non-Parallel Shift NPV: {npv}")
        
        else:
            return {'error': 'Unknown spread method'}

        return {
            'initial_npv': initial_npv,
            'npv_with_spread': npv
        }

    except Exception as e:
        return {'error': str(e)}
