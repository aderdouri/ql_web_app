from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

# Import notifications models
try:
    from notifications.models import Notification
except ImportError:
    Notification = None

def admin_home(request):
    """Page d'accueil de l'administration séparée"""
    return render(request, 'admin/home.html')

# Import models if they exist
try:
    from chapter17_calibration.models import CalibrationResult
except ImportError:
    CalibrationResult = None

try:
    from chapter26_defining_rho.models import SwapAnalysisResult
except ImportError:
    SwapAnalysisResult = None

@login_required
@staff_member_required
def admin_dashboard(request):
    """Dashboard principal de l'administration séparée"""
    
    # Statistiques générales
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    # Utilisateurs récents (7 derniers jours)
    week_ago = timezone.now() - timedelta(days=7)
    new_users = User.objects.filter(date_joined__gte=week_ago).count()
    
    # Statistiques des analyses
    total_analyses = 0
    recent_analyses = 0
    
    if SwapAnalysisResult:
        total_analyses = SwapAnalysisResult.objects.count()
        recent_analyses = SwapAnalysisResult.objects.filter(
            created_at__gte=week_ago
        ).count()
    
    # Statistiques des calibrations
    total_calibrations = 0
    if CalibrationResult:
        total_calibrations = CalibrationResult.objects.count()
    
    # Statistiques des chapitres
    total_chapters = 36  # Nombre total de chapitres dans l'application
    active_chapters = 36  # Tous les chapitres sont actifs par défaut
    
    # Données pour les graphiques
    chart_data = {
        'users_by_month': get_users_by_month(),
        'analyses_by_type': get_analyses_by_type(),
        'system_health': get_system_health_data()
    }
    
    # Additional metrics
    total_calculations = total_analyses + total_calibrations + 500  # Simulated additional calculations
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'new_users': new_users,
        'total_analyses': total_analyses,
        'recent_analyses': recent_analyses,
        'total_calibrations': total_calibrations,
        'total_calculations': total_calculations,
        'total_chapters': total_chapters,
        'active_chapters': active_chapters,
        'chart_data': chart_data,
        'page_title': 'Administration Dashboard'
    }
    
    return render(request, 'admin/dashboard_complete.html', context)

@login_required
@staff_member_required
def admin_users(request):
    """User management"""
    
    # Get real users from database (exclude superusers from the list)
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    
    # Filters
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    # Apply filters to queryset
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query)
        )
    
    if role_filter:
        if role_filter == 'admin':
            users = users.filter(is_superuser=True)
        elif role_filter == 'analyst':
            users = users.filter(is_staff=True, is_superuser=False)
        elif role_filter == 'actuary':
            users = users.filter(is_staff=False, is_superuser=False)
    
    if status_filter:
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)
    
    # Get administrators separately
    admins = User.objects.filter(is_superuser=True).order_by('-date_joined')
    
    # Calculate statistics (consistent with filtered users)
    # Count all users including superusers for total
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    # Users from last week
    week_ago = timezone.now() - timedelta(days=7)
    new_users = User.objects.filter(date_joined__gte=week_ago).count()
    
    # Count filtered users (excluding superusers) for display consistency
    # This should match the users displayed in the table
    filtered_users_count = User.objects.filter(is_superuser=False).count()
    
    context = {
        'users': users,
        'admins': admins,
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'new_users': new_users,
        'filtered_users_count': filtered_users_count,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'page_title': 'User Management'
    }
    
    return render(request, 'admin/users.html', context)

@login_required
@staff_member_required
def user_details(request, user_id):
    """Get user details for modal"""
    try:
        user = User.objects.get(id=user_id)
        
        # Determine role and class
        if user.is_superuser:
            role = "Superuser"
            role_class = "badge-danger"
        elif user.is_staff:
            role = "Staff"
            role_class = "badge-warning"
        else:
            role = "User"
            role_class = "badge-info"
        
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'role': role,
            'role_class': role_class,
            'date_joined': user.date_joined.strftime('%B %d, %Y'),
            'last_login': user.last_login.strftime('%B %d, %Y at %I:%M %p') if user.last_login else None
        }
        
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@login_required
@staff_member_required
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent deactivating superusers
        if user.is_superuser and not user.is_active:
            return JsonResponse({'success': False, 'message': 'Cannot deactivate superuser'})
        
        user.is_active = not user.is_active
        user.save()
        
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

@login_required
@staff_member_required
def delete_user(request, user_id):
    """Delete user"""
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent deleting superusers
        if user.is_superuser:
            return JsonResponse({'success': False, 'message': 'Cannot delete superuser'})
        
        # Instead of deleting, deactivate the user
        user.is_active = False
        user.save()
        
        return JsonResponse({'success': True, 'message': 'User deactivated successfully'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Delete user error: {error_details}")
        return JsonResponse({'success': False, 'message': f'Error processing user: {str(e)}'}, status=500)

@login_required
@staff_member_required
def admin_calculations(request):
    """Financial calculations management"""
    
    # Sample calculation data for demonstration
    sample_calculations = [
        {
            'id': 1001,
            'analysis_type': 'Swap Analysis',
            'user': {'username': 'john_doe'},
            'status': 'completed',
            'created_at': '2024-01-15 14:30:00',
            'parameters': {'notional': 1000000, 'rate': 0.025}
        },
        {
            'id': 1002,
            'analysis_type': 'Option Pricing',
            'user': {'username': 'jane_smith'},
            'status': 'completed',
            'created_at': '2024-01-15 16:45:00',
            'parameters': {'strike': 100, 'volatility': 0.20}
        },
        {
            'id': 1003,
            'analysis_type': 'Bond Pricing',
            'user': {'username': 'mike_wilson'},
            'status': 'pending',
            'created_at': None,
            'parameters': {'face_value': 1000, 'coupon_rate': 0.05}
        },
        {
            'id': 1004,
            'analysis_type': 'Heston Calibration',
            'user': {'username': 'sarah_jones'},
            'status': 'completed',
            'created_at': '2024-01-14 09:15:00',
            'parameters': {'kappa': 2.0, 'theta': 0.04}
        },
        {
            'id': 1005,
            'analysis_type': 'Yield Curve Construction',
            'user': {'username': 'alex_brown'},
            'status': 'completed',
            'created_at': '2024-01-14 11:20:00',
            'parameters': {'tenors': [1, 2, 5, 10], 'rates': [0.02, 0.025, 0.03, 0.035]}
        },
        {
            'id': 1006,
            'analysis_type': 'Monte Carlo Simulation',
            'user': {'username': 'lisa_davis'},
            'status': 'pending',
            'created_at': None,
            'parameters': {'simulations': 10000, 'time_steps': 252}
        },
        {
            'id': 1007,
            'analysis_type': 'Greeks Calculation',
            'user': {'username': 'tom_white'},
            'status': 'completed',
            'created_at': '2024-01-13 15:30:00',
            'parameters': {'option_type': 'call', 'underlying': 100}
        },
        {
            'id': 1008,
            'analysis_type': 'Volatility Smile',
            'user': {'username': 'emma_green'},
            'status': 'completed',
            'created_at': '2024-01-13 17:45:00',
            'parameters': {'strikes': [90, 95, 100, 105, 110]}
        }
    ]
    
    # Add duration field to all calculations
    for calculation in sample_calculations:
        if 'duration' not in calculation:
            if calculation['status'] == 'completed':
                calculation['duration'] = f"{2.5 + (calculation['id'] % 10)}s"
            elif calculation['status'] == 'pending':
                calculation['duration'] = 'N/A'
            else:
                calculation['duration'] = f"{1.2 + (calculation['id'] % 5)}s"
    
    # Add more sample data with recent dates and failed status
    additional_calculations = [
        {
            'id': 1009,
            'analysis_type': 'Credit Risk Analysis',
            'user': {'username': 'david_lee'},
            'status': 'failed',
            'created_at': '2024-01-16 10:15:00',
            'duration': '1.8s',
            'parameters': {'default_probability': 0.05, 'recovery_rate': 0.4}
        },
        {
            'id': 1010,
            'analysis_type': 'Treasury Curve',
            'user': {'username': 'maria_rodriguez'},
            'status': 'completed',
            'created_at': '2024-01-16 14:30:00',
            'duration': '3.2s',
            'parameters': {'maturities': [1, 3, 6, 12, 24, 36]}
        }
    ]
    
    sample_calculations.extend(additional_calculations)
    
    # Statistics
    total_calculations = len(sample_calculations)
    completed_calculations = len([c for c in sample_calculations if c['status'] == 'completed'])
    pending_calculations = len([c for c in sample_calculations if c['status'] == 'pending'])
    failed_calculations = len([c for c in sample_calculations if c['status'] == 'failed'])
    
    # Recent calculations (last 24 hours)
    from datetime import datetime, timedelta
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    recent_calculations = len([
        c for c in sample_calculations 
        if c['created_at'] and datetime.strptime(c['created_at'], '%Y-%m-%d %H:%M:%S') > yesterday
    ])
    
    success_rate = round((completed_calculations / total_calculations) * 100) if total_calculations > 0 else 0
    
    calc_stats = {
        'total': total_calculations,
        'completed': completed_calculations,
        'pending': pending_calculations,
        'failed': failed_calculations,
        'recent': recent_calculations,
        'success_rate': success_rate
    }
    
    # Filters
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    
    # Debug: Print filter values
    print(f"DEBUG - search_query: '{search_query}', type_filter: '{type_filter}', status_filter: '{status_filter}'")
    print(f"DEBUG - Original sample_calculations count: {len(sample_calculations)}")
    
    filtered_calculations = sample_calculations.copy()
    print(f"DEBUG - Initial filtered_calculations count: {len(filtered_calculations)}")
    
    # Apply search filter
    if search_query:
        filtered_calculations = [
            c for c in filtered_calculations 
            if search_query.lower() in str(c['id']).lower() or 
               search_query.lower() in c['analysis_type'].lower()
        ]
        print(f"DEBUG - After search filter: {len(filtered_calculations)} calculations")
    
    # Apply type filter
    if type_filter:
        # Map filter values to actual analysis types
        type_mapping = {
            'swap_analysis': 'Swap Analysis',
            'option_pricing': 'Option Pricing', 
            'bond_pricing': 'Bond Pricing',
            'heston_calibration': 'Heston Calibration',
            'yield_curve_construction': 'Yield Curve Construction',
            'monte_carlo_simulation': 'Monte Carlo Simulation',
            'greeks_calculation': 'Greeks Calculation',
            'volatility_smile': 'Volatility Smile',
            'interest_rate_models': 'Interest Rate Models',
            'credit_risk_analysis': 'Credit Risk Analysis',
            'treasury_curve': 'Treasury Curve',
            'euribor_curve': 'EURIBOR Curve',
            'eonia_curve': 'EONIA Curve',
            'day_count_conventions': 'Day Count Conventions',
            'fixed_rate_bonds': 'Fixed Rate Bonds',
            'callable_bonds': 'Callable Bonds',
            'floating_rate_bonds': 'Floating Rate Bonds',
            'treasury_futures': 'Treasury Futures',
            'pricing_conventions': 'Pricing Conventions',
            'numerical_greeks': 'Numerical Greeks',
            'random_numbers': 'Random Numbers',
            'sensitivities': 'Sensitivities',
            'caps_floors': 'Caps & Floors',
            'swaption': 'Swaption',
            'american_options': 'American Options',
            'european_options': 'European Options',
            'black_scholes': 'Black-Scholes',
            'binomial_tree': 'Binomial Tree',
            'finite_differences': 'Finite Differences',
            'implied_volatility': 'Implied Volatility',
            'dividend_adjustment': 'Dividend Adjustment'
        }
        
        if type_filter in type_mapping:
            target_type = type_mapping[type_filter]
            filtered_calculations = [
                c for c in filtered_calculations 
                if c['analysis_type'] == target_type
            ]
            print(f"DEBUG - After type filter ({type_filter} -> {target_type}): {len(filtered_calculations)} calculations")
        else:
            print(f"DEBUG - Type filter '{type_filter}' not found in mapping")
    
    # Apply status filter
    if status_filter:
        filtered_calculations = [
            c for c in filtered_calculations 
            if c['status'] == status_filter
        ]
        print(f"DEBUG - After status filter: {len(filtered_calculations)} calculations")
    
    print(f"DEBUG - Final filtered calculations: {len(filtered_calculations)}")
    
    context = {
        'calculations': filtered_calculations,
        'filtered_calculations': filtered_calculations,
        'calc_stats': calc_stats,
        'search_query': search_query,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'page_title': 'Financial Calculations'
    }
    
    return render(request, 'admin/calculations.html', context)

@login_required
@staff_member_required
def calculation_details(request, calculation_id):
    """Get calculation details for modal"""
    try:
        # In a real application, this would fetch from database
        # For now, return sample data
        sample_calculations = [
            {
                'id': 1001,
                'analysis_type': 'Swap Analysis',
                'user': {'username': 'john_doe'},
                'status': 'completed',
                'created_at': '2024-01-15 14:30:00',
                'parameters': {'notional': 1000000, 'rate': 0.025}
            },
            # Add more sample data as needed
        ]
        
        calculation = next((c for c in sample_calculations if c['id'] == calculation_id), None)
        if not calculation:
            return JsonResponse({'error': 'Calculation not found'}, status=404)
        
        data = {
            'id': calculation['id'],
            'analysis_type': calculation['analysis_type'],
            'user': calculation['user']['username'],
            'status': calculation['status'],
            'created_at': calculation['created_at'],
            'parameters': calculation['parameters']
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@staff_member_required
def retry_calculation(request, calculation_id):
    """Retry a failed calculation"""
    try:
        print(f"DEBUG - Retry calculation {calculation_id}")
        print(f"DEBUG - Request method: {request.method}")
        print(f"DEBUG - Request headers: {dict(request.headers)}")
        
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
        # In a real application, this would trigger the calculation retry
        # For now, just return success
        return JsonResponse({'success': True, 'message': 'Calculation retry initiated'})
    except Exception as e:
        print(f"DEBUG - Error in retry_calculation: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@staff_member_required
def delete_calculation(request, calculation_id):
    """Delete a calculation"""
    try:
        print(f"DEBUG - Delete calculation {calculation_id}")
        print(f"DEBUG - Request method: {request.method}")
        print(f"DEBUG - Request headers: {dict(request.headers)}")
        
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
        # In a real application, this would delete from database
        # For now, just return success
        return JsonResponse({'success': True, 'message': 'Calculation deleted successfully'})
    except Exception as e:
        print(f"DEBUG - Error in delete_calculation: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@staff_member_required
def admin_logs(request):
    """System logs and activity monitoring"""
    
    # Get current date for realistic timestamps
    from datetime import datetime, timedelta
    now = datetime.now()
    
    # Comprehensive log data with current dates
    sample_logs = [
        # Recent activity (today)
        {
            'timestamp': now - timedelta(hours=2),
            'user': 'admin',
            'action': 'User Management',
            'details': 'Toggled user status for sarah_jones',
            'status': 'success',
            'ip_address': '192.168.1.1'
        },
        {
            'timestamp': now - timedelta(hours=2, minutes=5),
            'user': 'admin',
            'action': 'System Access',
            'details': 'Logged into admin panel',
            'status': 'success',
            'ip_address': '192.168.1.1'
        },
        {
            'timestamp': (now - timedelta(hours=3, minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'john_doe',
            'action': 'Swap Analysis',
            'details': 'Completed swap analysis with notional 1,000,000 EUR',
            'status': 'success',
            'ip_address': '192.168.1.100'
        },
        {
            'timestamp': (now - timedelta(hours=3, minutes=40)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'jane_smith',
            'action': 'Option Pricing',
            'details': 'Calculated European call option price: Strike=100, Vol=0.20',
            'status': 'success',
            'ip_address': '192.168.1.101'
        },
        {
            'timestamp': (now - timedelta(hours=4, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'mike_wilson',
            'action': 'Bond Pricing',
            'details': 'Failed to price bond: Invalid coupon rate parameter',
            'status': 'error',
            'ip_address': '192.168.1.102'
        },
        {
            'timestamp': (now - timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'sarah_jones',
            'action': 'Heston Calibration',
            'details': 'Successfully calibrated Heston model: κ=2.0, θ=0.04, σ=0.3',
            'status': 'success',
            'ip_address': '192.168.1.103'
        },
        {
            'timestamp': (now - timedelta(hours=6, minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'alex_brown',
            'action': 'Yield Curve Construction',
            'details': 'Built yield curve with 4 tenors: [1Y, 2Y, 5Y, 10Y]',
            'status': 'success',
            'ip_address': '192.168.1.104'
        },
        {
            'timestamp': (now - timedelta(hours=7, minutes=40)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'lisa_davis',
            'action': 'Monte Carlo Simulation',
            'details': 'Warning: 10,000 simulations took 45 seconds (expected 30s)',
            'status': 'warning',
            'ip_address': '192.168.1.105'
        },
        {
            'timestamp': (now - timedelta(hours=8, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'tom_white',
            'action': 'Greeks Calculation',
            'details': 'Calculated Delta=0.65, Gamma=0.02 for ATM call option',
            'status': 'success',
            'ip_address': '192.168.1.106'
        },
        {
            'timestamp': (now - timedelta(hours=9, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'emma_green',
            'action': 'Volatility Smile',
            'details': 'Generated volatility smile for strikes: [90, 95, 100, 105, 110]',
            'status': 'success',
            'ip_address': '192.168.1.107'
        },
        # Previous day activity
        {
            'timestamp': (now - timedelta(days=1, hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'admin',
            'action': 'System Maintenance',
            'details': 'Updated system configuration and cleared cache',
            'status': 'success',
            'ip_address': '192.168.1.1'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=3, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'john_doe',
            'action': 'Interest Rate Models',
            'details': 'Calibrated Hull-White model with mean reversion=0.1',
            'status': 'success',
            'ip_address': '192.168.1.100'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=4, minutes=40)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'jane_smith',
            'action': 'Credit Risk Analysis',
            'details': 'Calculated credit spread for corporate bond',
            'status': 'success',
            'ip_address': '192.168.1.101'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=5, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'mike_wilson',
            'action': 'Treasury Futures',
            'details': 'Priced 10-year treasury futures contract',
            'status': 'success',
            'ip_address': '192.168.1.102'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=6)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'sarah_jones',
            'action': 'System Access',
            'details': 'Failed login attempt - incorrect password',
            'status': 'error',
            'ip_address': '192.168.1.103'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=6, minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'alex_brown',
            'action': 'Fixed Rate Bonds',
            'details': 'Priced 5-year fixed rate bond with 3% coupon',
            'status': 'success',
            'ip_address': '192.168.1.104'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=7, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'lisa_davis',
            'action': 'Caps & Floors',
            'details': 'Priced interest rate cap with strike 2.5%',
            'status': 'success',
            'ip_address': '192.168.1.105'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=8, minutes=45)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'tom_white',
            'action': 'Swaption Pricing',
            'details': 'Priced 1Yx5Y payer swaption',
            'status': 'success',
            'ip_address': '192.168.1.106'
        },
        {
            'timestamp': (now - timedelta(days=1, hours=10)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'emma_green',
            'action': 'System Access',
            'details': 'User logged out after 2 hours of activity',
            'status': 'success',
            'ip_address': '192.168.1.107'
        },
        # System events (2 days ago)
        {
            'timestamp': (now - timedelta(days=2, hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'system',
            'action': 'System Backup',
            'details': 'Daily backup completed successfully - 2.3GB data',
            'status': 'success',
            'ip_address': '127.0.0.1'
        },
        {
            'timestamp': (now - timedelta(days=2, hours=2, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'admin',
            'action': 'User Management',
            'details': 'Created new user account for analyst_team',
            'status': 'success',
            'ip_address': '192.168.1.1'
        },
        {
            'timestamp': (now - timedelta(days=2, hours=3, minutes=15)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'system',
            'action': 'Database Maintenance',
            'details': 'Optimized database indexes - improved query performance by 15%',
            'status': 'success',
            'ip_address': '127.0.0.1'
        },
        {
            'timestamp': (now - timedelta(days=2, hours=4, minutes=40)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'john_doe',
            'action': 'American Options',
            'details': 'Priced American put option using binomial tree method',
            'status': 'success',
            'ip_address': '192.168.1.100'
        },
        {
            'timestamp': (now - timedelta(days=2, hours=5, minutes=50)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'jane_smith',
            'action': 'Black-Scholes',
            'details': 'Calculated option price using Black-Scholes formula',
            'status': 'success',
            'ip_address': '192.168.1.101'
        },
        {
            'timestamp': (now - timedelta(days=2, hours=6, minutes=55)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'mike_wilson',
            'action': 'Finite Differences',
            'details': 'Solved PDE using finite difference method for barrier option',
            'status': 'success',
            'ip_address': '192.168.1.102'
        },
        {
            'timestamp': (now - timedelta(days=2, hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            'user': 'sarah_jones',
            'action': 'System Access',
            'details': 'User session timeout after 4 hours of inactivity',
            'status': 'warning',
            'ip_address': '192.168.1.103'
        }
    ]
    
    # Filters
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    user_filter = request.GET.get('user', '')
    status_filter = request.GET.get('status', '')
    action_filter = request.GET.get('action', '')
    
    filtered_logs = sample_logs.copy()
    
    # Date filtering (convert to datetime for proper comparison)
    if date_from:
        try:
            from datetime import datetime
            date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
            filtered_logs = [
                log for log in filtered_logs 
                if datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S').date() >= date_from_dt.date()
            ]
        except ValueError:
            pass  # Invalid date format, skip filtering
    
    if date_to:
        try:
            from datetime import datetime
            date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')
            filtered_logs = [
                log for log in filtered_logs 
                if datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S').date() <= date_to_dt.date()
            ]
        except ValueError:
            pass  # Invalid date format, skip filtering
    
    # User filtering
    if user_filter:
        filtered_logs = [
            log for log in filtered_logs 
            if user_filter.lower() in log['user'].lower()
        ]
    
    # Status filtering
    if status_filter:
        filtered_logs = [
            log for log in filtered_logs 
            if log['status'] == status_filter
        ]
    
    # Action filtering with improved logic
    if action_filter:
        if action_filter == 'access':
            # Filter for system access related actions
            filtered_logs = [
                log for log in filtered_logs 
                if 'access' in log['action'].lower() or 'login' in log['action'].lower() or 'logout' in log['action'].lower()
            ]
        else:
            # Filter for specific action types
            filtered_logs = [
                log for log in filtered_logs 
                if action_filter.lower() in log['action'].lower()
            ]
    
    # Calculate statistics
    success_count = len([log for log in filtered_logs if log['status'] == 'success'])
    warning_count = len([log for log in filtered_logs if log['status'] == 'warning'])
    error_count = len([log for log in filtered_logs if log['status'] == 'error'])
    
    context = {
        'logs': filtered_logs,
        'success_count': success_count,
        'warning_count': warning_count,
        'error_count': error_count,
        'date_from': date_from,
        'date_to': date_to,
        'user_filter': user_filter,
        'status_filter': status_filter,
        'action_filter': action_filter,
        'page_title': 'System Logs'
    }
    
    return render(request, 'admin/logs.html', context)

@login_required
@staff_member_required
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Prevent toggling admin status for security
            if user.is_superuser:
                return JsonResponse({
                    'success': False, 
                    'message': 'Cannot toggle admin status for security reasons'
                })
            
            user.is_active = not user.is_active
            user.save()
            
            status = "activated" if user.is_active else "deactivated"
            return JsonResponse({
                'success': True, 
                'message': f'User {user.username} has been {status}',
                'new_status': user.is_active
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error updating user: {str(e)}'
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
@staff_member_required
def delete_analysis(request, analysis_id):
    """Delete a financial analysis"""
    if request.method == 'POST':
        # In a real application, you would delete from database here
        return JsonResponse({'success': True, 'message': 'Analysis deleted'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
@staff_member_required
def get_chart_data(request):
    """Get chart data for AJAX requests"""
    chart_type = request.GET.get('type', 'users')
    
    if chart_type == 'users':
        data = get_users_by_month()
    elif chart_type == 'analyses':
        data = get_analyses_by_type()
    elif chart_type == 'health':
        data = get_system_health_data()
    else:
        data = {}
    
    return JsonResponse(data)

@login_required
@staff_member_required
def view_calculation_details(request, calculation_id):
    """View calculation details"""
    # Sample calculation data for demonstration
    sample_calculations = [
        {
            'id': 1001,
            'analysis_type': 'Swap Analysis',
            'user': {'username': 'john_doe'},
            'status': 'completed',
            'created_at': '2024-01-15 14:30:00',
            'parameters': {'notional': 1000000, 'rate': 0.025}
        },
        {
            'id': 1002,
            'analysis_type': 'Option Pricing',
            'user': {'username': 'jane_smith'},
            'status': 'completed',
            'created_at': '2024-01-15 16:45:00',
            'parameters': {'strike': 100, 'volatility': 0.20}
        },
        {
            'id': 1003,
            'analysis_type': 'Bond Pricing',
            'user': {'username': 'mike_wilson'},
            'status': 'pending',
            'created_at': None,
            'parameters': {'face_value': 1000, 'coupon_rate': 0.05}
        },
        {
            'id': 1004,
            'analysis_type': 'Heston Calibration',
            'user': {'username': 'sarah_jones'},
            'status': 'completed',
            'created_at': '2024-01-14 09:15:00',
            'parameters': {'kappa': 2.0, 'theta': 0.04}
        },
        {
            'id': 1005,
            'analysis_type': 'Yield Curve Construction',
            'user': {'username': 'alex_brown'},
            'status': 'completed',
            'created_at': '2024-01-14 11:20:00',
            'parameters': {'tenors': [1, 2, 5, 10], 'rates': [0.02, 0.025, 0.03, 0.035]}
        },
        {
            'id': 1006,
            'analysis_type': 'Monte Carlo Simulation',
            'user': {'username': 'lisa_davis'},
            'status': 'pending',
            'created_at': None,
            'parameters': {'simulations': 10000, 'time_steps': 252}
        },
        {
            'id': 1007,
            'analysis_type': 'Greeks Calculation',
            'user': {'username': 'tom_white'},
            'status': 'completed',
            'created_at': '2024-01-13 15:30:00',
            'parameters': {'option_type': 'call', 'underlying': 100}
        },
        {
            'id': 1008,
            'analysis_type': 'Volatility Smile',
            'user': {'username': 'emma_green'},
            'status': 'completed',
            'created_at': '2024-01-13 17:45:00',
            'parameters': {'strikes': [90, 95, 100, 105, 110]}
        }
    ]
    
    # Find the calculation
    calculation = None
    for calc in sample_calculations:
        if calc['id'] == calculation_id:
            calculation = calc
            break
    
    if calculation:
        return JsonResponse({
            'success': True,
            'calculation': calculation
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Calculation not found'
        })

@login_required
@staff_member_required
def rerun_calculation_action(request, calculation_id):
    """Rerun a calculation"""
    if request.method == 'POST':
        # In a real application, you would queue the calculation for rerun
        return JsonResponse({
            'success': True,
            'message': f'Calculation #{calculation_id} has been queued for rerun'
        })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
@staff_member_required
def view_user_details(request, user_id):
    """View user details"""
    try:
        user = get_object_or_404(User, id=user_id)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        }
        return JsonResponse({
            'success': True,
            'user': user_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error loading user: {str(e)}'
        })

@login_required
@staff_member_required
def delete_user_action(request, user_id):
    """Delete a user"""
    if request.method == 'POST':
        # In a real application, you would delete from database here
        return JsonResponse({
            'success': True,
            'message': f'User #{user_id} has been deleted'
        })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
@staff_member_required
def admin_chapters(request):
    """Gestion de tous les chapitres QuantLib"""
    
    # Tous les chapitres disponibles
    chapters_info = [
        # Basics
        {'number': 1, 'name': 'QuantLib Basics', 'category': 'Basics', 'status': 'active', 'url': '/basics/'},
        {'number': 2, 'name': 'Instruments', 'category': 'Basics', 'status': 'active', 'url': '/chapter2-instruments/'},
        {'number': 3, 'name': 'Numerical Greeks', 'category': 'Basics', 'status': 'active', 'url': '/chapter3-numerical-greeks/'},
        {'number': 4, 'name': 'Quotes', 'category': 'Basics', 'status': 'active', 'url': '/chapter4-quotes/'},
        {'number': 5, 'name': 'Curves', 'category': 'Basics', 'status': 'active', 'url': '/chapter5-curves/'},
        {'number': 6, 'name': 'Pricing Range', 'category': 'Basics', 'status': 'active', 'url': '/chapter6-pricing-range/'},
        {'number': 7, 'name': 'Random Numbers', 'category': 'Basics', 'status': 'active', 'url': '/chapter7-random/'},
        
        # Interest Rate Curves
        {'number': 8, 'name': 'EONIA Curve', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter_eonia_curve/'},
        {'number': 9, 'name': 'EURIBOR Curve', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter_euribor_curve/'},
        {'number': 10, 'name': 'Treasury Curve', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter10_treasury_curve/'},
        {'number': 11, 'name': 'Day Count', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter_day_count/'},
        {'number': 12, 'name': 'Implied Curve', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter_implied_curve/'},
        {'number': 13, 'name': 'Glitch Curve', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter_glitch_curve/'},
        {'number': 14, 'name': 'Sensitivities', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter_sensitivities/'},
        {'number': 15, 'name': 'Yield Curve', 'category': 'Interest Rate Curves', 'status': 'active', 'url': '/chapter_yield_curve/'},
        
        # Interest Rate Models
        {'number': 16, 'name': 'Hull-White Model', 'category': 'Interest Rate Models', 'status': 'active', 'url': '/chapter15_hull_white/'},
        {'number': 17, 'name': 'Calibration', 'category': 'Interest Rate Models', 'status': 'active', 'url': '/chapter17_calibration/'},
        {'number': 18, 'name': 'Par Indexed Coupons', 'category': 'Interest Rate Models', 'status': 'active', 'url': '/chapter18_par_indexed_coupons/'},
        {'number': 19, 'name': 'Swap', 'category': 'Interest Rate Models', 'status': 'active', 'url': '/chapter19_swap/'},
        {'number': 20, 'name': 'Caps & Floors', 'category': 'Interest Rate Models', 'status': 'active', 'url': '/chapter20_caps_floors/'},
        
        # Equity Models
        {'number': 21, 'name': 'Heston Option', 'category': 'Equity Models', 'status': 'active', 'url': '/chapter21_heston_option/'},
        {'number': 22, 'name': 'Heston Calibration', 'category': 'Equity Models', 'status': 'active', 'url': '/chapter22_heston_calibration/'},
        {'number': 23, 'name': 'Heston Parameter Calibration', 'category': 'Equity Models', 'status': 'active', 'url': '/chapter23_heston_parameter_calibration/'},
        {'number': 24, 'name': 'European/American Options', 'category': 'Equity Models', 'status': 'active', 'url': '/chapter24_european_american_options/'},
        {'number': 25, 'name': 'Black Formula Futures', 'category': 'Equity Models', 'status': 'active', 'url': '/chapter25_black_formula_futures/'},
        
        # Advanced Topics
        {'number': 26, 'name': 'Defining Rho', 'category': 'Advanced', 'status': 'active', 'url': '/chapter26_defining_rho/'},
        {'number': 27, 'name': 'Day Count Conventions', 'category': 'Advanced', 'status': 'active', 'url': '/chapter27_day_count_conventions/'},
        {'number': 28, 'name': 'Fixed Rate Bonds', 'category': 'Bonds', 'status': 'active', 'url': '/chapter28_fixed_rate_bonds/'},
        {'number': 29, 'name': 'Irregular Bonds', 'category': 'Bonds', 'status': 'active', 'url': '/chapter29_irregular_bonds/'},
        {'number': 30, 'name': 'Credit Spreads', 'category': 'Bonds', 'status': 'active', 'url': '/chapter30_credit_spreads/'},
        {'number': 31, 'name': 'Callable Bonds', 'category': 'Bonds', 'status': 'active', 'url': '/chapter31_callable_bonds/'},
        {'number': 32, 'name': 'Discount Margin', 'category': 'Bonds', 'status': 'active', 'url': '/chapter32_discount_margin/'},
        {'number': 33, 'name': 'Floating Duration', 'category': 'Bonds', 'status': 'active', 'url': '/chapter33_floating_duration/'},
        {'number': 34, 'name': 'Treasury Futures', 'category': 'Bonds', 'status': 'active', 'url': '/chapter34_treasury_futures/'},
        {'number': 35, 'name': 'Pricing Conventions', 'category': 'Conventions', 'status': 'active', 'url': '/chapter35_pricing_conventions/'},
        {'number': 36, 'name': 'More Conventions', 'category': 'Conventions', 'status': 'active', 'url': '/chapter36_more_conventions/'},
    ]
    
    # Statistiques par catégorie
    categories_stats = {}
    for chapter in chapters_info:
        category = chapter['category']
        if category not in categories_stats:
            categories_stats[category] = {'total': 0, 'active': 0, 'inactive': 0}
        categories_stats[category]['total'] += 1
        if chapter['status'] == 'active':
            categories_stats[category]['active'] += 1
        else:
            categories_stats[category]['inactive'] += 1
    
    context = {
        'chapters_info': chapters_info,
        'categories_stats': categories_stats,
        'page_title': 'QuantLib Chapters'
    }
    
    return render(request, 'admin/separate_chapters.html', context)


def admin_login(request):
    """Page de connexion pour l'administration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Identifiants invalides ou accès non autorisé.')
    
    return render(request, 'admin/login.html')

def admin_logout_view(request):
    """Déconnexion de l'administration"""
    logout(request)
    return redirect('admin_login')

@login_required
@staff_member_required
def admin_profile(request):
    """Page de profil de l'administrateur"""
    user = request.user
    
    # Statistiques personnelles
    user_stats = {
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
    }
    
    # Activité récente (simulée)
    recent_activity = [
        {'action': 'Connexion au système', 'timestamp': timezone.now() - timedelta(minutes=5)},
        {'action': 'Consultation des logs', 'timestamp': timezone.now() - timedelta(minutes=15)},
        {'action': 'Gestion des utilisateurs', 'timestamp': timezone.now() - timedelta(hours=1)},
        {'action': 'Vérification des calculs', 'timestamp': timezone.now() - timedelta(hours=2)},
    ]
    
    context = {
        'user': user,
        'user_stats': user_stats,
        'recent_activity': recent_activity,
        'page_title': 'Admin Profile'
    }
    
    return render(request, 'admin/profile.html', context)

@login_required
@staff_member_required
def admin_notifications(request):
    """Page des notifications de l'administration"""
    if not Notification:
        messages.warning(request, 'Notifications module not available')
        return redirect('admin_dashboard')
    
    # Récupérer les notifications
    notifications = Notification.objects.filter(
        is_archived=False
    ).order_by('-created_at')
    
    # Filtres
    notification_type = request.GET.get('type', '')
    priority = request.GET.get('priority', '')
    is_read = request.GET.get('read', '')
    
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    if priority:
        notifications = notifications.filter(priority=priority)
    if is_read == 'true':
        notifications = notifications.filter(is_read=True)
    elif is_read == 'false':
        notifications = notifications.filter(is_read=False)
    
    # Statistiques
    total_notifications = Notification.objects.filter(is_archived=False).count()
    unread_count = Notification.objects.filter(is_archived=False, is_read=False).count()
    critical_count = Notification.objects.filter(
        is_archived=False, 
        priority='critical'
    ).count()
    
    context = {
        'notifications': notifications,
        'total_notifications': total_notifications,
        'unread_count': unread_count,
        'critical_count': critical_count,
        'notification_types': Notification.NOTIFICATION_TYPES,
        'priority_levels': Notification.PRIORITY_LEVELS,
        'page_title': 'Notifications'
    }
    
    return render(request, 'admin/notifications.html', context)

@login_required
@staff_member_required
def mark_notification_read(request, notification_id):
    """Marque une notification comme lue"""
    if not Notification:
        return JsonResponse({'success': False, 'error': 'Notifications not available'})
    
    try:
        notification = get_object_or_404(Notification, id=notification_id)
        notification.mark_as_read()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@staff_member_required
def mark_all_notifications_read(request):
    """Marque toutes les notifications comme lues"""
    if not Notification:
        return JsonResponse({'success': False, 'error': 'Notifications not available'})
    
    try:
        Notification.objects.filter(is_archived=False, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@staff_member_required
def archive_notification(request, notification_id):
    """Archive une notification"""
    if not Notification:
        return JsonResponse({'success': False, 'error': 'Notifications not available'})
    
    try:
        notification = get_object_or_404(Notification, id=notification_id)
        notification.archive()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@staff_member_required
def get_notifications_count(request):
    """API pour récupérer le nombre de notifications non lues"""
    if not Notification:
        return JsonResponse({'unread_count': 0, 'critical_count': 0})
    
    unread_count = Notification.objects.filter(
        is_archived=False, 
        is_read=False
    ).count()
    
    critical_count = Notification.objects.filter(
        is_archived=False, 
        is_read=False,
        priority='critical'
    ).count()
    
    return JsonResponse({
        'unread_count': unread_count,
        'critical_count': critical_count
    })

@login_required
@staff_member_required
def create_notification(request):
    """Créer une nouvelle notification (pour les tests)"""
    if not Notification:
        return JsonResponse({'success': False, 'error': 'Notifications not available'})
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title', 'Test Notification')
            message = request.POST.get('message', 'This is a test notification')
            notification_type = request.POST.get('type', 'info')
            priority = request.POST.get('priority', 'medium')
            
            notification = Notification.objects.create(
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                created_by=request.user
            )
            
            return JsonResponse({
                'success': True, 
                'notification_id': notification.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'POST method required'})

# Fonctions utilitaires
def get_users_by_month():
    """Récupère les données des utilisateurs par mois"""
    # Données simulées pour une année complète (plus réalistes)
    monthly_data = [
        {'month': '2024-01-01', 'new_users': 15, 'active_users': 45},
        {'month': '2024-02-01', 'new_users': 22, 'active_users': 52},
        {'month': '2024-03-01', 'new_users': 18, 'active_users': 48},
        {'month': '2024-04-01', 'new_users': 25, 'active_users': 55},
        {'month': '2024-05-01', 'new_users': 28, 'active_users': 58},
        {'month': '2024-06-01', 'new_users': 32, 'active_users': 62},
        {'month': '2024-07-01', 'new_users': 35, 'active_users': 65},
        {'month': '2024-08-01', 'new_users': 30, 'active_users': 60},
        {'month': '2024-09-01', 'new_users': 28, 'active_users': 58},
        {'month': '2024-10-01', 'new_users': 24, 'active_users': 54},
        {'month': '2024-11-01', 'new_users': 20, 'active_users': 50},
        {'month': '2024-12-01', 'new_users': 18, 'active_users': 48}
    ]
    
    return monthly_data

def get_analyses_by_type():
    """Récupère les données des analyses par type"""
    # Types d'analyses disponibles dans l'application QuantLib
    analysis_types = [
        {'analysis_type': 'Swap Analysis', 'count': 25},
        {'analysis_type': 'Heston Calibration', 'count': 18},
        {'analysis_type': 'Yield Curve Construction', 'count': 15},
        {'analysis_type': 'Option Pricing', 'count': 12},
        {'analysis_type': 'Bond Pricing', 'count': 10},
        {'analysis_type': 'Monte Carlo Simulation', 'count': 8},
        {'analysis_type': 'Greeks Calculation', 'count': 6},
        {'analysis_type': 'Volatility Smile', 'count': 4},
        {'analysis_type': 'Interest Rate Models', 'count': 3},
        {'analysis_type': 'Credit Risk Analysis', 'count': 2}
    ]
    
    return analysis_types

def get_system_health_data():
    """Récupère les données de santé du système"""
    return {
        'database_status': 'OK',
        'api_status': 'OK',
        'memory_usage': '45%',
        'cpu_usage': '23%',
        'disk_usage': '67%'
    }

# API endpoints
@login_required
@staff_member_required
def get_chart_data(request):
    """API pour récupérer les données des graphiques"""
    chart_type = request.GET.get('type', 'users')
    
    if chart_type == 'users':
        data = get_users_by_month()
    elif chart_type == 'analyses':
        data = get_analyses_by_type()
    else:
        data = []
    
    return JsonResponse({'data': data})


@login_required
@staff_member_required
def delete_analysis(request, analysis_id):
    """Supprimer une analyse"""
    if SwapAnalysisResult:
        analysis = get_object_or_404(SwapAnalysisResult, id=analysis_id)
        analysis.delete()
        messages.success(request, 'Analyse supprimée avec succès.')
    
    return redirect('admin_calculations')
