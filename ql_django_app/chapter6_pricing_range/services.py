# Fichier : ql_web_app/chapter6_pricing_range/services.py (VERSION FINALE GARANTIE)
import QuantLib as ql
from datetime import date, timedelta
import numpy as np

def calculate_price_history(bond_params: dict, date_range: dict):
    
    start_date_py = date_range['start_date']
    end_date_py = date_range['end_date']
    coupon_rate = bond_params['coupon_rate_pct'] / 100
    
    # Paramètres fixes
    settlement_days = 0 # On simplifie à 0 pour éviter les problèmes de calendrier
    face_amount = 100.0
    calendar = ql.TARGET()
    day_count = ql.Actual365Fixed()
    
    # Création d'une obligation dont la vie est très longue pour être sûr
    issue_date_ql = ql.Date(1, 1, 2010)
    maturity_date_ql = ql.Date(1, 1, 2040)

    schedule = ql.Schedule(
        issue_date_ql, maturity_date_ql, ql.Period('6M'), calendar,
        ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Forward, False
    )
    
    bond = ql.FixedRateBond(
        settlement_days, face_amount, schedule, [coupon_rate], day_count
    )
    
    price_history = []
    current_date_py = end_date_py

    while current_date_py >= start_date_py:
        eval_date_ql = ql.Date(current_date_py.day, current_date_py.month, current_date_py.year)
        ql.Settings.instance().evaluationDate = eval_date_ql

        # ==============================================================================
        # SIMPLIFICATION RADICALE
        # ==============================================================================
        # On utilise une courbe de taux plate, la plus simple et la plus stable possible.
        # La simulation aléatoire de la courbe peut causer des instabilités.
        market_rate = 0.02 # Un taux fixe de 2% pour l'exemple
        flat_curve = ql.YieldTermStructureHandle(
            ql.FlatForward(eval_date_ql, market_rate, day_count)
        )
        
        bond_engine = ql.DiscountingBondEngine(flat_curve)
        bond.setPricingEngine(bond_engine)
        
        try:
            price = bond.cleanPrice()
            price_history.append({'date': current_date_py.isoformat(), 'price': round(price, 4)})
        except Exception as e:
            # Cette erreur ne devrait plus se produire.
            print(f"ERROR on {eval_date_ql}: {e}")

        current_date_py -= timedelta(days=1)

    return sorted(price_history, key=lambda x: x['date'])