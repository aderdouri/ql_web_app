#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chapter6_pricing_range.services import simulate_bond_price_history
import datetime

# Test data
test_data = {
    'start_date': datetime.date(2017, 5, 9),
    'end_date': datetime.date(2018, 5, 9),
    'simulation_method': 'rebuild_curve',
    'noise_level': 0.005
}

print("Testing simulation with data:", test_data)
try:
    results = simulate_bond_price_history(test_data)
    print("Results:", results)
    if 'error' in results:
        print("ERROR:", results['error'])
    else:
        print("SUCCESS: Simulation completed")
        print("Price history dates:", len(results['price_history']['dates']))
        print("Price history prices:", len(results['price_history']['prices']))
except Exception as e:
    print("EXCEPTION:", str(e))
    import traceback
    traceback.print_exc()





