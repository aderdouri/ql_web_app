# chapter3_numerical_greeks/services.py

import QuantLib as ql
from datetime import datetime
import json

def quantlib_date_from_python_date(python_date):
    """Convert Python date to QuantLib Date"""
    return ql.Date(python_date.day, python_date.month, python_date.year)

def create_barrier_option_exact(barrier_type, option_type, strike_price, barrier_level, rebate, 
                               evaluation_date, maturity_date, underlying_price, risk_free_rate, volatility):
    """Create a barrier option using QuantLib - exact match to book code"""
    
    # Set evaluation date
    ql.Settings.instance().evaluationDate = quantlib_date_from_python_date(evaluation_date)
    
    # Create dates
    maturity = quantlib_date_from_python_date(maturity_date)
    
    # Create payoff
    if option_type == 'call':
        payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike_price)
    else:
        payoff = ql.PlainVanillaPayoff(ql.Option.Put, strike_price)
    
    # Create exercise
    exercise = ql.EuropeanExercise(maturity)
    
    # Create barrier option
    if barrier_type == 'up_and_in':
        barrier_type_ql = ql.Barrier.UpIn
    elif barrier_type == 'up_and_out':
        barrier_type_ql = ql.Barrier.UpOut
    elif barrier_type == 'down_and_in':
        barrier_type_ql = ql.Barrier.DownIn
    else:  # down_and_out
        barrier_type_ql = ql.Barrier.DownOut
    
    barrier_option = ql.BarrierOption(barrier_type_ql, barrier_level, rebate, payoff, exercise)
    
    # Create market data using SimpleQuote for dynamic changes (exact match to book)
    u = ql.SimpleQuote(underlying_price)
    r = ql.SimpleQuote(risk_free_rate)
    sigma = ql.SimpleQuote(volatility)
    
    # Create term structures (exact match to book)
    riskFreeCurve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r), ql.Actual360())
    volatility_curve = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360())
    
    # Create process
    process = ql.BlackScholesProcess(ql.QuoteHandle(u), 
                                   ql.YieldTermStructureHandle(riskFreeCurve),
                                   ql.BlackVolTermStructureHandle(volatility_curve))
    
    # Create engine
    engine = ql.AnalyticBarrierEngine(process)
    barrier_option.setPricingEngine(engine)
    
    return barrier_option, u, r, sigma

def calculate_numerical_greeks(form_data):
    """Calculate option price and numerical Greeks - exact match to book formulas"""
    
    try:
        # Extract form data
        barrier_type = form_data['barrier_type']
        option_type = form_data['option_type']
        strike_price = float(form_data['strike_price'])
        barrier_level = float(form_data['barrier_level'])
        rebate = float(form_data['rebate'])
        evaluation_date = datetime.strptime(form_data['evaluation_date'], '%Y-%m-%d').date()
        maturity_date = datetime.strptime(form_data['maturity_date'], '%Y-%m-%d').date()
        underlying_price = float(form_data['underlying_price'])
        risk_free_rate = float(form_data['risk_free_rate'])
        volatility = float(form_data['volatility'])
        underlying_perturbation = float(form_data['underlying_perturbation'])
        rate_perturbation = float(form_data['rate_perturbation'])
        volatility_perturbation = float(form_data['volatility_perturbation'])
        
        # Create base option with quotes for dynamic changes
        base_option, u, r, sigma = create_barrier_option_exact(
            barrier_type, option_type, strike_price, barrier_level, rebate,
            evaluation_date, maturity_date, underlying_price, risk_free_rate, volatility
        )
        
        # Calculate base NPV
        P0 = base_option.NPV()
        
        # Calculate Delta using two-sided formula (exact match to book)
        u0 = u.value()
        h_u = underlying_perturbation
        
        # Save current value and perturb
        u.setValue(u0 + h_u)
        P_plus = base_option.NPV()
        
        u.setValue(u0 - h_u)
        P_minus = base_option.NPV()
        
        # Reset to original value
        u.setValue(u0)
        
        # Calculate Delta and Gamma (exact formulas from book)
        Delta = (P_plus - P_minus) / (2 * h_u)
        Gamma = (P_plus - 2 * P0 + P_minus) / (h_u * h_u)
        
        # Calculate Rho using one-sided formula (exact match to book)
        r0 = r.value()
        h_r = rate_perturbation
        
        r.setValue(r0 + h_r)
        P_plus_rho = base_option.NPV()
        r.setValue(r0)  # Reset
        
        Rho = (P_plus_rho - P0) / h_r
        
        # Calculate Vega using one-sided formula (exact match to book)
        sigma0 = sigma.value()
        h_sigma = volatility_perturbation
        
        sigma.setValue(sigma0 + h_sigma)
        P_plus_vega = base_option.NPV()
        sigma.setValue(sigma0)  # Reset
        
        Vega = (P_plus_vega - P0) / h_sigma
        
        return {
            'success': True,
            'npv': P0,
            'delta': Delta,
            'gamma': Gamma,
            'rho': Rho,
            'vega': Vega
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def calculate_price_series(form_data, price_range=(90, 110), num_points=21):
    """Calculate option prices and Greeks for a range of underlying prices"""
    
    try:
        # Extract form data
        barrier_type = form_data['barrier_type']
        option_type = form_data['option_type']
        strike_price = float(form_data['strike_price'])
        barrier_level = float(form_data['barrier_level'])
        rebate = float(form_data['rebate'])
        evaluation_date = datetime.strptime(form_data['evaluation_date'], '%Y-%m-%d').date()
        maturity_date = datetime.strptime(form_data['maturity_date'], '%Y-%m-%d').date()
        risk_free_rate = float(form_data['risk_free_rate'])
        volatility = float(form_data['volatility'])
        underlying_perturbation = float(form_data['underlying_perturbation'])
        rate_perturbation = float(form_data['rate_perturbation'])
        volatility_perturbation = float(form_data['volatility_perturbation'])
        
        # Generate price range
        min_price, max_price = price_range
        price_step = (max_price - min_price) / (num_points - 1)
        prices = [min_price + i * price_step for i in range(num_points)]
        
        # Calculate values for each price
        npv_values = []
        delta_values = []
        gamma_values = []
        rho_values = []
        vega_values = []
        
        for price in prices:
            # Create option for this price with quotes for dynamic changes
            option, u, r, sigma = create_barrier_option_exact(
                barrier_type, option_type, strike_price, barrier_level, rebate,
                evaluation_date, maturity_date, price, risk_free_rate, volatility
            )
            
            # Calculate NPV
            P0 = option.NPV()
            npv_values.append(P0)
            
            # Calculate Greeks using finite differences (exact formulas from book)
            u0 = u.value()
            h_u = underlying_perturbation
            
            # Delta and Gamma
            u.setValue(u0 + h_u)
            P_plus = option.NPV()
            
            u.setValue(u0 - h_u)
            P_minus = option.NPV()
            
            u.setValue(u0)  # Reset
            
            Delta = (P_plus - P_minus) / (2 * h_u)
            Gamma = (P_plus - 2 * P0 + P_minus) / (h_u * h_u)
            
            delta_values.append(Delta)
            gamma_values.append(Gamma)
            
            # Rho
            r0 = r.value()
            h_r = rate_perturbation
            
            r.setValue(r0 + h_r)
            P_plus_rho = option.NPV()
            r.setValue(r0)  # Reset
            
            Rho = (P_plus_rho - P0) / h_r
            rho_values.append(Rho)
            
            # Vega
            sigma0 = sigma.value()
            h_sigma = volatility_perturbation
            
            sigma.setValue(sigma0 + h_sigma)
            P_plus_vega = option.NPV()
            sigma.setValue(sigma0)  # Reset
            
            Vega = (P_plus_vega - P0) / h_sigma
            vega_values.append(Vega)
        
        return {
            'success': True,
            'prices': prices,
            'npv': npv_values,
            'delta': delta_values,
            'gamma': gamma_values,
            'rho': rho_values,
            'vega': vega_values
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }