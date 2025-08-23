import QuantLib as ql
import numpy as np

def calculate_swaption_metrics(
    # --- Paramètres du formulaire ---
    option_type_str: str,
    maturity_years: int,
    swap_tenor_years: int,
    strike_rate_pct: float,
    notional: float,
    volatility_pct: float,
    # --- Paramètres de marché ---
    curve_rate_pct: float
) -> dict:
    """
    Calcule la NPV et la volatilité implicite d'une swaption européenne.
    Toute la logique QuantLib est encapsulée ici.
    """
    
    # 1. Conversion et préparation des paramètres
    option_type = ql.Option.Call if option_type_str == 'Call' else ql.Option.Put
    strike_rate = strike_rate_pct / 100
    volatility = volatility_pct / 100
    curve_rate = curve_rate_pct / 100

    # 2. Définition des conventions et de la date de calcul
    calculation_date = ql.Date(15, 1, 2016)
    ql.Settings.instance().evaluationDate = calculation_date
    calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    day_count = ql.Actual365Fixed()

    # 3. Construction de la courbe et de l'index
    term_structure = ql.YieldTermStructureHandle(
        ql.FlatForward(calculation_date, curve_rate, day_count)
    )
    libor_index = ql.USDLibor(ql.Period('6M'), term_structure)

    # 4. Construction de la Swaption
    option_maturity_date = calendar.advance(calculation_date, ql.Period(maturity_years, ql.Years))
    swap_maturity_date = calendar.advance(option_maturity_date, ql.Period(swap_tenor_years, ql.Years))
    
    fixed_schedule = ql.Schedule(
        option_maturity_date, swap_maturity_date, ql.Period('1Y'), calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False
    )
    float_schedule = ql.Schedule(
        option_maturity_date, swap_maturity_date, ql.Period('6M'), calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing, ql.DateGeneration.Forward, False
    )

    underlying_swap = ql.VanillaSwap(
        ql.VanillaSwap.Payer, notional,
        fixed_schedule, strike_rate, ql.Thirty360(ql.Thirty360.BondBasis),
        float_schedule, libor_index, 0.0, ql.Actual360()
    )
    
    exercise = ql.EuropeanExercise(option_maturity_date)
    swaption = ql.Swaption(underlying_swap, exercise)

    # 5. Pricing
    swaption_engine = ql.BlackSwaptionEngine(term_structure, ql.QuoteHandle(ql.SimpleQuote(volatility)))
    swaption.setPricingEngine(swaption_engine)

    # 6. Calcul et retour des résultats
    results = {
        'npv': np.round(swaption.NPV(), 4),
        'implied_volatility': np.round(swaption.impliedVolatility(swaption.NPV(), term_structure, 0.1) * 100, 4) # En %
    }
    return results