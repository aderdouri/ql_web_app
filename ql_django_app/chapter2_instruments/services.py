# chapter2_instruments/services.py

import QuantLib as ql
import time
from datetime import datetime, date
from typing import Dict, Any, Tuple

def quantlib_date_from_python_date(python_date):
    """Convert Python date to QuantLib Date"""
    if isinstance(python_date, str):
        python_date = datetime.strptime(python_date, '%Y-%m-%d').date()
    return ql.Date(python_date.day, python_date.month, python_date.year)

def create_black_scholes_engine(underlying_price, risk_free_rate, volatility, evaluation_date):
    """Create Black-Scholes pricing engine"""
    # Set evaluation date
    ql.Settings.instance().evaluationDate = evaluation_date
    
    # Create market data exactly like the reference code
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(underlying_price))
    rate_handle = ql.YieldTermStructureHandle(
        ql.FlatForward(0, ql.TARGET(), risk_free_rate, ql.Actual360())
    )
    vol_handle = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(0, ql.TARGET(), volatility, ql.Actual360())
    )
    
    # Create process exactly like the reference code
    process = ql.BlackScholesProcess(spot_handle, rate_handle, vol_handle)
    
    # Create engine
    engine = ql.AnalyticEuropeanEngine(process)
    
    return engine, process

def create_heston_engine(underlying_price, risk_free_rate, volatility, evaluation_date, 
                        v0, kappa, theta, sigma, rho):
    """Create Heston pricing engine"""
    # Set evaluation date
    ql.Settings.instance().evaluationDate = evaluation_date
    
    # Create market data exactly like the reference code
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(underlying_price))
    rate_handle = ql.YieldTermStructureHandle(
        ql.FlatForward(0, ql.TARGET(), risk_free_rate, ql.Actual360())
    )
    
    # Create Heston process exactly like the reference code
    process = ql.HestonProcess(
        rate_handle,
        ql.YieldTermStructureHandle(ql.FlatForward(0, ql.TARGET(), 0.0, ql.Actual360())),
        spot_handle,
        v0, kappa, theta, sigma, rho
    )
    
    # Create engine
    engine = ql.AnalyticHestonEngine(ql.HestonModel(process))
    
    return engine, process

def create_monte_carlo_engine(underlying_price, risk_free_rate, volatility, evaluation_date,
                             time_steps=20, required_samples=100000):
    """Create Monte Carlo pricing engine"""
    # Set evaluation date
    ql.Settings.instance().evaluationDate = evaluation_date
    
    # Create market data exactly like the reference code
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(underlying_price))
    rate_handle = ql.YieldTermStructureHandle(
        ql.FlatForward(0, ql.TARGET(), risk_free_rate, ql.Actual360())
    )
    vol_handle = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(0, ql.TARGET(), volatility, ql.Actual360())
    )
    
    # Create process exactly like the reference code
    process = ql.BlackScholesProcess(spot_handle, rate_handle, vol_handle)
    
    # Create Monte Carlo engine
    engine = ql.MCEuropeanEngine(process, "PseudoRandom", timeSteps=time_steps, 
                                requiredSamples=required_samples)
    
    return engine, process

def calculate_option_price(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate option price using the specified engine"""
    try:
        # Extract parameters
        underlying_price = float(form_data['underlying_price'])
        strike_price = float(form_data['strike_price'])
        risk_free_rate = float(form_data['risk_free_rate'])
        volatility = float(form_data['volatility'])
        evaluation_date = quantlib_date_from_python_date(form_data['evaluation_date'])
        maturity_date = quantlib_date_from_python_date(form_data['maturity_date'])
        option_type = ql.Option.Call if form_data['option_type'] == 'call' else ql.Option.Put
        pricing_engine = form_data['pricing_engine']
        
        # Special case: evaluation date equals maturity date
        if evaluation_date == maturity_date:
            return {
                'success': True,
                'npv': 0.0,
                'greeks': {
                    'delta': 0.0,
                    'gamma': 0.0,
                    'vega': 0.0
                },
                'calculation_time': 0.0,
                'engine_used': 'analytic_european',
                'parameters': {
                    'underlying_price': underlying_price,
                    'strike_price': strike_price,
                    'risk_free_rate': risk_free_rate,
                    'volatility': volatility,
                    'evaluation_date': evaluation_date.to_date(),
                    'maturity_date': maturity_date.to_date(),
                    'option_type': form_data['option_type']
                }
            }
        
        # Create option exactly like the reference code
        option = ql.EuropeanOption(ql.PlainVanillaPayoff(option_type, strike_price),
                                   ql.EuropeanExercise(maturity_date))
        
        # Create appropriate engine
        start_time = time.time()
        
        if pricing_engine == 'black_scholes':
            engine, process = create_black_scholes_engine(
                underlying_price, risk_free_rate, volatility, evaluation_date
            )
        elif pricing_engine == 'heston':
            v0 = float(form_data.get('v0', 0.04))
            kappa = float(form_data.get('kappa', 0.1))
            theta = float(form_data.get('theta', 0.01))
            sigma = float(form_data.get('sigma', 0.05))
            rho = float(form_data.get('rho', -0.75))
            engine, process = create_heston_engine(
                underlying_price, risk_free_rate, volatility, evaluation_date,
                v0, kappa, theta, sigma, rho
            )
        elif pricing_engine == 'monte_carlo':
            time_steps = int(form_data.get('time_steps', 20))
            required_samples = int(form_data.get('required_samples', 100000))
            engine, process = create_monte_carlo_engine(
                underlying_price, risk_free_rate, volatility, evaluation_date,
                time_steps, required_samples
            )
        else:
            raise ValueError(f"Unknown pricing engine: {pricing_engine}")
        
        # Set engine and calculate price
        option.setPricingEngine(engine)
        npv = option.NPV()
        
        calculation_time = time.time() - start_time
        
        # Calculate Greeks (only for Black-Scholes) - Chapter 2: Delta, Gamma, Vega only
        greeks = {}
        if pricing_engine == 'black_scholes':
            try:
                greeks = {
                    'delta': option.delta(),
                    'gamma': option.gamma(),
                    'vega': option.vega()
                }
            except:
                greeks = {}
        
        return {
            'success': True,
            'npv': npv,
            'greeks': greeks,
            'calculation_time': calculation_time,
            'engine_used': pricing_engine,
            'parameters': {
                'underlying_price': underlying_price,
                'strike_price': strike_price,
                'risk_free_rate': risk_free_rate,
                'volatility': volatility,
                'evaluation_date': evaluation_date.to_date(),
                'maturity_date': maturity_date.to_date(),
                'option_type': form_data['option_type']
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'npv': None,
            'greeks': {},
            'calculation_time': 0
        }

def calculate_price_series(underlying_prices, form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate option prices for a range of underlying prices"""
    results = []
    
    for price in underlying_prices:
        # Create modified form data with new underlying price
        modified_data = form_data.copy()
        modified_data['underlying_price'] = price
        
        result = calculate_option_price(modified_data)
        if result['success']:
            results.append({
                'underlying_price': price,
                'npv': result['npv']
            })
    
    return {
        'success': True,
        'series': results
    }

def calculate_volatility_series(volatilities, form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate option prices for a range of volatilities"""
    results = []
    
    for vol in volatilities:
        # Create modified form data with new volatility
        modified_data = form_data.copy()
        modified_data['volatility'] = vol
        
        result = calculate_option_price(modified_data)
        if result['success']:
            results.append({
                'volatility': vol,
                'npv': result['npv']
            })
    
    return {
        'success': True,
        'series': results
    }

def calculate_time_decay_series(evaluation_dates, form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate option prices for different evaluation dates"""
    results = []
    
    for eval_date in evaluation_dates:
        # Create modified form data with new evaluation date
        modified_data = form_data.copy()
        modified_data['evaluation_date'] = eval_date
        
        result = calculate_option_price(modified_data)
        if result['success']:
            results.append({
                'evaluation_date': eval_date,
                'npv': result['npv']
            })
    
    return {
        'success': True,
        'series': results
    }

def compare_engines(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compare results from different pricing engines"""
    engines = ['black_scholes', 'heston', 'monte_carlo']
    results = {}
    
    for engine in engines:
        modified_data = form_data.copy()
        modified_data['pricing_engine'] = engine
        
        result = calculate_option_price(modified_data)
        if result['success']:
            results[engine] = {
                'npv': result['npv'],
                'calculation_time': result['calculation_time'],
                'engine_name': engine.replace('_', ' ').title()
            }
    
    return {
        'success': True,
        'comparison': results
    }