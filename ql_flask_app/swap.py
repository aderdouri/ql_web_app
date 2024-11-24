from flask import Blueprint, request, render_template
import QuantLib as ql

swap_bp = Blueprint('swap', __name__)

@swap_bp.route('/swap')
def swap():
    return render_template('swap.html', swap_value=None)

@swap_bp.route('/swap_value', methods=['GET'])
def swap_value():
    # Get nominal value from query parameters
    nominal = request.args.get('nominal', default=1000000, type=int)

    # Set up QuantLib environment
    calendar = ql.TARGET()
    settlement_date = ql.Date(22, ql.September, 2023)
    settlement_date = calendar.adjust(settlement_date)
    ql.Settings.instance().evaluationDate = settlement_date

    # Define swap parameters
    fixed_rate = 0.02
    floating_spread = 0.001
    fixed_leg_tenor = ql.Period(ql.Annual)
    floating_leg_tenor = ql.Period(ql.Semiannual)
    fixed_leg_daycount = ql.Thirty360(ql.Thirty360.BondBasis)
    floating_leg_daycount = ql.Actual360()
    
    # Create a flat forward curve for the index
    index_term_structure = ql.FlatForward(settlement_date, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
    index = ql.Euribor6M(ql.YieldTermStructureHandle(index_term_structure))

    # Add missing fixing data
    fixing_date = ql.Date(20, ql.September, 2023)
    index.addFixing(fixing_date, 0.005)  # Example fixing rate

    # Create fixed and floating schedules
    fixed_schedule = ql.Schedule(settlement_date,
                                 settlement_date + ql.Period(5, ql.Years),
                                 fixed_leg_tenor,
                                 calendar,
                                 ql.ModifiedFollowing,
                                 ql.ModifiedFollowing,
                                 ql.DateGeneration.Forward,
                                 False)

    floating_schedule = ql.Schedule(settlement_date,
                                    settlement_date + ql.Period(5, ql.Years),
                                    floating_leg_tenor,
                                    calendar,
                                    ql.ModifiedFollowing,
                                    ql.ModifiedFollowing,
                                    ql.DateGeneration.Forward,
                                    False)

    # Create the swap
    swap = ql.VanillaSwap(ql.VanillaSwap.Payer,
                          nominal,
                          fixed_schedule,
                          fixed_rate,
                          fixed_leg_daycount,
                          floating_schedule,
                          index,
                          floating_spread,
                          floating_leg_daycount)

    # Set up the pricing engine
    discount_curve = ql.FlatForward(settlement_date, ql.QuoteHandle(ql.SimpleQuote(0.01)), ql.Actual360())
    engine = ql.DiscountingSwapEngine(ql.YieldTermStructureHandle(discount_curve))
    swap.setPricingEngine(engine)

    # Calculate NPV
    npv = swap.NPV()

    return render_template('swap.html', swap_value=npv)