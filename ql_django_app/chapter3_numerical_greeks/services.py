"""
Chapter 3 - Numerical Greeks calculation services
Exact implementation from QuantLib Python Cookbook
"""
import QuantLib as ql
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, date


def quantlib_date_from_python_date(python_date):
    """Convert Python date to QuantLib Date"""
    if isinstance(python_date, str):
        python_date = datetime.strptime(python_date, '%Y-%m-%d').date()
    return ql.Date(python_date.day, python_date.month, python_date.year)


def build_option(params):
    """
    Build the barrier option exactly as in the notebook
    Reproduces In[3] to In[7] from the book
    """
    # Extract parameters with proper defaults
    barrier_type = params.get('barrier_type', 'UpIn')
    barrier_level = float(params.get('barrier_level', 120.0))
    rebate = float(params.get('rebate', 0.0))
    option_type = params.get('option_type', 'Call')
    strike = float(params.get('strike_price', params.get('strike', 100.0)))
    exercise_date = params.get('maturity_date', params.get('exercise_date', '2015-01-08'))
    evaluation_date = params.get('evaluation_date', '2014-10-08')
    underlying = float(params.get('underlying_price', params.get('underlying', 100.0)))
    risk_free_rate = float(params.get('risk_free_rate', 0.01))
    volatility = float(params.get('volatility', 0.20))
    
    # Debug: Print all parameters
    print(f"DEBUG build_option: barrier_type={barrier_type}, barrier_level={barrier_level}")
    print(f"DEBUG build_option: option_type={option_type}, strike={strike}")
    print(f"DEBUG build_option: underlying={underlying}, risk_free_rate={risk_free_rate}, volatility={volatility}")
    
    # Set evaluation date (In[2])
    today = quantlib_date_from_python_date(evaluation_date)
    ql.Settings.instance().evaluationDate = today
    print(f"DEBUG build_option: evaluation_date set to {today}")
    
    # Create barrier option (In[3])
    barrier_map = {
        'UpIn': ql.Barrier.UpIn,
        'UpOut': ql.Barrier.UpOut,
        'DownIn': ql.Barrier.DownIn,
        'DownOut': ql.Barrier.DownOut
    }
    
    option_type_map = {
        'Call': ql.Option.Call,
        'Put': ql.Option.Put
    }
    
    option = ql.BarrierOption(
        barrier_map[barrier_type],
        barrier_level,
        rebate,
        ql.PlainVanillaPayoff(option_type_map[option_type], strike),
        ql.EuropeanExercise(quantlib_date_from_python_date(exercise_date))
    )
    
    # Create quotes (In[4])
    u = ql.SimpleQuote(underlying)
    r = ql.SimpleQuote(risk_free_rate)
    sigma = ql.SimpleQuote(volatility)
    
    # Build term structures (In[5])
    riskFreeCurve = ql.FlatForward(0, ql.TARGET(), ql.QuoteHandle(r), ql.Actual360())
    volatility_curve = ql.BlackConstantVol(0, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360())
    
    # Create process (In[6])
    process = ql.BlackScholesProcess(
        ql.QuoteHandle(u),
                                   ql.YieldTermStructureHandle(riskFreeCurve),
        ql.BlackVolTermStructureHandle(volatility_curve)
    )
    
    # Set pricing engine (In[7])
    option.setPricingEngine(ql.AnalyticBarrierEngine(process))
    
    return option, u, r, sigma


def calculate_numerical_greeks(option, u, r, sigma, h_u=0.01, h_r=1e-4, h_sigma=1e-4, theta_step_days=1):
    """
    Calculate numerical Greeks exactly as in the notebook
    Reproduces In[10] to In[18] from the book
    """
    # Get base price (In[10], In[11]) - EXACTLY as in notebook
    u0 = u.value()
    h = h_u
    P0 = option.NPV()
    
    # Delta and Gamma calculation (In[12], In[13], In[14], In[15])
    # Step 1: Increase underlying value (In[12])
    u.setValue(u0 + h)
    P_plus = option.NPV()
    
    # Step 2: Decrease underlying value (In[13])
    u.setValue(u0 - h)
    P_minus = option.NPV()
    
    # Step 3: Reset to original value (In[14])
    u.setValue(u0)
    
    # Apply formulas (In[15])
    Delta = (P_plus - P_minus) / (2 * h)
    Gamma = (P_plus - 2 * P0 + P_minus) / (h * h)
    
    # Rho calculation (In[16]) - one-sided formula
    r0 = r.value()
    h_r_used = h_r
    r.setValue(r0 + h_r_used)
    P_plus_rho = option.NPV()
    r.setValue(r0)  # Reset to original value
    Rho = (P_plus_rho - P0) / h_r_used
    
    # Vega calculation (In[17]) - one-sided formula
    sigma0 = sigma.value()
    h_sigma_used = h_sigma
    sigma.setValue(sigma0 + h_sigma_used)
    P_plus_vega = option.NPV()
    sigma.setValue(sigma0)  # Reset to original value
    Vega = (P_plus_vega - P0) / h_sigma_used
    
    # Theta calculation (In[18]) - time step
    today = ql.Settings.instance().evaluationDate
    ql.Settings.instance().evaluationDate = today + theta_step_days
    P1 = option.NPV()
    ql.Settings.instance().evaluationDate = today  # Reset to original date
    h_theta = 1.0 / 365  # Exactly as in notebook
    Theta = (P1 - P0) / h_theta
    
    return {
        'P0': P0,
        'P_plus': P_plus,
        'P_minus': P_minus,
        'Delta': Delta,
        'Gamma': Gamma,
        'Rho': Rho,
        'Vega': Vega,
        'Theta': Theta
    }


def create_price_curve_plot(option, u, plot_range=(80.0, 120.0), num_points=400):
    """
    Create the exact plot from page 23 of the book
    Reproduces the matplotlib plot with underlying values from 80 to 120
    X-axis: underlying value (xs = np.linspace(80.0, 120.0, 400))
    Y-axis: option NPV
    Title: "Option value vs Underlying"
    """
    u_min, u_max = plot_range
    xs = np.linspace(u_min, u_max, num_points)
    ys = []
    
    original_u = u.value()
    
    # Calculate option prices for each underlying value
    for x in xs:
        u.setValue(x)
        try:
            price = option.NPV()
            ys.append(price)
        except:
            ys.append(0.0)  # Handle barrier touched cases
        
        # Reset to original value
    u.setValue(original_u)
    
    # Create the plot exactly as in the book
    plt.figure(figsize=(12, 8))
    plt.plot(xs, ys, 'b-', linewidth=2.5, label='Option Price')
    
    # Add reference lines
    plt.axvline(x=100, color='r', linestyle='--', alpha=0.7, label='Strike Price (100)')
    plt.axvline(x=120, color='g', linestyle='--', alpha=0.7, label='Barrier Level (120)')
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.xlabel('Underlying Value', fontsize=12, fontweight='bold')
    plt.ylabel('Option NPV', fontsize=12, fontweight='bold')
    plt.title('Option value vs Underlying', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Set axis limits for better visualization
    plt.xlim(80, 120)
    plt.ylim(0, max(ys) * 1.1)
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return image_base64


def create_interactive_plot_data(option, u, h_u=1.0, plot_range=(80.0, 120.0), num_points=400):
    """
    Create the EXACT graph from Chapter 3, page 23 using the real barrier option data
    This uses the actual option.NPV() values and creates the finite difference visualization
    """
    original_u = u.value()
    
    # Get the current underlying value and step size from the option
    u0 = original_u
    h = h_u  # Use the actual h value from the form
    
    # Calculate the three specific points for finite difference method
    u_plus = u0 + h
    u_minus = u0 - h
    
    # Get the actual option values at these points
    u.setValue(u_plus)
    try:
        p_plus = option.NPV()
    except:
        p_plus = 0.0
    
    u.setValue(u_minus)
    try:
        p_minus = option.NPV()
    except:
        p_minus = 0.0
    
    u.setValue(u0)
    try:
        p0 = option.NPV()
    except:
        p0 = 0.0
    
    # ==============================================================================
    # SECTION GRAPHIQUE : On revient à la VRAIE valeur de l'option
    # ==============================================================================
    chart_data = {'curve': {'x': [], 'y': []}}
    
    # On définit une plage de visualisation zoomée autour du point de calcul
    x_range_min = original_u - 3 * h
    x_range_max = original_u + 3 * h
    x_values = np.linspace(x_range_min, x_range_max, 100)
    
    # On calcule la VRAIE courbe de valeur
    for x in x_values:
        u.setValue(x)
        chart_data['curve']['x'].append(x)
        try:
            chart_data['curve']['y'].append(option.NPV())
        except RuntimeError:
            chart_data['curve']['y'].append(None)
    
    # On ajoute les données pour les points et la ligne sécante
    chart_data['points'] = [
        {'x': u_minus, 'y': p_minus},
        {'x': original_u, 'y': p0},
        {'x': u_plus, 'y': p_plus}
    ]
    
    # Reset to original value
    u.setValue(original_u)
    
    return chart_data


def calculate_numerical_greeks_lab_api(params):
    """
    Complete API function for Chapter 3 Numerical Greeks Lab
    Returns all Greeks and chart data
    """
    try:
        # Debug: Print parameters
        print(f"DEBUG: Parameters received: {params}")
        
        # Build option
        option, u, r, sigma = build_option(params)
        
        # Debug: Test basic NPV calculation
        basic_npv = option.NPV()
        print(f"DEBUG: Basic NPV: {basic_npv}")
        
        # Calculate numerical Greeks
        greeks_result = calculate_numerical_greeks(
            option, u, r, sigma,
            h_u=params.get('h_underlying', 0.01),
            h_r=params.get('h_rate', 0.0001),
            h_sigma=params.get('h_volatility', 0.0001),
            theta_step_days=1
        )
        
        print(f"DEBUG: Greeks result: {greeks_result}")
        
        # Create chart data with multiple curves
        chart_data = create_greeks_chart_data(option, u, r, sigma, params)
        
        return {
            'success': True,
            'npv': greeks_result['P0'],
            'P_plus': greeks_result['P_plus'],
            'P_minus': greeks_result['P_minus'],
            'delta': greeks_result['Delta'],
            'gamma': greeks_result['Gamma'],
            'rho': greeks_result['Rho'],
            'vega': greeks_result['Vega'],
            'theta': greeks_result['Theta'],
            'chart_data': chart_data
        }
        
    except Exception as e:
        error_msg = str(e)
        if "barrier touched" in error_msg.lower():
            return {
                'success': False,
                'error': f"Barrier touched: The barrier level ({params.get('barrier_level', 'N/A')}) is not appropriate for the barrier type ({params.get('barrier_type', 'N/A')}) with underlying price ({params.get('underlying_price', 'N/A')}). For DownIn/DownOut barriers, the barrier must be below the underlying price. For UpIn/UpOut barriers, the barrier must be above the underlying price."
            }
        else:
            return {
                'success': False,
                'error': error_msg
            }


def create_greeks_chart_data(option, u, r, sigma, params):
    """
    Create chart data with multiple curves (NPV, Delta, Gamma, Rho, Vega)
    """
    # Define underlying price range - use a wider range for better visualization
    u_values = np.linspace(80, 120, 20)  # 20 points from 80 to 120
    
    # Initialize arrays for each Greek
    npv_values = []
    delta_values = []
    gamma_values = []
    rho_values = []
    vega_values = []
        
    original_u = u.value()
    original_r = r.value()
    original_sigma = sigma.value()
    
    for u_val in u_values:
        u.setValue(u_val)
        try:
            # Calculate NPV
            npv = option.NPV()
            npv_values.append(float(npv))
            
            # Calculate Delta (finite difference)
            h = params.get('h_underlying', 0.01)
            u.setValue(u_val + h)
            npv_plus = option.NPV()
            u.setValue(u_val - h)
            npv_minus = option.NPV()
            u.setValue(u_val)
            
            delta = (npv_plus - npv_minus) / (2 * h)
            delta_values.append(float(delta))
            
            # Calculate Gamma
            gamma = (npv_plus - 2 * npv + npv_minus) / (h * h)
            gamma_values.append(float(gamma))
            
            # Calculate Rho
            h_r = params.get('h_rate', 0.0001)
            r.setValue(original_r + h_r)
            npv_rho = option.NPV()
            r.setValue(original_r)
            rho = (npv_rho - npv) / h_r
            rho_values.append(float(rho))
            
            # Calculate Vega
            h_sigma = params.get('h_volatility', 0.0001)
            sigma.setValue(original_sigma + h_sigma)
            npv_vega = option.NPV()
            sigma.setValue(original_sigma)
            vega = (npv_vega - npv) / h_sigma
            vega_values.append(float(vega))
            
        except Exception as e:
            # Handle errors gracefully - append 0 for failed calculations
            npv_values.append(0.0)
            delta_values.append(0.0)
            gamma_values.append(0.0)
            rho_values.append(0.0)
            vega_values.append(0.0)
    
    # Reset to original values
    u.setValue(original_u)
    r.setValue(original_r)
    sigma.setValue(original_sigma)
    
    return {
        'u_values': [float(x) for x in u_values],
        'npv_values': npv_values,
        'delta_values': delta_values,
        'gamma_values': gamma_values,
        'rho_values': rho_values,
        'vega_values': vega_values
    }