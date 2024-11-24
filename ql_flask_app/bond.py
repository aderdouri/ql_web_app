from flask import Blueprint, request, render_template
import QuantLib as ql

bond_bp = Blueprint('bond', __name__)

@bond_bp.route('/bond')
def bond():
    return render_template('bond.html', bond_value=None)

@bond_bp.route('/bond_value', methods=['GET'])
def bond_value():
    # Get bond parameters from query parameters
    face_value = request.args.get('face_value', default=1000, type=float)
    coupon_rate = request.args.get('coupon_rate', default=5.0, type=float) / 100
    maturity_date_str = request.args.get('maturity_date', default='2025-12-31')
    maturity_date = ql.Date(*map(int, maturity_date_str.split('-')[::-1]))

    # Set up QuantLib environment
    calendar = ql.TARGET()
    settlement_date = ql.Date(22, ql.September, 2023)
    settlement_date = calendar.adjust(settlement_date)
    ql.Settings.instance().evaluationDate = settlement_date

    # Define bond parameters
    issue_date = settlement_date
    tenor = ql.Period(ql.Annual)
    day_count = ql.Thirty360()
    business_convention = ql.ModifiedFollowing
    redemption = 100

    # Create the schedule
    schedule = ql.Schedule(issue_date,
                           maturity_date,
                           tenor,
                           calendar,
                           business_convention,
                           business_convention,
                           ql.DateGeneration.Backward,
                           False)

    # Create the bond
    fixed_rate_bond = ql.FixedRateBond(0, face_value, schedule, [coupon_rate], day_count)

    # Set up the pricing engine
    discount_curve = ql.FlatForward(settlement_date, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
    bond_engine = ql.DiscountingBondEngine(ql.YieldTermStructureHandle(discount_curve))
    fixed_rate_bond.setPricingEngine(bond_engine)

    # Calculate NPV
    bond_value = fixed_rate_bond.NPV()

    return render_template('bond.html', bond_value=bond_value)