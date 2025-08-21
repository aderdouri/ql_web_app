# Fichier : ql_web_app/chapter_calibration/services.py
import QuantLib as ql
from collections import namedtuple
import math

def calibrate_short_rate_model(model_name: str):
    """
    Calibre un modèle de taux d'intérêt choisi par l'utilisateur sur un jeu de swaptions.
    """
    # --- 1. Setup commun (date, courbe, données de marché) ---
    today = ql.Date(15, ql.February, 2002)
    settlement = ql.Date(19, ql.February, 2002)
    ql.Settings.instance().evaluationDate = today
    term_structure = ql.YieldTermStructureHandle(
        ql.FlatForward(settlement, 0.04875825, ql.Actual365Fixed())
    )
    index = ql.Euribor1Y(term_structure)

    CalibrationData = namedtuple("CalibrationData", "start, length, volatility")
    data = [
        CalibrationData(1, 5, 0.1148), CalibrationData(2, 4, 0.1108),
        CalibrationData(3, 3, 0.1070), CalibrationData(4, 2, 0.1021),
        CalibrationData(5, 1, 0.1000)
    ]

    # --- 2. Sélection du modèle et du moteur de pricing ---
    model = None
    engine = None
    if model_name == 'HullWhite':
        model = ql.HullWhite(term_structure)
        engine = ql.JamshidianSwaptionEngine(model)
    elif model_name == 'BlackKarasinski':
        model = ql.BlackKarasinski(term_structure)
        engine = ql.TreeSwaptionEngine(model, 100)
    elif model_name == 'G2':
        model = ql.G2(term_structure)
        engine = ql.TreeSwaptionEngine(model, 25)
    else:
        raise ValueError("Modèle inconnu")
        
    # --- 3. Création des helpers de calibration ---
    swaptions = []
    for d in data:
        vol_handle = ql.QuoteHandle(ql.SimpleQuote(d.volatility))
        helper = ql.SwaptionHelper(ql.Period(d.start, ql.Years), ql.Period(d.length, ql.Years),
                                   vol_handle, index, ql.Period(1, ql.Years), ql.Actual360(),
                                   ql.Actual360(), term_structure)
        helper.setPricingEngine(engine)
        swaptions.append(helper)
        
    # --- 4. Processus de Calibration ---
    method = ql.LevenbergMarquardt()
    end_criteria = ql.EndCriteria(1000, 100, 1e-6, 1e-8, 1e-8)
    model.calibrate(swaptions, method, end_criteria)

    # --- 5. Formatage des résultats ---
    params = model.params()
    param_string = ""
    if model_name == 'HullWhite':
        param_string = f"a = {params[0]:.4f}, sigma = {params[1]:.4f}"
    elif model_name == 'BlackKarasinski':
        param_string = f"a = {params[0]:.4f}, sigma = {params[1]:.4f}"
    elif model_name == 'G2':
        param_string = f"a = {params[0]:.4f}, sigma = {params[1]:.4f}, b = {params[2]:.4f}, eta = {params[3]:.4f}, rho = {params[4]:.4f}"

    # Calcul de l'erreur
    errors = []
    cum_err = 0.0
    for i, s in enumerate(swaptions):
        model_price = s.modelValue()
        market_vol = data[i].volatility
        black_price = s.blackPrice(market_vol)
        rel_error = (model_price / black_price) - 1.0
        cum_err += rel_error * rel_error
        errors.append({
            'instrument': f"{data[i].start}Y into {data[i].length}Y",
            'market_vol': f"{market_vol*100:.2f}%",
            'model_price': f"{model_price:.4f}",
            'rel_error': f"{rel_error*100:.2f}%"
        })
    
    rmse_error = math.sqrt(cum_err)

    return {
        'model_name': model_name,
        'params': param_string,
        'rmse_error': round(rmse_error, 6),
        'errors': errors
    }