import QuantLib as ql
from datetime import date, timedelta
import numpy as np

def calculate_price_history(bond_params: dict, date_range: dict):
    
    start_date_py = date_range['start_date']
    end_date_py = date_range['end_date']
    
    coupon_rate = bond_params['coupon_rate_pct'] / 100.0
    maturity_in_years = bond_params['maturity_years']

    # Paramètres fixes
    settlement_days = 3
    face_amount = 100.0
    calendar = ql.TARGET()
    day_count = ql.Thirty360(ql.Thirty360.BondBasis)
    
    # L'obligation est créée dynamiquement en fonction des entrées utilisateur
    bond_start_date_ql = ql.Date(start_date_py.day, start_date_py.month, start_date_py.year)
    bond_maturity_date_ql = calendar.advance(bond_start_date_ql, ql.Period(maturity_in_years, ql.Years))
    
    schedule = ql.Schedule(
        bond_start_date_ql, bond_maturity_date_ql, ql.Period(ql.Semiannual), calendar,
        ql.Following, ql.Following, ql.DateGeneration.Backward, False
    )
    
    bond = ql.FixedRateBond(
        settlement_days, face_amount, schedule, [coupon_rate], day_count
    )

    # 2. On utilise un RelinkableHandle pour la courbe de taux
    discount_handle = ql.RelinkableYieldTermStructureHandle()
    bond.setPricingEngine(ql.DiscountingBondEngine(discount_handle))
    
    # 3. Boucle à travers la plage de dates définie par l'utilisateur
    price_history = []
    current_date_py = end_date_py
    
    base_rates = np.array([0.007, 0.010, 0.012, 0.013, 0.014, 0.016, 0.017, 0.018, 0.020, 0.021, 0.022])
    
    while current_date_py >= start_date_py:
        eval_date_ql = ql.Date(current_date_py.day, current_date_py.month, current_date_py.year)
        
        # On ne calcule que si l'évaluation est avant la maturité
        if eval_date_ql < bond.maturityDate():
            ql.Settings.instance().evaluationDate = eval_date_ql
            nodes = [eval_date_ql + ql.Period(i, ql.Years) for i in range(11)]
            simulated_rates = base_rates * np.random.normal(1.0, 0.005, base_rates.shape)
            daily_curve = ql.ZeroCurve(nodes, list(simulated_rates), ql.Actual360())
            discount_handle.linkTo(daily_curve)
            
            try:
                price = bond.cleanPrice()
                if not np.isnan(price):
                    price_history.append({'x': current_date_py.isoformat(), 'y': round(price, 4)})
            except Exception as e:
                print(f"Could not price bond on {eval_date_ql}: {e}")

        current_date_py -= timedelta(days=1)

    return sorted(price_history, key=lambda x: x['x'])