
import QuantLib as ql
import datetime
from math import sqrt

def analyze_day_count_glitch(data):
    """
    Reproduces the analysis from Chapter 27 to demonstrate the day count convention glitch.
    """
    try:
        # 1. Setup from form data
        eval_date = data['evaluation_date']
        exercise_date_form = data['exercise_date']
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        exercise_date = ql.Date(exercise_date_form.day, exercise_date_form.month, exercise_date_form.year)
        ql.Settings.instance().evaluationDate = today

        strike = data['strike_price']
        spot = data['spot_price']
        volatility_rate = data['volatility']
        risk_free_rate = data['risk_free_rate']
        
        # Mapping des conventions de décompte
        day_count_map = {
            'Actual365Fixed': ql.Actual365Fixed(),
            'Business252': ql.Business252(ql.UnitedStates(ql.UnitedStates.NYSE))
        }
        r_day_count = day_count_map.get(data['r_day_count'])
        sigma_day_count = day_count_map.get(data['sigma_day_count'])
        
        calendar = ql.UnitedStates(ql.UnitedStates.NYSE)

        # 2. Create the option and process with relinkable handles
        option = ql.EuropeanOption(ql.PlainVanillaPayoff(ql.Option.Call, strike), ql.EuropeanExercise(exercise_date))
        
        u_handle = ql.RelinkableQuoteHandle(ql.SimpleQuote(spot))
        r_handle = ql.RelinkableYieldTermStructureHandle()
        sigma_handle = ql.RelinkableBlackVolTermStructureHandle()
        
        process = ql.BlackScholesProcess(u_handle, r_handle, sigma_handle)

        # 3. Link handles to the curves with user-defined day counts
        r_handle.linkTo(ql.FlatForward(today, risk_free_rate, r_day_count))
        sigma_handle.linkTo(ql.BlackConstantVol(today, calendar, volatility_rate, sigma_day_count))
        
        # 4. Create the two pricing engines (exactly as in the book)
        analytic_engine = ql.AnalyticEuropeanEngine(process)
        fd_engine = ql.FdBlackScholesVanillaEngine(process, 1000, 1000)  # Same as book

        # 5. Calculate prices with both engines
        option.setPricingEngine(analytic_engine)
        analytic_price = option.NPV()
        
        option.setPricingEngine(fd_engine)
        fd_price = option.NPV()
        
        # 6. Perform the analysis to explain the glitch (exactly as in the book)
        T_vol = sigma_handle.dayCounter().yearFraction(today, exercise_date)
        T_grid = r_handle.dayCounter().yearFraction(today, exercise_date)
        correct_variance = sigma_handle.blackVariance(exercise_date, strike)
        fd_variance = (volatility_rate**2) * T_grid
        
        # 7. Calculate the workaround (exactly as in the book)
        synthetic_vol = sqrt(correct_variance / T_grid) if T_grid > 0 else 0
        
        # Re-price with the corrected volatility (exactly as in the book)
        corrected_sigma_handle = ql.RelinkableBlackVolTermStructureHandle()
        corrected_sigma_handle.linkTo(ql.BlackConstantVol(today, calendar, synthetic_vol, r_day_count))
        corrected_process = ql.BlackScholesProcess(u_handle, r_handle, corrected_sigma_handle)
        corrected_fd_engine = ql.FdBlackScholesVanillaEngine(corrected_process, 1000, 1000)
        
        option.setPricingEngine(corrected_fd_engine)
        fd_price_corrected = option.NPV()

        # Check if there's a day-count convention mismatch
        day_count_mismatch = data['r_day_count'] != data['sigma_day_count']
        significant_difference = abs(analytic_price - fd_price) > 1e-4
        
        return {
            'analytic_price': analytic_price,
            'fd_price': fd_price,
            'price_difference': analytic_price - fd_price,
            'is_mismatch': day_count_mismatch and significant_difference,
            'day_count_mismatch': day_count_mismatch,
            'analysis': {
                'T_vol': T_vol,
                'T_grid': T_grid,
                'time_difference': T_vol - T_grid,
                'correct_variance': correct_variance,
                'fd_variance': fd_variance,
                'variance_difference': correct_variance - fd_variance,
            },
            'workaround': {
                'synthetic_vol': synthetic_vol,
                'fd_price_corrected': fd_price_corrected,
            }
        }
    except Exception as e:
        return {'error': str(e)}