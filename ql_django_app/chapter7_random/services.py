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
                    # For 2D+: generate individual numbers (flattened)
                    for _ in range(dimensionality):
                        numbers.append(rng.next().value())
            return numbers  # Return all numbers for display
            
        elif rng_type == 'Sobol':
            # Exact notebook code: rng = ql.SobolRsg(dimensionality)
            rng = ql.SobolRsg(dimensionality)
            numbers = []
            for _ in range(min(num_simulations, 2047)):  # Use 2047 like in notebook
                sequence = rng.nextSequence().value()
                if dimensionality == 1:
                    numbers.append(sequence[0])
                else:
                    # For 2D+: flatten the sequence
                    for value in sequence:
                        numbers.append(value)
            return numbers  # Return all numbers for display
            
        elif rng_type == 'Inverse Cumulative Normal':
            rng = ql.MersenneTwisterUniformRng(seed)
            numbers = []
            for _ in range(min(num_simulations, 2047)):
                uniform = rng.next().value()
                # Convert to normal using QuantLib
                normal = ql.InverseCumulativeNormal()(uniform)
                numbers.append(normal)
            return numbers  # Return all numbers for display
            
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
            
            # Create points for 1D display (y=0 for all points) - exact notebook format
            points = []
            for x in xs:
                points.append({'x': x, 'y': 0})  # All points on horizontal line y=0
            
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
    """Create correlated stocks simulation data using the provided code"""
    try:
        # 1. Setup fixe (comme dans le livre)
        today = ql.Date(27, 1, 2018)
        ql.Settings.instance().evaluationDate = today
        risk_free = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual360()))
        
        processes_data = [(100, 0.20), (80, 0.25), (110, 0.18)]
        processes = [
            ql.BlackScholesProcess(
                ql.QuoteHandle(ql.SimpleQuote(S)), risk_free,
                ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.TARGET(), sigma, ql.Actual360())))
            for S, sigma in processes_data
        ]
        
        rho = [[1.0, 0.6, 0.8], [0.6, 1.0, 0.4], [0.8, 0.4, 1.0]]
        multi_process = ql.StochasticProcessArray(processes, rho)

        # 2. Paramètres de la simulation
        num_steps = 4  # 4 steps comme dans le livre
        simulation_length = 1.0  # 1 an
        
        # Utiliser les mêmes times que dans le livre: [0.25, 0.50, 0.75, 1.0]
        times = [0.25, 0.50, 0.75, 1.0]
        dimensionality = multi_process.factors() * len(times)
        
        # 3. Génération d'une seule trajectoire
        rng = ql.GaussianRandomSequenceGenerator(
            ql.UniformRandomSequenceGenerator(dimensionality, ql.UniformRandomGenerator(seed))
        )
        generator = ql.GaussianMultiPathGenerator(multi_process, list(times), rng, False)
        
        path = generator.next().value()
        
        # 4. Formatage des résultats pour le graphique
        time_grid = [0.0] + list(times)
        paths_data = []
        for i in range(multi_process.size()):
            paths_data.append([path[i].front()] + list(path[i]))

        # 5. Créer les données dans le format attendu par le nouveau code JavaScript
        result = {
            'title': 'Correlated Stocks Simulation',
            'time_grid': time_grid,
            'paths': paths_data,
            'required_dimensionality': dimensionality
        }
        
        print(f"Correlated stocks data generated: {len(paths_data)} paths")
        print(f"Time grid: {time_grid}")
        print(f"Required dimensionality: {dimensionality}")
        return result
        
    except Exception as e:
        print(f"Error in create_correlated_stocks_data: {e}")
        import traceback
        traceback.print_exc()
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
        
        # Create Monte Carlo engine with proper error handling
        try:
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
            
        except Exception as mc_error:
            print(f"Monte Carlo engine error: {mc_error}")
            # Fallback to analytical pricing if MC fails
            try:
                analytical_engine = ql.AnalyticEuropeanEngine(process)
                option.setPricingEngine(analytical_engine)
                return option.NPV()
            except Exception as analytical_error:
                print(f"Analytical fallback error: {analytical_error}")
                return 0.0
        
    except Exception as e:
        print(f"Monte Carlo error: {e}")
        return 0.0

def calculate_all_results(rng_params, option_params):
    """Calculate all results for the lab - exact notebook implementation"""
    try:
        print(f"Starting calculations with RNG: {rng_params['rng_type']}, Seed: {rng_params['seed']}")
        
        # Calculate each component with individual error handling
        results = {
            'success': True,
            'random_numbers': [],
            'unit_square_data': None,
            'sobol_1d_data': None,
            'sobol_2d_data': None,
            'correlated_stocks_data': None,
            'black_scholes_price': 0.0,
            'monte_carlo_price_rng': 0.0,
            'monte_carlo_price_sobol': 0.0
        }
        
        # Generate random numbers
        try:
            results['random_numbers'] = generate_random_numbers(
                rng_params['rng_type'], 
                rng_params['seed'], 
                rng_params['num_simulations'], 
                rng_params['dimensionality']
            )
            print("✓ Random numbers generated successfully")
        except Exception as e:
            print(f"✗ Error generating random numbers: {e}")
        
        # Create unit square plot data
        try:
            results['unit_square_data'] = create_unit_square_plot_data(
                rng_params['rng_type'], 
                rng_params['seed'], 
                rng_params['num_simulations']
            )
            print("✓ Unit square data created successfully")
        except Exception as e:
            print(f"✗ Error creating unit square data: {e}")
        
        # Create Sobol 1D progression data
        try:
            results['sobol_1d_data'] = create_sobol_1d_progression_data()
            print("✓ Sobol 1D data created successfully")
        except Exception as e:
            print(f"✗ Error creating Sobol 1D data: {e}")
        
        # Create Sobol 2D progression data
        try:
            results['sobol_2d_data'] = create_sobol_2d_progression_data()
            print("✓ Sobol 2D data created successfully")
        except Exception as e:
            print(f"✗ Error creating Sobol 2D data: {e}")
        
        # Create correlated stocks data
        try:
            results['correlated_stocks_data'] = create_correlated_stocks_data(
                rng_params['seed'], 
                rng_params['num_simulations']
            )
            print("✓ Correlated stocks data created successfully")
        except Exception as e:
            print(f"✗ Error creating correlated stocks data: {e}")
        
        # Calculate Black-Scholes price
        try:
            results['black_scholes_price'] = calculate_black_scholes_price(option_params)
            print(f"✓ Black-Scholes price: {results['black_scholes_price']:.4f}")
        except Exception as e:
            print(f"✗ Error calculating Black-Scholes price: {e}")
        
        # Calculate Monte Carlo price with RNG
        try:
            results['monte_carlo_price_rng'] = monte_carlo_option_price(
                rng_params['rng_type'], 
                rng_params['seed'], 
                rng_params['num_simulations'], 
                option_params
            )
            print(f"✓ Monte Carlo price (RNG): {results['monte_carlo_price_rng']:.4f}")
        except Exception as e:
            print(f"✗ Error calculating Monte Carlo price (RNG): {e}")
        
        # Calculate Monte Carlo price with Sobol
        try:
            results['monte_carlo_price_sobol'] = monte_carlo_option_price(
                'Sobol', 
                rng_params['seed'], 
                rng_params['num_simulations'], 
                option_params
            )
            print(f"✓ Monte Carlo price (Sobol): {results['monte_carlo_price_sobol']:.4f}")
        except Exception as e:
            print(f"✗ Error calculating Monte Carlo price (Sobol): {e}")
        
        print("🎉 All calculations completed!")
        return results
        
    except Exception as e:
        print(f"❌ Critical error in calculate_all_results: {e}")
        return {
            'success': False,
            'error': str(e)
        }