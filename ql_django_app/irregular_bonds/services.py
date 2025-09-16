import QuantLib as ql
import datetime

def add_index_fixings(index, start_date, end_date, base_rate):
    """Add fixings to avoid runtime errors - cover the entire bond period"""
    current_date = start_date
    while current_date <= end_date:
        try:
            # Add fixing for the current date
            ql.IndexManager.instance().setHistory(index.name(), current_date, base_rate)
            current_date = current_date + ql.Period(1, ql.Days)
        except:
            current_date = current_date + ql.Period(1, ql.Days)

def format_cashflows_for_template(cashflows):
    """Format QuantLib cashflows for template display"""
    formatted_cashflows = []
    
    for i, cf in enumerate(cashflows):
        if hasattr(cf, 'date'):
            payment_date = cf.date()
            payment_date_py = ql.Date.to_date(payment_date)
            
            # Format date nicely
            formatted_date = payment_date_py.strftime("%B %d, %Y")
            
            if hasattr(cf, 'amount'):
                amount = cf.amount()
            else:
                amount = 0.0
                
            if hasattr(cf, 'rate'):
                rate = cf.rate()
                rate_percent = rate * 100
            else:
                rate_percent = 0.0
                
            # Check if this is a floating rate coupon
            is_floating = hasattr(cf, 'accrualStartDate') and hasattr(cf, 'accrualEndDate')
            
            if is_floating:
                start_date = cf.accrualStartDate()
                end_date = cf.accrualEndDate()
                start_date_py = ql.Date.to_date(start_date)
                end_date_py = ql.Date.to_date(end_date)
                formatted_start = start_date_py.strftime("%B %d, %Y")
                formatted_end = end_date_py.strftime("%B %d, %Y")
                
                formatted_cashflows.append({
                    'payment_date': formatted_date,
                    'rate': f"{rate_percent:.2f}",
                    'amount': f"{amount:.6f}",
                    'start_date': formatted_start,
                    'end_date': formatted_end,
                    'is_floating': True
                })
            else:
                formatted_cashflows.append({
                    'payment_date': formatted_date,
                    'rate': f"{rate_percent:.2f}",
                    'amount': f"{amount:.6f}",
                    'is_floating': False
                })
    
    return formatted_cashflows

# --- CAS 1: DERNIER COUPON AVANT LA MATURITÉ ---
def build_bond_with_last_coupon_gap(issue_date, maturity_date, coupon_rate, bond_type):
    """Build a bond where the last coupon is paid one period before maturity"""
    # Convert user input dates to QuantLib dates (MODIFICATION POUR RENDRE DYNAMIQUE)
    issue_date_ql = ql.Date(issue_date.day, issue_date.month, issue_date.year)
    maturity_date_ql = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
    
    # Set evaluation date to issue date
    ql.Settings.instance().evaluationDate = issue_date_ql
    
    # Create schedule exactly like in the book
    schedule = ql.Schedule(issue_date_ql, maturity_date_ql,
                          ql.Period(ql.Annual), ql.TARGET(),
                          ql.Following, ql.Following,
                          ql.DateGeneration.Backward, False)
    
    if not list(schedule):
        return {'error': 'Could not generate a schedule for the given dates.'}
    
    N = len(schedule) - 1
    if N <= 0: return {'cashflows': []}

    if bond_type == 'Fixed':
        # Fixed rate bond exactly like in the book
        settlementDays = 3
        faceAmount = 100
        paymentDayCounter = ql.Thirty360(ql.Thirty360.BondBasis)
        coupon_rate_decimal = coupon_rate / 100.0
        coupons = [coupon_rate_decimal] * (N - 1) + [0.0]
        
        bond = ql.FixedRateBond(settlementDays, faceAmount, schedule, coupons, paymentDayCounter)
        
    else: # Floating
        # Use the exact FloatingRateBond approach from the book (Out[8])
        # For public app: Use fixed base rate to match original behavior
        base_rate = 0.002  # Fixed base rate to match original code behavior
        euribor_curve = ql.FlatForward(0, ql.TARGET(), base_rate, ql.Actual360())
        index = ql.Euribor1Y(ql.YieldTermStructureHandle(euribor_curve))
        
        # Add fixings to avoid runtime errors - cover the entire bond period
        add_index_fixings(index, issue_date_ql - ql.Period(5, ql.Days), maturity_date_ql, base_rate)
        
        # Create gearings array exactly like in the book: 1.0 for all coupons except last one (0.0)
        gearings = [1.0] * (N - 1) + [0.0]
        
        # Create FloatingRateBond exactly like in the book (Out[8])
        bond = ql.FloatingRateBond(
            settlementDays=3,
            faceAmount=100,
            schedule=schedule,
            index=index,
            paymentDayCounter=ql.Thirty360(ql.Thirty360.BondBasis),
            paymentConvention=ql.Following,
            fixingDays=index.fixingDays(),
            gearings=gearings,
            spreads=[],
            caps=[],
            floors=[],
            inArrears=False,
            redemption=100.0,
            issueDate=issue_date_ql
        )

    return {'cashflows': format_cashflows_for_template(bond.cashflows())}

# --- CAS 2: OBLIGATION À TAUX FIXE PUIS FLOTTANT ---
def build_fixed_to_floater_bond(issue_date, maturity_date, fixed_years, fixed_rate, float_spread):
    """Build a bond that pays fixed rate for first N years, then floating rate"""
    # Convert dates
    issue_date_ql = ql.Date(issue_date.day, issue_date.month, issue_date.year)
    maturity_date_ql = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
    
    # Set evaluation date
    ql.Settings.instance().evaluationDate = issue_date_ql
    
    # Create schedule
    schedule = ql.Schedule(issue_date_ql, maturity_date_ql,
                          ql.Period(ql.Annual), ql.TARGET(),
                          ql.Following, ql.Following,
                          ql.DateGeneration.Backward, False)
    
    if not list(schedule):
        return {'error': 'Could not generate a schedule for the given dates.'}
    
    N = len(schedule) - 1
    if N <= 0: return {'cashflows': []}

    # Create fixed-to-floater bond
    settlementDays = 3
    faceAmount = 100
    paymentDayCounter = ql.Thirty360(ql.Thirty360.BondBasis)
    
    # Fixed rate for first fixed_years periods
    fixed_rate_decimal = fixed_rate / 100.0
    float_spread_decimal = float_spread / 100.0
    
    # Create coupons array: fixed rate for first fixed_years, then 0 for floating
    coupons = [fixed_rate_decimal] * min(fixed_years, N-1) + [0.0] * max(0, N-1-fixed_years)
    
    # Create floating rate bond with mixed structure
    base_rate = 0.002  # Base floating rate
    euribor_curve = ql.FlatForward(0, ql.TARGET(), base_rate, ql.Actual360())
    index = ql.Euribor1Y(ql.YieldTermStructureHandle(euribor_curve))
    
    # Add fixings
    add_index_fixings(index, issue_date_ql - ql.Period(5, ql.Days), maturity_date_ql, base_rate)
    
    # Gearings: 0 for fixed periods, 1 for floating periods
    gearings = [0.0] * min(fixed_years, N-1) + [1.0] * max(0, N-1-fixed_years)
    
    # Spreads: 0 for fixed periods, float_spread for floating periods
    spreads = [0.0] * min(fixed_years, N-1) + [float_spread_decimal] * max(0, N-1-fixed_years)
    
    bond = ql.FloatingRateBond(
        settlementDays=settlementDays,
        faceAmount=faceAmount,
        schedule=schedule,
        index=index,
        paymentDayCounter=paymentDayCounter,
        paymentConvention=ql.Following,
        fixingDays=index.fixingDays(),
        gearings=gearings,
        spreads=spreads,
        caps=[],
        floors=[],
        inArrears=False,
        redemption=100.0,
        issueDate=issue_date_ql
    )

    return {'cashflows': format_cashflows_for_template(bond.cashflows())}

# --- CAS 3: COUPON STUB ---
def build_stub_coupon_bond(start_date, end_date):
    """Build a bond with irregular first coupon (stub coupon)"""
    # Convert dates
    start_date_ql = ql.Date(start_date.day, start_date.month, start_date.year)
    end_date_ql = ql.Date(end_date.day, end_date.month, end_date.year)
    
    # Set evaluation date
    ql.Settings.instance().evaluationDate = start_date_ql
    
    # Create a short schedule for stub coupon
    schedule = ql.Schedule(start_date_ql, end_date_ql,
                          ql.Period(ql.Annual), ql.TARGET(),
                          ql.Following, ql.Following,
                          ql.DateGeneration.Backward, False)
    
    if not list(schedule):
        return {'error': 'Could not generate a schedule for the given dates.'}
    
    # Create floating rate bond for stub coupon
    settlementDays = 3
    faceAmount = 100
    paymentDayCounter = ql.Thirty360(ql.Thirty360.BondBasis)
    
    base_rate = 0.002
    euribor_curve = ql.FlatForward(0, ql.TARGET(), base_rate, ql.Actual360())
    index = ql.Euribor1Y(ql.YieldTermStructureHandle(euribor_curve))
    
    # Add fixings
    add_index_fixings(index, start_date_ql - ql.Period(5, ql.Days), end_date_ql, base_rate)
    
    # Create floating rate bond for stub coupon
    bond = ql.FloatingRateBond(
        settlementDays=settlementDays,
        faceAmount=faceAmount,
        schedule=schedule,
        index=index,
        paymentDayCounter=paymentDayCounter,
        paymentConvention=ql.Following,
        fixingDays=index.fixingDays(),
        gearings=[1.0],
        spreads=[0.0],
        caps=[],
        floors=[],
        inArrears=False,
        redemption=100.0,
        issueDate=start_date_ql
    )

    return {'cashflows': format_cashflows_for_template(bond.cashflows())}
