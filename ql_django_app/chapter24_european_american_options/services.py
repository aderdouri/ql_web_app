# services.py

import QuantLib as ql
import datetime

def price_options_and_convergence(data):
    """
    Price European and American options using Black-Scholes and Binomial Tree methods,
    and generate convergence data for plotting.
    """
    try:
        # 1. Setup from form data
        eval_date = data['evaluation_date']
        maturity_date_dt = data['maturity_date']
        
        calculation_date = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = calculation_date
        
        maturity_date = ql.Date(maturity_date_dt.day, maturity_date_dt.month, maturity_date_dt.year)
        spot_price = data['spot_price']
        strike_price = data['strike_price']
        volatility = data['volatility']
        dividend_rate = data['dividend_rate']
        risk_free_rate = data['risk_free_rate']
        
        # Debug: Print parameters to identify the issue
        print(f"DEBUG: Parameters - Spot: {spot_price}, Strike: {strike_price}, Vol: {volatility}")
        print(f"DEBUG: Rates - Risk-free: {risk_free_rate}, Dividend: {dividend_rate}")
        print(f"DEBUG: Dates - Eval: {eval_date}, Maturity: {maturity_date_dt}")
        print(f"DEBUG: Option type: {data.get('option_type', 'Unknown')}")
        
        # Validate parameters to avoid negative probability
        if volatility <= 0:
            return {'error': 'Volatility must be positive'}
        if spot_price <= 0:
            return {'error': 'Spot price must be positive'}
        if strike_price <= 0:
            return {'error': 'Strike price must be positive'}
        if maturity_date <= calculation_date:
            return {'error': 'Maturity date must be after calculation date'}
        
        # Check for extreme parameters that could cause negative probability
        time_to_maturity = (maturity_date - calculation_date) / 365.0
        if time_to_maturity <= 0:
            return {'error': 'Time to maturity must be positive'}
        
        # Check for reasonable parameter ranges
        if volatility > 2.0:  # 200% volatility is more conservative
            return {'error': 'Volatility too high (max 200%)'}
        if abs(risk_free_rate) > 0.5:  # 50% interest rate is more conservative
            return {'error': 'Risk-free rate too high (max 50%)'}
        if abs(dividend_rate) > 0.5:  # 50% dividend rate is more conservative
            return {'error': 'Dividend rate too high (max 50%)'}
        
        # Additional checks for negative probability prevention
        if volatility < 0.01:  # Too low volatility
            return {'error': 'Volatility too low (min 1%)'}
        if time_to_maturity < 0.01:  # Too short time
            return {'error': 'Time to maturity too short (min 1 day)'}
        if time_to_maturity > 10:  # Too long time
            return {'error': 'Time to maturity too long (max 10 years)'}
        
        option_types = {'Call': ql.Option.Call, 'Put': ql.Option.Put}
        option_type = option_types.get(data['option_type'])
        
        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)

        # 2. Construct the European option
        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        european_exercise = ql.EuropeanExercise(maturity_date)
        european_option = ql.VanillaOption(payoff, european_exercise)
        
        # 3. Construct the American option
        american_exercise = ql.AmericanExercise(calculation_date, maturity_date)
        american_option = ql.VanillaOption(payoff, american_exercise)

        # 4. Construct the Black-Scholes-Merton process
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
        flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, risk_free_rate, day_count))
        dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, dividend_rate, day_count))
        flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
        bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

        # 5. Calculate the theoretical Black-Scholes price for the European option
        european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
        bs_price = european_option.NPV()

        # 6. Define the binomial pricing function with robust error handling
        def binomial_price(option, bsm_process, steps):
            try:
                # Use CRR method with conservative steps
                binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", steps)
                option.setPricingEngine(binomial_engine)
                price = option.NPV()
                
                # Check for NaN or infinite values
                if not (price == price):  # NaN check
                    raise ValueError("NaN price calculated")
                if abs(price) > 1e10:  # Unreasonably large price
                    raise ValueError("Price too large")
                if price < 0:  # Negative price check
                    raise ValueError("Negative price calculated")
                    
                return price
            except Exception as e:
                error_msg = str(e).lower()
                if "negative probability" in error_msg or "probability" in error_msg:
                    print(f"DEBUG: Negative probability error with steps={steps}")
                    print(f"DEBUG: Error details: {str(e)}")
                    # Try with fewer steps as fallback
                    if steps > 5:
                        try:
                            binomial_engine = ql.BinomialVanillaEngine(bsm_process, "crr", 5)
                            option.setPricingEngine(binomial_engine)
                            price = option.NPV()
                            if price >= 0:
                                return price
                        except:
                            pass
                    raise ValueError("negative probability")
                else:
                    print(f"DEBUG: Other error: {str(e)}")
                    raise e

        # 7. Generate convergence data
        max_steps = data['max_steps']
        steps = range(2, max_steps)
        
        try:
            european_prices = []
            american_prices = []
            
            for step in steps:
                try:
                    # Calculate European option price
                    european_price = binomial_price(european_option, bsm_process, step)
                    european_prices.append(european_price)
                    
                    # Calculate American option price
                    american_price = binomial_price(american_option, bsm_process, step)
                    american_prices.append(american_price)
                    
                except ValueError as e:
                    if "negative probability" in str(e):
                        print(f"DEBUG: Negative probability at step {step}, stopping calculation")
                        break
                    else:
                        raise e
                        
        except Exception as e:
            if "negative probability" in str(e).lower():
                return {'error': 'negative probability - try adjusting volatility or time to maturity'}
            else:
                raise e

        # Ensure steps and prices arrays have the same length
        actual_steps = list(steps)[:len(european_prices)]
        
        return {
            'bs_price': bs_price,
            'european_convergence': {
                'steps': actual_steps,
                'prices': european_prices
            },
            'american_convergence': {
                'steps': actual_steps,
                'prices': american_prices
            }
        }

    except Exception as e:
        return {'error': str(e)}