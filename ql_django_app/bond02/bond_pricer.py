# your_app/bond_pricer.py

 
import QuantLib as ql
 
def price_fixed_rate_bond(
    evaluation_date,
    issue_date,
    maturity_date,
    coupon_rate,
    face_amount,
    market_yield,
    frequency,
    day_count_convention,
    settlement_days=2
):
    """
    Calcule le prix d'une obligation à taux fixe en utilisant QuantLib.
 
    Args:
        evaluation_date (ql.Date): La date d'évaluation.
        issue_date (ql.Date): La date d'émission.
        maturity_date (ql.Date): La date de maturité.
        coupon_rate (float): Le taux de coupon annuel (ex: 0.05 pour 5%).
        face_amount (float): La valeur faciale de l'obligation.
        market_yield (float): Le rendement de marché (ex: 0.04 pour 4%).
        frequency (ql.Frequency): La fréquence des coupons (ex: ql.Semiannual).
        day_count_convention (ql.DayCounter): La convention de décompte des jours.
        settlement_days (int): Le nombre de jours pour le règlement.
 
    Returns:
        dict: Un dictionnaire contenant les résultats du pricing.
    """
    
    # 1. Configuration de l'environnement QuantLib
    ql.Settings.instance().evaluationDate = evaluation_date
    calendar = ql.TARGET()
 
    # 2. Définition du schedule (échéancier des paiements)
    schedule = ql.Schedule(
        issue_date,
        maturity_date,
        ql.Period(frequency),
        calendar,
        ql.Unadjusted,
        ql.Unadjusted,
        ql.DateGeneration.Backward,
        False
    )
 
    # 3. Création de l'objet Obligation (Bond)
    bond = ql.FixedRateBond(
        settlement_days,
        face_amount,
        schedule,
        [coupon_rate],  # Le coupon est une liste
        day_count_convention,
        ql.ModifiedFollowing,
        100.0, # Redemption
        issue_date
    )
 
    # 4. Calcul du prix et des indicateurs
    # Nous utilisons les fonctions statiques de BondFunctions pour calculer le prix à partir du rendement
    # car c'est un cas d'usage très courant.
    
    # La convention de compounding est fixée à 'Compounded' ici pour l'exemple.
    compounding = ql.Compounded
 
    try:
        clean_price = ql.BondFunctions.cleanPrice(bond, market_yield, day_count_convention, compounding, frequency)
        accrued_amount = ql.BondFunctions.accruedAmount(bond, evaluation_date)
        dirty_price = clean_price + accrued_amount
        
        # Use the input market_yield as the calculated yield since we're pricing with it
        calculated_yield = market_yield
 
        return {
            "status": "success",
            "clean_price": clean_price,
            "accrued_amount": accrued_amount,
            "dirty_price": dirty_price,
            "yield": calculated_yield,
            "face_amount": face_amount
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
 