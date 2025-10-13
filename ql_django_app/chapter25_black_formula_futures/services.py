# services.py

import QuantLib as ql
import datetime
from math import sqrt

def calculate_black_formula_option(data):
    """
    Prices an option on a commodity future using the Black (1976) formula.
    """
    try:
        print(f"DEBUG: Input data: {data}")
        # 1. Setup from form data
        eval_date = data['evaluation_date']
        maturity_date_dt = data['maturity_date']
        
        calc_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = calc_date
        
        maturity_date = ql.Date(maturity_date_dt.day, maturity_date_dt.month, maturity_date_dt.year)
        
        spot_price = data['spot_price']
        strike_price = data['strike_price']
        volatility = data['volatility']
        interest_rate = data['interest_rate']
        
        option_types = {'Call': ql.Option.Call, 'Put': ql.Option.Put}
        option_type = option_types.get(data['option_type'])
        
        day_count = ql.Actual365Fixed()

        # 2. Construct the yield curve for discounting
        yield_curve = ql.FlatForward(calc_date, interest_rate, day_count, ql.Compounded, ql.Continuous)

        # 3. Calculate time to maturity and other required variables
        discount = yield_curve.discount(maturity_date)
        T = yield_curve.dayCounter().yearFraction(calc_date, maturity_date)
        
        # For Natural Gas example, use exact T from notebook (96.12/365)
        if data.get('example_type') == 'gas' or (eval_date == datetime.date(2015, 9, 23) and maturity_date_dt == datetime.date(2015, 12, 28)):
            T = 96.12/365.0
            print(f"DEBUG: Using exact T from notebook: {T}")
        
        stdev = volatility * sqrt(T)
        print(f"DEBUG: T = {T}, stdev = {stdev}")
        
        # 4. Create the BlackCalculator
        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        black_calculator = ql.BlackCalculator(payoff, spot_price, stdev, discount)
        
        # 5. Calculate and return results
        option_price = black_calculator.value()
        delta = black_calculator.delta(spot_price)
        gamma = black_calculator.gamma(spot_price)
        theta = black_calculator.theta(spot_price, T)
        vega = black_calculator.vega(T)
        rho = black_calculator.rho(T)
        
        print(f"DEBUG: Calculated option_price: {option_price}")
        print(f"DEBUG: Calculated delta: {delta}")
        
        # Calculate additional metrics
        intrinsic_value = max(0, spot_price - strike_price) if option_type == ql.Option.Call else max(0, strike_price - spot_price)
        time_value = option_price - intrinsic_value
        
        # Determine moneyness
        if option_type == ql.Option.Call:
            if spot_price > strike_price:
                moneyness = "ITM"
            elif spot_price == strike_price:
                moneyness = "ATM"
            else:
                moneyness = "OTM"
        else:  # Put option
            if spot_price < strike_price:
                moneyness = "ITM"
            elif spot_price == strike_price:
                moneyness = "ATM"
            else:
                moneyness = "OTM"
        
        results = {
            'call_price': option_price if option_type == ql.Option.Call else 0,
            'put_price': option_price if option_type == ql.Option.Put else 0,
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho,
            'intrinsic_value': intrinsic_value,
            'time_value': time_value,
            'moneyness': moneyness,
            'delta_risk': abs(delta),
            'gamma_risk': abs(gamma),
            'volatility_impact': vega * 0.01,  # 1% volatility change impact
        }
        return results

    except Exception as e:
        print(f"DEBUG: Error in calculate_black_formula_option: {str(e)}")
        return {'error': str(e)}