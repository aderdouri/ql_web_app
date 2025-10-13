# services.py

import QuantLib as ql
import datetime

def analyze_rho_for_black_process(form_data):
    """
    Reproduces the analysis from Chapter 26 to demonstrate the rho calculation glitch
    for the BlackProcess.
    """
    try:
        # 1. Setup from form data
        eval_date = form_data['evaluation_date']
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = today
        
        underlying_price = form_data['underlying_price']
        risk_free_rate = form_data['risk_free_rate']
        volatility = form_data['volatility']
        strike_price = form_data['strike_price']
        days_to_expiry = form_data['days_to_expiry']
        
        # 2. Create market data objects
        u = ql.SimpleQuote(underlying_price)
        r = ql.SimpleQuote(risk_free_rate)
        sigma = ql.SimpleQuote(volatility)
        
        risk_free_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.QuoteHandle(r), ql.Actual360()))
        volatility_curve = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.TARGET(), ql.QuoteHandle(sigma), ql.Actual360()))

        # --- Case 1: BlackScholesProcess (for a stock with no dividends) ---
        process_1 = ql.BlackScholesProcess(ql.QuoteHandle(u), risk_free_curve, volatility_curve)
        option_1 = ql.EuropeanOption(
            ql.PlainVanillaPayoff(ql.Option.Call, strike_price),
            ql.EuropeanExercise(today + days_to_expiry)
        )
        option_1.setPricingEngine(ql.AnalyticEuropeanEngine(process_1))
        
        # --- Case 2: BlackProcess (for a future) ---
        process_2 = ql.BlackProcess(ql.QuoteHandle(u), risk_free_curve, volatility_curve)
        option_2 = ql.EuropeanOption(
            ql.PlainVanillaPayoff(ql.Option.Call, strike_price),
            ql.EuropeanExercise(today + days_to_expiry)
        )
        option_2.setPricingEngine(ql.AnalyticEuropeanEngine(process_2))

        # 3. Helper function for numerical greeks (from the book)
        def greek(option, quote, dx):
            x0 = quote.value()
            quote.setValue(x0 + dx); p_u = option.NPV()
            quote.setValue(x0 - dx); p_d = option.NPV()
            quote.setValue(x0) # Reset
            return (p_u - p_d) / (2 * dx)

        # 4. Perform all calculations
        # Compute dividend/risk-free rates
        process_1_div_ir = process_1.dividendYield().zeroRate(1.0, ql.Continuous)
        process_2_rf_ir  = process_2.riskFreeRate().zeroRate(1.0, ql.Continuous)
        process_2_div_ir = process_2.dividendYield().zeroRate(1.0, ql.Continuous)

        # Numeric percent values (for potential charts/logic)
        process_1_div_pct = process_1_div_ir.rate() * 100.0
        process_2_div_pct = process_2_div_ir.rate() * 100.0

        # Pre-formatted strings to match the book's exact output style
        process_1_div_display = f"{process_1_div_pct:.6f} % Actual/365 (Fixed) continuous compounding"
        process_2_div_display = f"{process_2_div_pct:.6f} % Actual/360 continuous compounding"

        # Calculate all values first
        option_1_npv = option_1.NPV()
        option_2_npv = option_2.NPV()
        option_1_rho_analytic = option_1.rho()
        option_1_rho_numeric = greek(option_1, r, 0.001)
        option_2_rho_analytic = option_2.rho()
        option_2_rho_numeric = greek(option_2, r, 0.001)
        option_2_rho_corrected = option_2.rho() + option_2.dividendRho()
        dividend_rho = option_2.dividendRho()

        results = {
            # Raw interest rate objects (if ever needed elsewhere)
            'process_1_div_yield': process_1_div_ir,
            'process_2_risk_free': process_2_rf_ir,
            'process_2_div_yield': process_2_div_ir,

            # Numeric and display-friendly values
            'process_1_div_yield_pct': process_1_div_pct,
            'process_2_div_yield_pct': process_2_div_pct,
            'process_1_div_yield_display': process_1_div_display,
            'process_2_div_yield_display': process_2_div_display,
            
            'option_1_npv': option_1_npv,
            'option_2_npv': option_2_npv,
            'price_difference': abs(option_1_npv - option_2_npv),
            
            'option_1_delta_analytic': option_1.delta(),
            'option_1_delta_numeric': greek(option_1, u, 0.01),
            'option_2_delta_analytic': option_2.delta(),
            'option_2_delta_numeric': greek(option_2, u, 0.01),
            
            'option_1_vega_analytic': option_1.vega(),
            'option_1_vega_numeric': greek(option_1, sigma, 0.001),
            'option_2_vega_analytic': option_2.vega(),
            'option_2_vega_numeric': greek(option_2, sigma, 0.001),

            'option_1_rho_analytic': option_1_rho_analytic,
            'option_1_rho_numeric': option_1_rho_numeric,
            'bs_rho_difference': abs(option_1_rho_analytic - option_1_rho_numeric),
            
            # The "glitch" part
            'option_2_rho_analytic': option_2_rho_analytic,
            'option_2_rho_numeric': option_2_rho_numeric,
            'black_rho_difference': abs(option_2_rho_analytic - option_2_rho_numeric),
            
            # The verification
            'option_2_rho_corrected': option_2_rho_corrected,
            'dividend_rho': dividend_rho,
            'correction_difference': abs(option_2_rho_corrected - option_2_rho_numeric)
        }
        return results

    except Exception as e:
        return {'error': str(e)}