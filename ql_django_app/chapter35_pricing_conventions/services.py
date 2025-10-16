# services.py

import QuantLib as ql
import datetime

def analyze_pricing_conventions(data):
    """
    Reproduces the analysis from Chapter 35 to demonstrate the effect
    of mismatched day-count conventions.
    """
    try:
        # 1. Setup from form data
        eval_date = data['evaluation_date']
        today = ql.Date(eval_date.day, eval_date.month, eval_date.year)
        ql.Settings.instance().evaluationDate = today
        
        flat_rate_value = data['flat_rate']
        bond_day_count_str = data['bond_day_count']
        curve_day_count_str = data['curve_day_count']
        
        # Mapping des conventions de décompte
        day_count_map = {
            'Thirty360': ql.Thirty360(ql.Thirty360.BondBasis),
            'Actual360': ql.Actual360(),
        }
        bond_day_count = day_count_map.get(bond_day_count_str)
        curve_day_count = day_count_map.get(curve_day_count_str)

        # 2. Setup commun (courbes, index, schedule)
        discounting_curve = ql.RelinkableYieldTermStructureHandle()
        forecasting_curve = ql.RelinkableYieldTermStructureHandle()
        
        # L'index USDLibor a une convention Actual/360 "codée en dur"
        index = ql.USDLibor(ql.Period(3, ql.Months), forecasting_curve)
        
        schedule = ql.Schedule(today, today + ql.Period(4, ql.Years),
                               ql.Period(3, ql.Months), ql.NullCalendar(),
                               ql.Unadjusted, ql.Unadjusted,
                               ql.DateGeneration.Forward, False)

        # 3. Création de l'obligation avec la convention choisie par l'utilisateur
        bond = ql.FloatingRateBond(
            0, 100.0, schedule, index, bond_day_count,
            fixingDays=0
        )
        bond.setPricingEngine(ql.DiscountingBondEngine(discounting_curve))
        
        # 4. Création de la courbe avec la convention choisie par l'utilisateur
        flat_rate_curve = ql.FlatForward(
            today, flat_rate_value, curve_day_count,
            ql.Compounded, ql.Quarterly
        )
        forecasting_curve.linkTo(flat_rate_curve)
        discounting_curve.linkTo(flat_rate_curve)

        # 5. Calcul du prix et analyse
        price = bond.cleanPrice()
        
        # Extraction des informations pour l'explication
        first_coupon = ql.as_coupon(bond.cashflows()[0])
        
        coupon_details = []
        for cf in bond.cashflows()[:-1]: # Exclure le remboursement
            c = ql.as_coupon(cf)
            
            # Format date comme "October5th,2013"
            date_obj = c.date()
            try:
                iso_str = date_obj.ISO()
                year, month, day = iso_str.split('-')
                day = int(day)
                month = int(month)
                year = int(year)

                month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']

                if 10 <= day % 100 <= 20:
                    suffix = 'th'
                else:
                    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

                formatted_date = f"{month_names[month]}{day}{suffix},{year}"
            except:
                formatted_date = date_obj.ISO()
            
            coupon_details.append({
                'date': formatted_date,
                'rate': c.rate(),
                'accrual_period': c.accrualPeriod()
            })

        return {
            'price': price,
            'analysis': {
                'curve_day_count': flat_rate_curve.dayCounter().name(),
                'bond_day_count': first_coupon.dayCounter().name(),
                'index_day_count': index.dayCounter().name(),
            },
            'coupons': coupon_details
        }

    except Exception as e:
        return {'error': str(e)}
