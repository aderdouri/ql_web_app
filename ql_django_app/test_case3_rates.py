#!/usr/bin/env python3
"""
Test pour diagnostiquer le problème des taux dans le Case 3
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import QuantLib as ql
import datetime

def test_case3_rates():
    print("=== TEST CASE 3: STUB COUPON RATES ===")
    
    # Dates exactes du livre
    today = ql.Date(8, ql.October, 2014)
    ql.Settings.instance().evaluationDate = today
    
    start_date = datetime.date(2014, 10, 15)
    start_date_ql = ql.Date(start_date.day, start_date.month, start_date.year)
    end_date_ql = start_date_ql + ql.Period(3, ql.Months) + ql.Period(5, ql.Years)
    
    print(f"Start Date: {start_date_ql}")
    print(f"End Date: {end_date_ql}")
    print(f"Evaluation Date: {ql.Settings.instance().evaluationDate}")
    
    # Curves et index
    euribor_curve_3m = ql.FlatForward(0, ql.TARGET(), 0.0015, ql.Actual360())
    index_3m = ql.Euribor3M(ql.YieldTermStructureHandle(euribor_curve_3m))
    euribor_curve_6m = ql.FlatForward(0, ql.TARGET(), 0.0020, ql.Actual360())
    index_6m = ql.Euribor6M(ql.YieldTermStructureHandle(euribor_curve_6m))
    
    print(f"3M Rate: {0.0015*100:.4f}%")
    print(f"6M Rate: {0.0020*100:.4f}%")
    
    # Ajouter les fixings
    def add_index_fixings(index, start_date, end_date, rate_value):
        ql.IndexManager.instance().clearHistories()
        fixing_date = start_date - ql.Period(7, ql.Days)
        while fixing_date <= end_date:
            try: 
                index.addFixing(fixing_date, rate_value)
            except RuntimeError: 
                pass
            fixing_date += ql.Period(1, ql.Days)
    
    add_index_fixings(index_3m, start_date_ql, end_date_ql, 0.0015)
    add_index_fixings(index_6m, start_date_ql, end_date_ql, 0.0020)
    
    # Schedule
    schedule = ql.Schedule(start_date_ql, end_date_ql, ql.Period(ql.Semiannual), ql.TARGET(),
                           ql.Following, ql.Following, ql.DateGeneration.Backward, False)
    
    print(f"Schedule dates: {list(schedule)}")
    
    # Créer la jambe standard avec index 6M
    cashflows = ql.IborLeg(nominals=[100.0], schedule=schedule, index=index_6m)
    
    print(f"\n=== AVANT REMPLACEMENT (Index 6M) ===")
    for i, cf in enumerate(cashflows):
        c = ql.as_coupon(cf)
        if c:
            try:
                rate = c.rate() * 100
                amount = cf.amount()
                print(f"Coupon {i}: Rate={rate:.4f}%, Amount={amount:.6f}")
            except Exception as e:
                print(f"Coupon {i}: Error - {e}")
    
    # Remplacer le premier coupon avec index 3M
    first = ql.as_floating_rate_coupon(cashflows[0])
    coupon_3m = ql.IborCoupon(first.date(), first.nominal(),
                              first.accrualStartDate(), first.accrualEndDate(),
                              first.fixingDays(), index_3m)
    coupon_3m.setPricer(ql.BlackIborCouponPricer())
    
    # Créer la nouvelle liste
    new_cashflows = [coupon_3m] + list(cashflows[1:])
    
    print(f"\n=== APRÈS REMPLACEMENT (Premier avec 3M, autres avec 6M) ===")
    for i, cf in enumerate(new_cashflows):
        c = ql.as_coupon(cf)
        if c:
            try:
                rate = c.rate() * 100
                amount = cf.amount()
                index_name = "3M" if i == 0 else "6M"
                print(f"Coupon {i} ({index_name}): Rate={rate:.4f}%, Amount={amount:.6f}")
            except Exception as e:
                print(f"Coupon {i}: Error - {e}")
    
    # Test des fixings
    print(f"\n=== TEST DES FIXINGS ===")
    test_date = ql.Date(15, 1, 2015)
    try:
        fixing_3m = index_3m.fixing(test_date)
        print(f"3M Fixing for {test_date}: {fixing_3m*100:.4f}%")
    except Exception as e:
        print(f"3M Fixing error: {e}")
    
    try:
        fixing_6m = index_6m.fixing(test_date)
        print(f"6M Fixing for {test_date}: {fixing_6m*100:.4f}%")
    except Exception as e:
        print(f"6M Fixing error: {e}")

if __name__ == "__main__":
    test_case3_rates()
