import QuantLib as ql
import numpy as np
import datetime

def simulate_bond_price_history(data):
    """
    Simulates the price history of a fixed-rate bond over a range of days,
    based on the QuantLib book Chapter 6 implementation.
    """
    try:
        # 1. Setup from form data
        start_date_sim = data['start_date']
        end_date_sim = data['end_date']
        simulation_method = data['simulation_method']
        noise_level = data['noise_level']
        
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # 2. Create the bond (exactly as in the book)
        start_date_bond = ql.Date(8, ql.February, 2016)
        maturity_date_bond = start_date_bond + ql.Period(5, ql.Years)
        schedule = ql.Schedule(start_date_bond, maturity_date_bond, ql.Period(ql.Semiannual),
                               ql.TARGET(), ql.Following, ql.Following,
                               ql.DateGeneration.Backward, False)
        coupons = [0.01] * 10
        bond = ql.FixedRateBond(3, 100.0, schedule, coupons, ql.Thirty360(ql.Thirty360.BondBasis))
        
        # 3. Setup for simulation
        discount_handle = ql.RelinkableYieldTermStructureHandle()
        bond.setPricingEngine(ql.DiscountingBondEngine(discount_handle))
        
        # Base rates (exactly as in the book)
        base_rates = np.array([0.007, 0.010, 0.012, 0.013, 0.014, 0.016, 0.017, 0.018, 0.020, 0.021, 0.022])

        # Convert dates and validate
        current_date = ql.Date(end_date_sim.day, end_date_sim.month, end_date_sim.year)
        first_date = ql.Date(start_date_sim.day, start_date_sim.month, start_date_sim.year)
        
        # Validate date range
        if first_date >= current_date:
            if first_date == current_date:
                return {'error': f'Simulation error: start date ({start_date_sim}) and end date ({end_date_sim}) cannot be identical. Please select different dates.'}
            else:
                return {'error': f'Simulation error: start date ({start_date_sim}) must be before end date ({end_date_sim}). Please select different dates.'}
        
        # Ensure dates are within bond lifetime
        if current_date > maturity_date_bond:
            current_date = maturity_date_bond
        if first_date < start_date_bond:
            first_date = start_date_bond
            
        # Final validation
        if first_date >= current_date:
            return {'error': f'Simulation error: invalid date range. Start date ({start_date_sim}) must be before end date ({end_date_sim}) and within bond lifetime (2016-2021).'}

        prices = {}
        calendar = ql.TARGET()

        # 4. Execute simulation (exactly as in the book)
        if simulation_method == 'rebuild_curve':
            # Method 1: Rebuild curve for each date
            date = current_date
            while date >= first_date:
                ql.Settings.instance().evaluationDate = date
                # Build nodes from current date (as in book)
                nodes = [date + ql.Period(i, ql.Years) for i in range(11)]
                # Generate random rates (as in book)
                rates = base_rates * np.random.normal(loc=1.0, scale=noise_level, size=base_rates.shape)
                discount_curve = ql.ZeroCurve(nodes, list(rates), ql.Actual360())
                discount_handle.linkTo(discount_curve)
                
                prices[date] = bond.cleanPrice()
                date = calendar.advance(date, -1, ql.Days)

        elif simulation_method == 'update_quotes':
            # Method 2: True quotes method (as in QuantLib book)
            # Create quotes and helpers for OIS rates
            quotes = []
            helpers = []
            index = ql.Eonia()
            tenors = [ql.Period(i, ql.Years) for i in range(1, 11)]
            
            for tenor, rate in zip(tenors, base_rates):
                q = ql.SimpleQuote(rate)
                h = ql.OISRateHelper(2, tenor, ql.QuoteHandle(q), index)
                quotes.append(q)
                helpers.append(h)
            
            # Create risk-free curve from helpers
            risk_free_curve = ql.PiecewiseFlatForward(0, ql.TARGET(), helpers, ql.Actual360())
            
            # Add credit spread
            spread = ql.SimpleQuote(0.01)
            discount_curve = ql.ZeroSpreadedTermStructure(
                ql.YieldTermStructureHandle(risk_free_curve),
                ql.QuoteHandle(spread))
            discount_handle.linkTo(discount_curve)
            
            date = current_date
            while date >= first_date:
                ql.Settings.instance().evaluationDate = date
                
                # Update quotes with new rates (this triggers curve recalculation)
                new_rates = base_rates * np.random.normal(loc=1.0, scale=noise_level, size=base_rates.shape)
                for q, r in zip(quotes, new_rates):
                    q.setValue(r)
                
                # Update spread
                spread.setValue(spread.value() * np.random.normal(loc=1.0, scale=noise_level))
                
                # The curve automatically updates when quotes change
                prices[date] = bond.cleanPrice()
                date = calendar.advance(date, -1, ql.Days)

        # 5. Format results for chart
        sorted_prices = sorted(prices.items())
        dates = [item[0].ISO() for item in sorted_prices]
        price_values = [item[1] for item in sorted_prices]
        
        return {'price_history': {'dates': dates, 'prices': price_values}}
        
    except Exception as e:
        return {'error': f'Simulation error: {str(e)}'}