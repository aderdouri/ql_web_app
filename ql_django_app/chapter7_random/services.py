import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from datetime import date

def set_unit_square(ax):
    """Helper function to set up unit square plot - exact from notebook"""
    ax.axis('scaled')
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])

def generate_random_numbers(rng_type, seed, num_simulations, dimensionality):
    """Generate random numbers using specified RNG type - exact notebook implementation"""
    try:
        if rng_type == 'Mersenne Twister':
            # Exact notebook code: rng = ql.MersenneTwisterUniformRng(42)
            rng = ql.MersenneTwisterUniformRng(seed)
            numbers = []
            for _ in range(min(num_simulations, 2047)):  # Use 2047 like in notebook
                if dimensionality == 1:
                    numbers.append(rng.next().value())
                else:
                    # For 2D: generate pairs like in notebook
                    sample = []
                    for _ in range(dimensionality):
                        sample.append(rng.next().value())
                    numbers.append(sample)
            return numbers[:10]  # Return first 10 for display
            
        elif rng_type == 'Sobol':
            # Exact notebook code: rng = ql.SobolRsg(dimensionality)
            rng = ql.SobolRsg(dimensionality)
            numbers = []
            for _ in range(min(num_simulations, 2047)):  # Use 2047 like in notebook
                sequence = rng.nextSequence().value()
                if dimensionality == 1:
                    numbers.append(sequence[0])
                else:
                    numbers.append(list(sequence))
            return numbers[:10]  # Return first 10 for display
            
        elif rng_type == 'Inverse Cumulative Normal':
            rng = ql.MersenneTwisterUniformRng(seed)
            numbers = []
            for _ in range(min(num_simulations, 2047)):
                uniform = rng.next().value()
                # Convert to normal using QuantLib
                normal = ql.InverseCumulativeNormal()(uniform)
                numbers.append(normal)
            return numbers[:10]  # Return first 10 for display
            
        return []
        
    except Exception as e:
        print(f"Error generating random numbers: {e}")
        return []

def create_unit_square_plot_data(rng_type, seed, num_simulations):
    """Create unit square plot data matching the notebook exactly"""
    try:
        if rng_type == 'Sobol':
            # Use Sobol for 2D (correct dimensionality) - exact notebook code
            rng = ql.SobolRsg(2)
            xs = []
            ys = []
            for i in range(min(2047, num_simulations)):
                x, y = rng.nextSequence().value()
                xs.append(x)
                ys.append(y)
        else:
            # Mersenne Twister (pseudo-random) - exact notebook code
            rng = ql.MersenneTwisterUniformRng(seed)
            xs = []
            ys = []
            for i in range(min(2047, num_simulations)):
                xs.append(rng.next().value())
                ys.append(rng.next().value())
        
        # Create Chart.js compatible data
        data_points = []
        for i in range(len(xs)):
            data_points.append({
                'x': xs[i],
                'y': ys[i]
            })
        
        return {
            'title': f'Unit Square Coverage - {rng_type}',
            'x_label': 'X',
            'y_label': 'Y',
            'data': data_points,
            'x_min': 0,
            'x_max': 1,
            'y_min': 0,
            'y_max': 1
        }
        
    except Exception as e:
        print(f"Error in create_unit_square_plot_data: {e}")
        return None

def create_sobol_1d_progression_data():
    """Create 1D Sobol progression data (16 mini-plots) - exact notebook implementation"""
    try:
        progression_data = []
        n_values = [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 15, 19, 23, 27, 31]  # Exact from notebook
        
        for n in n_values:
            rng = ql.SobolRsg(1)  # 1D Sobol
            xs = []
            for j in range(n):
                xs.append(rng.nextSequence().value()[0])
            
            # Create points for 1D display (y=0 for all points)
            points = []
            for x in xs:
                points.append({'x': x, 'y': 0})
            
            progression_data.append({
                'n': n,
                'points': points
            })
        
        return {
            'title': 'Sobol 1D Sequence Progression',
            'progression': progression_data
        }
        
    except Exception as e:
        print(f"Error in create_sobol_1d_progression_data: {e}")
        return None

def create_sobol_2d_progression_data():
    """Create 2D Sobol progression data (12 mini-plots) - exact notebook implementation"""
    try:
        progression_data = []
        n_values = [0, 1, 2, 3, 4, 5, 6, 7, 15, 31, 63, 127]  # Exact from notebook
        
        for n in n_values:
            rng = ql.SobolRsg(2)  # 2D Sobol
            points = []
            for j in range(n):
                x, y = rng.nextSequence().value()
                points.append({'x': x, 'y': y})
            
            progression_data.append({
                'n': n,
                'points': points
            })
        
        return {
            'title': 'Sobol 2D Sequence Progression',
            'progression': progression_data
        }
        
    except Exception as e:
        print(f"Error in create_sobol_2d_progression_data: {e}")
        return None

def create_correlated_stocks_data(seed, num_simulations):
    """Create correlated stocks simulation data - exact notebook implementation"""
    try:
        # Exact notebook setup
        today = ql.Date(27, ql.January, 2018)
        ql.Settings.instance().evaluationDate = today
        risk_free = ql.YieldTermStructureHandle(
            ql.FlatForward(today, 0.01, ql.Actual360()))
        
        # Exact notebook processes
        processes = [
            ql.BlackScholesProcess(
                ql.QuoteHandle(ql.SimpleQuote(S)),
                risk_free,
                ql.BlackVolTermStructureHandle(
                    ql.BlackConstantVol(today, ql.TARGET(), sigma, ql.Actual360())))
            for S, sigma in [(100, 0.20), (80, 0.25), (110, 0.18)]
        ]
        
        # Exact notebook correlation matrix
        rho = [[1.0, 0.6, 0.8],
               [0.6, 1.0, 0.4],
               [0.8, 0.4, 1.0]]
        process = ql.StochasticProcessArray(processes, rho)
        
        # Exact notebook helper function
        def rng(dimensionality):
            return ql.GaussianRandomSequenceGenerator(
                ql.UniformRandomSequenceGenerator(
                    dimensionality,
                    ql.UniformRandomGenerator(seed)))
        
        # Exact notebook times
        times = [0.25, 0.50, 0.75, 1.0]
        
        # Use correct dimensionality (3 factors * 4 time steps = 12)
        generator = ql.GaussianMultiPathGenerator(process, times, rng(12))
        sample = generator.next().value()
        
        # Create Chart.js compatible data - exact values from book
        datasets = []
        ts = [0.0] + times  # Add initial time
        
        colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)']  # Blue, Orange, Green
        
        for i in range(3):
            stock_data = []
            for j in range(len(ts)):
                stock_data.append({
                    'x': ts[j],
                    'y': sample[i][j]
                })
            
            datasets.append({
                'label': f'Stock {i+1}',
                'data': stock_data,
                'borderColor': colors[i],
                'backgroundColor': colors[i],
                'fill': False,
                'tension': 0.1,
                'pointRadius': 4,
                'pointHoverRadius': 6
            })
        
        result = {
            'title': 'Correlated Stocks Simulation',
            'x_label': 'Time',
            'y_label': 'Stock Price',
            'datasets': datasets,
            'x_min': 0.0,
            'x_max': 1.0
        }
        print(f"Correlated stocks data generated: {len(datasets)} datasets")
        return result
        
    except Exception as e:
        print(f"Error in create_correlated_stocks_data: {e}")
        return None

def calculate_black_scholes_price(option_params):
    """Calculate Black-Scholes option price"""
    try:
        # Set up QuantLib
        today = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = today
        
        # Option parameters
        spot = option_params['spot']
        strike = option_params['strike']
        risk_free_rate = option_params['risk_free_rate']
        volatility = option_params['volatility']
        maturity = option_params['maturity']
        
        # Create option
        option_type = ql.Option.Call
        payoff = ql.PlainVanillaPayoff(option_type, strike)
        exercise = ql.EuropeanExercise(today + int(maturity * 365))
        option = ql.VanillaOption(payoff, exercise)
        
        # Create market data
        risk_free_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, ql.Actual360()))
        volatility_curve = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), volatility, ql.Actual360()))
        
        # Create process
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
        process = ql.BlackScholesProcess(spot_handle, risk_free_curve, volatility_curve)
        
        # Create engine
        engine = ql.AnalyticEuropeanEngine(process)
        option.setPricingEngine(engine)
        
        price = option.NPV()
        return price
        
    except Exception as e:
        print(f"Black-Scholes error: {e}")
        return 0.0

def monte_carlo_option_price(rng_type, seed, num_simulations, option_params):
    """Calculate Monte Carlo option price - exact notebook implementation"""
    try:
        # Set up QuantLib
        today = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = today
        
        # Option parameters
        spot = option_params['spot']
        strike = option_params['strike']
        risk_free_rate = option_params['risk_free_rate']
        volatility = option_params['volatility']
        maturity = option_params['maturity']
        
        # Create option
        option_type = ql.Option.Call
        payoff = ql.PlainVanillaPayoff(option_type, strike)
        exercise = ql.EuropeanExercise(today + int(maturity * 365))
        option = ql.VanillaOption(payoff, exercise)
        
        # Create market data
        risk_free_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, risk_free_rate, ql.Actual360()))
        volatility_curve = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), volatility, ql.Actual360()))
        
        # Create process
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
        process = ql.BlackScholesProcess(spot_handle, risk_free_curve, volatility_curve)
        
        # Create Monte Carlo engine - DEFINITIVE SOLUTION using string-based RNG type
        # Use string-based approach: "pseudorandom" or "lowdiscrepancy"
        if rng_type == 'Sobol':
            # For Sobol, use lowdiscrepancy sequence
            mc_engine = ql.MCEuropeanEngine(
                process,
                "lowdiscrepancy",  # Sobol sequence
                timeSteps=1,
                requiredSamples=num_simulations
            )
        else:
            # For Mersenne Twister and others, use pseudorandom
            mc_engine = ql.MCEuropeanEngine(
                process,
                "pseudorandom",  # Mersenne Twister
                timeSteps=1,
                requiredSamples=num_simulations
            )
        
        option.setPricingEngine(mc_engine)
        
        price = option.NPV()
        return price
        
    except Exception as e:
        print(f"Monte Carlo error: {e}")
        return 0.0

def calculate_all_results(rng_params, option_params):
    """Calculate all results for the lab - exact notebook implementation"""
    try:
        results = {
            'success': True,
            'random_numbers': generate_random_numbers(
                rng_params['rng_type'], 
                rng_params['seed'], 
                rng_params['num_simulations'], 
                rng_params['dimensionality']
            ),
            'unit_square_data': create_unit_square_plot_data(
                rng_params['rng_type'], 
                rng_params['seed'], 
                rng_params['num_simulations']
            ),
            'sobol_1d_data': create_sobol_1d_progression_data(),
            'sobol_2d_data': create_sobol_2d_progression_data(),
            'correlated_stocks_data': create_correlated_stocks_data(
                rng_params['seed'], 
                rng_params['num_simulations']
            ),
            'black_scholes_price': calculate_black_scholes_price(option_params),
            'monte_carlo_price_rng': monte_carlo_option_price(
                rng_params['rng_type'], 
                rng_params['seed'], 
                rng_params['num_simulations'], 
                option_params
            ),
            'monte_carlo_price_sobol': monte_carlo_option_price(
                'Sobol', 
                rng_params['seed'], 
                rng_params['num_simulations'], 
                option_params
            )
        }
        
        return results
        
    except Exception as e:
        print(f"Error in calculate_all_results: {e}")
        return {
            'success': False,
            'error': str(e)
        }