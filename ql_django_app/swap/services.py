import QuantLib as ql
import numpy as np

def calculate_vanilla_swap_metrics(
    # --- Paramètres du formulaire ---
    notional: float,
    maturity_years: int,
    fixed_rate_pct: float,
    float_spread_pct: float,
    # --- Paramètres de marché (pourrait aussi venir d'un formulaire) ---
    discount_curve_rate_pct: float,
    libor_curve_rate_pct: float
) -> dict:
    """
    Calcule la NPV et d'autres métriques pour un swap de taux d'intérêt vanille.
    Toute la logique QuantLib est encapsulée ici.
    """
    
    # 1. Conversion des pourcentages et préparation des paramètres
    fixed_rate = fixed_rate_pct / 100
    float_spread = float_spread_pct / 100
    discount_curve_rate = discount_curve_rate_pct / 100
    libor_curve_rate = libor_curve_rate_pct / 100

    # 2. Définition des conventions et de la date de calcul
    calculation_date = ql.Date(15, 1, 2016) # Exemple de date
    ql.Settings.instance().evaluationDate = calculation_date
    
    # 3. Construction des courbes (yield curves)
    day_count = ql.Actual365Fixed()
    discount_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, discount_curve_rate, day_count)
    )
    libor_curve = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, libor_curve_rate, day_count)
    )

    # 4. Construction de l'instrument Swap
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    settle_date = calendar.advance(calculation_date, ql.Period('2D'))
    maturity_date = calendar.advance(settle_date, ql.Period(maturity_years, ql.Years))

    # Schedules pour les deux jambes
    fixed_leg_tenor = ql.Period('6M')
    float_leg_tenor = ql.Period('3M')
    
    fixed_schedule = ql.Schedule(
        settle_date, maturity_date, fixed_leg_tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, 
        ql.DateGeneration.Forward, False
    )
    float_schedule = ql.Schedule(
        settle_date, maturity_date, float_leg_tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, 
        ql.DateGeneration.Forward, False
    )
    
    # Index flottant
    libor_index = ql.USDLibor(ql.Period('3M'), libor_curve)

    # Création du swap
    vanilla_swap = ql.VanillaSwap(
        ql.VanillaSwap.Payer, notional,
        fixed_schedule, fixed_rate, ql.Thirty360(ql.Thirty360.BondBasis),
        float_schedule, libor_index, float_spread, ql.Actual360()
    )

    # 5. Pricing
    swap_engine = ql.DiscountingSwapEngine(discount_curve)
    vanilla_swap.setPricingEngine(swap_engine)

    # 6. Calcul et retour des résultats
    results = {
        'npv': np.round(vanilla_swap.NPV(), 4),
        'fair_rate': np.round(vanilla_swap.fairRate() * 100, 4), # En %
        'fair_spread': np.round(vanilla_swap.fairSpread() * 10000, 2), # En points de base (bps)
        'fixed_leg_bps': np.round(vanilla_swap.fixedLegBPS() / 100, 4),
        'floating_leg_bps': np.round(vanilla_swap.floatingLegBPS() / 100, 4),
    }
    return results