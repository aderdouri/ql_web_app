import QuantLib as ql


def analyze_coupon_details(convention_str: str):
    """
    Deconstructs a floating-rate coupon to illustrate the difference between
    the index tenor period and the coupon's actual accrual period, based on a
    user-selected business day convention.
    """
    today = ql.Date(7, ql.January, 2013)
    ql.Settings.instance().evaluationDate = today
    
    # 1. Forward curve from the notebook
    dates, forwards = zip(*[
        (ql.Date(7,1,2013), 0.03613), (ql.Date(8,4,2013), 0.03613),
        (ql.Date(8,7,2013), 0.03384), (ql.Date(7,1,2014), 0.03573),
        (ql.Date(7,7,2014), 0.03445)
    ])
    libor_curve = ql.ForwardCurve(list(dates), list(forwards), ql.Actual365Fixed())

    # 2. Convert the user's string choice into a QuantLib object
    convention_map = {
        'Following': ql.Following,
        'ModifiedFollowing': ql.ModifiedFollowing,
        'Preceding': ql.Preceding,
        'Unadjusted': ql.Unadjusted,
    }
    business_convention = convention_map.get(convention_str, ql.Following)
    
    # 3. Floating leg of the swap
    index = ql.GBPLibor(ql.Period(6, ql.Months), ql.YieldTermStructureHandle(libor_curve))
    calendar = index.fixingCalendar()
    maturity = calendar.advance(today, 1, ql.Years)
    
    # The selected business_convention is now used to build the schedule
    schedule = ql.Schedule(today, maturity, index.tenor(), calendar,
                           business_convention, business_convention,
                           ql.DateGeneration.Backward, False)
                           
    floating_leg = ql.IborLeg([1000000], schedule, index, index.dayCounter())

    # 4. Analysis of the second coupon (the most interesting one)
    # The results of this analysis will change based on the selected convention
    coupon = ql.as_floating_rate_coupon(floating_leg[1])
    
    # Index dates
    fixing_date = coupon.fixingDate()
    index_fixing_rate = index.fixing(fixing_date)
    index_start_date = index.valueDate(fixing_date)
    index_end_date = index.maturityDate(index_start_date)
    
    # Coupon dates
    coupon_start_date = coupon.accrualStartDate()
    coupon_end_date = coupon.accrualEndDate()
    
    # Rates
    index_tenor_rate = libor_curve.forwardRate(index_start_date, index_end_date,
                                               coupon.dayCounter(), ql.Simple).rate()
    coupon_period_rate = libor_curve.forwardRate(coupon_start_date, coupon_end_date,
                                                 coupon.dayCounter(), ql.Simple).rate()
                                                 
    return {
        'fixing_date': fixing_date.ISO(),
        'index_fixing_rate': f"{index_fixing_rate*100:.4f}%",
        'index_start_date': index_start_date.ISO(),
        'index_end_date': index_end_date.ISO(),
        'index_tenor_rate': f"{index_tenor_rate*100:.4f}%",
        'coupon_start_date': coupon_start_date.ISO(),
        'coupon_end_date': coupon_end_date.ISO(),
        'coupon_period_rate': f"{coupon_period_rate*100:.4f}%",
        'coupon_final_rate': f"{coupon.rate()*100:.4f}%",
        'coupon_amount': f"{coupon.amount():,.2f}"
    }