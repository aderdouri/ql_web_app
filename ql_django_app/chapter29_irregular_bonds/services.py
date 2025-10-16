# irregular_bonds/services.py (VERSION FINALE, CORRIGÉE ET GARANTIE)

import QuantLib as ql
import datetime

def format_date_like_book(date_ql):
    """Formate une date QuantLib au format 'January15th,2015' comme dans le livre."""
    if not date_ql:
        return ''
    
    # Extraire les composants de la date
    day = date_ql.dayOfMonth()
    month = date_ql.month()
    year = date_ql.year()
    
    # Noms des mois
    month_names = [
        '', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # Format du jour avec suffixe (1st, 2nd, 3rd, 4th, etc.)
    if day in [1, 21, 31]:
        day_suffix = 'st'
    elif day in [2, 22]:
        day_suffix = 'nd'
    elif day in [3, 23]:
        day_suffix = 'rd'
    else:
        day_suffix = 'th'
    
    return f"{month_names[month]}{day}{day_suffix},{year}"

def format_cashflows_for_template(cashflows, include_accrual_dates=False):
    """Utilitaire pour formater les cashflows pour l'affichage HTML."""
    formatted_cfs = []
    for cf in cashflows:
        c = ql.as_coupon(cf)
        rate_str = ''
        start_date = ''
        end_date = ''
        
        if c:
            try:
                rate_str = f"{c.rate()*100:.4f} %"
                if include_accrual_dates:
                    start_date = format_date_like_book(c.accrualStartDate())
                    end_date = format_date_like_book(c.accrualEndDate())
            except RuntimeError:
                rate_str = 'N/A'  # Si le fixing manque
                if include_accrual_dates:
                    start_date = 'N/A'
                    end_date = 'N/A'
        
        if isinstance(cf, ql.Redemption):
            rate_str = '' # Pas de taux pour le remboursement
            if include_accrual_dates:
                start_date = ''
                end_date = ''
        
        try:
            amount = cf.amount()
        except RuntimeError:
            amount = 0.0  # Si le fixing manque, montant = 0
        
        result = {
            'date': format_date_like_book(cf.date()),
            'rate': rate_str,
            'amount': amount
        }
        
        if include_accrual_dates:
            result['start_date'] = start_date
            result['end_date'] = end_date
        
        formatted_cfs.append(result)
    return formatted_cfs

def add_index_fixings(index, start_date, end_date, rate_value):
    """Utilitaire pour ajouter des fixings historiques à un index."""
    ql.IndexManager.instance().clearHistories()
    fixing_date = start_date - ql.Period(7, ql.Days)
    while fixing_date <= end_date:
        try: 
            index.addFixing(fixing_date, rate_value)
        except RuntimeError: 
            pass
        fixing_date += ql.Period(1, ql.Days)

# --- CAS 1: DERNIER COUPON AVANT LA MATURITÉ (FIDÈLE AU LIVRE) ---
def build_bond_with_last_coupon_gap(issue_date, maturity_date, coupon_rate, bond_type):
    try:
        # Dates comme dans le livre
        today = ql.Date(8, ql.October, 2014)
        ql.Settings.instance().evaluationDate = today
        
        issue_date_ql = ql.Date(issue_date.day, issue_date.month, issue_date.year)
        maturity_date_ql = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
        
        schedule = ql.Schedule(issue_date_ql, maturity_date_ql, ql.Period(ql.Annual), ql.TARGET(),
                               ql.Following, ql.Following, ql.DateGeneration.Backward, False)
        
        if not list(schedule): 
            return {'error': 'Could not generate a schedule.'}
        N = len(schedule) - 1
        if N <= 0: 
            return {'cashflows': []}
        
        if bond_type == 'Fixed':
            # Code exact du livre
            settlementDays = 3
            faceAmount = 100
            paymentDayCounter = ql.Thirty360(ql.Thirty360.BondBasis)
            coupon_rate_decimal = coupon_rate / 100.0
            coupons = [coupon_rate_decimal] * (N - 1) + [0.0]
            bond = ql.FixedRateBond(settlementDays, faceAmount, schedule, coupons, paymentDayCounter)
        else:
            # Code exact du livre pour floating
            euribor_curve = ql.FlatForward(0, ql.TARGET(), 0.002, ql.Actual360())
            index = ql.Euribor1Y(ql.YieldTermStructureHandle(euribor_curve))
            add_index_fixings(index, issue_date_ql, maturity_date_ql, 0.002)
            gearings = [1.0] * (N - 1) + [0.0]
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
        
        return {'cashflows': format_cashflows_for_template(bond.cashflows(), include_accrual_dates=False)}
    except Exception as e:
        return {'error': str(e)}

# --- CAS 2: OBLIGATION FIXED-TO-FLOATER (FIDÈLE AU LIVRE) ---
def build_fixed_to_floater_bond(issue_date, maturity_date, fixed_rate, float_spread, fixed_years):
    try:
        # Dates comme dans le livre
        today = ql.Date(8, ql.October, 2014)
        ql.Settings.instance().evaluationDate = today
        
        issue_date_ql = ql.Date(issue_date.day, issue_date.month, issue_date.year)
        maturity_date_ql = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
        
        # Schedule complet comme dans le livre
        schedule = ql.Schedule(issue_date_ql, maturity_date_ql, ql.Period(ql.Annual), ql.TARGET(),
                               ql.Following, ql.Following, ql.DateGeneration.Backward, False)
        
        if not list(schedule): 
            return {'error': 'Could not generate a schedule.'}

        # Index comme dans le livre
        euribor_curve = ql.FlatForward(0, ql.TARGET(), 0.002, ql.Actual360())
        index = ql.Euribor1Y(ql.YieldTermStructureHandle(euribor_curve))
        add_index_fixings(index, issue_date_ql, maturity_date_ql, 0.002)

        # Code exact du livre - CORRECTION: pas de dayCounter dans IborLeg
        fixed = ql.FixedRateLeg(schedule=schedule, dayCount=ql.Actual360(), 
                               nominals=[100.0], couponRates=[fixed_rate / 100.0])
        floating = ql.IborLeg(nominals=[100.0], schedule=schedule, index=index, 
                             spreads=[float_spread / 100.0])
        
        # Combinaison comme dans le livre
        cashflows = list(fixed[:fixed_years]) + list(floating[fixed_years:]) + [ql.Redemption(100.0, maturity_date_ql)]
        
        bond = ql.Bond(3, ql.TARGET(), 100.0, maturity_date_ql, issue_date_ql, cashflows)
        
        return {'cashflows': format_cashflows_for_template(bond.cashflows(), include_accrual_dates=False)}
    except Exception as e:
        return {'error': str(e)}

# --- CAS 3: PREMIER COUPON IRRÉGULIER (STUB) ---
def build_bond_with_stub_coupon(start_date, stub_months, total_years):
    try:
        # Dates exactes du livre
        today = ql.Date(8, ql.October, 2014)
        ql.Settings.instance().evaluationDate = today
        
        start_date_ql = ql.Date(start_date.day, start_date.month, start_date.year)
        end_date_ql = start_date_ql + ql.Period(stub_months, ql.Months) + ql.Period(total_years, ql.Years)

        # Curves et index exacts du livre
        euribor_curve_3m = ql.FlatForward(0, ql.TARGET(), 0.0015, ql.Actual360())
        index_3m = ql.Euribor3M(ql.YieldTermStructureHandle(euribor_curve_3m))
        euribor_curve_6m = ql.FlatForward(0, ql.TARGET(), 0.0020, ql.Actual360())
        index_6m = ql.Euribor6M(ql.YieldTermStructureHandle(euribor_curve_6m))

        add_index_fixings(index_3m, start_date_ql, end_date_ql, 0.0015)
        add_index_fixings(index_6m, start_date_ql, end_date_ql, 0.0020)

        # Schedule exact du livre
        schedule = ql.Schedule(start_date_ql, end_date_ql, ql.Period(ql.Semiannual), ql.TARGET(),
                               ql.Following, ql.Following, ql.DateGeneration.Backward, False)
        
        if not list(schedule): 
            return {'error': 'Could not generate schedule.'}

        # ==============================================================================
        # CODE EXACT DU LIVRE : In[23] et In[25]
        # ==============================================================================
        
        # D'abord créer la jambe standard avec index 6M (In[23])
        cashflows = ql.IborLeg(nominals=[100.0], schedule=schedule, index=index_6m)
        
        # Ensuite remplacer le premier coupon avec index 3M (In[25])
        first = ql.as_floating_rate_coupon(cashflows[0])
        coupon_3m = ql.IborCoupon(first.date(), first.nominal(),
                                  first.accrualStartDate(), first.accrualEndDate(),
                                  first.fixingDays(), index_3m)
        coupon_3m.setPricer(ql.BlackIborCouponPricer())
        
        # Créer la nouvelle liste de cashflows
        cashflows = [coupon_3m] + list(cashflows[1:])

        return {'cashflows': format_cashflows_for_template(cashflows, include_accrual_dates=True)}

    except Exception as e:
        return {'error': str(e)}