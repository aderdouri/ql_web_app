from django.test import TestCase
from .services import analyze_swap_coupons, setup_market_data
from .models import SwapAnalysisResult

class SwapAnalysisTestCase(TestCase):
    def setUp(self):
        self.test_data = {
            'notional': 1000000,
            'swap_length': 1.0,
            'evaluation_date': '2013-01-07'
        }
    
    def test_swap_analysis_success(self):
        """Test successful swap analysis"""
        results = analyze_swap_coupons(**self.test_data)
        self.assertTrue(results['success'])
        self.assertIn('swap_info', results)
        self.assertIn('par_coupons', results)
        self.assertIn('indexed_coupons', results)
        self.assertIn('comparison', results)
    
    def test_par_coupons_only(self):
        """Test analysis with only par coupons"""
        results = analyze_swap_coupons(
            use_par=True, 
            use_indexed=False, 
            **self.test_data
        )
        self.assertTrue(results['success'])
        self.assertIn('par_coupons', results)
        self.assertNotIn('indexed_coupons', results)
        self.assertNotIn('comparison', results)
    
    def test_indexed_coupons_only(self):
        """Test analysis with only indexed coupons"""
        results = analyze_swap_coupons(
            use_par=False, 
            use_indexed=True, 
            **self.test_data
        )
        self.assertTrue(results['success'])
        self.assertNotIn('par_coupons', results)
        self.assertIn('indexed_coupons', results)
        self.assertNotIn('comparison', results)
    
    def test_market_data_setup(self):
        """Test market data setup"""
        ql_date, libor_curve = setup_market_data('2013-01-07')
        self.assertIsNotNone(ql_date)
        self.assertIsNotNone(libor_curve)
    
    def test_model_creation(self):
        """Test SwapAnalysisResult model creation"""
        result = SwapAnalysisResult.objects.create(
            analysis_type='comparison',
            notional=1000000,
            swap_length=1.0,
            evaluation_date='2013-01-07',
            coupon_data=[],
            par_coupon_amounts=[],
            indexed_coupon_amounts=[],
            difference_analysis=[],
            total_par_amount=1000,
            total_indexed_amount=1005,
            difference_amount=-5,
            max_rate_difference=0.001
        )
        self.assertEqual(result.notional, 1000000)
        self.assertTrue(result.has_significant_difference)

















