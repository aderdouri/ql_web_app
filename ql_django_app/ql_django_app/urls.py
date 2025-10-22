from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.http import HttpResponse
from . import views as home_views
from . import separate_admin_views

urlpatterns = [
    # Favicon route to prevent 404 errors
    path('favicon.ico', lambda request: HttpResponse(status=204), name='favicon'),
    path('', home_views.home, name='home'),

    # On ne garde QUE les catégories qui existent et sont configurées
    path('basics/', include('basics.urls')),
    path('chapter2-instruments/', include('chapter2_instruments.urls')),
    path('chapter3-numerical-greeks/', include('chapter3_numerical_greeks.urls')),
    path('chapter4-quotes/', include('chapter4_quotes.urls')),
    path('chapter5-curves/', include('chapter5_curves.urls')),
    path('chapter6-pricing-range/', include('chapter6_pricing_range.urls')),
    path('chapter7-random/', include('chapter7_random.urls')),
    path('interest-rate-curves/', include('interest_rate_curves.urls')),
    path('interest-rate-models/', include('interest_rate_models.urls')),
    path('equity-models/', include('equity_models.urls')),
    path('bonds/', include('bonds.urls')),
    path('chapter17-calibration/', include('chapter17_calibration.urls')),
    path('chapter18-par-indexed-coupons/', include('chapter18_par_indexed_coupons.urls')),
    path('chapter33-floating-duration/', include('chapter33_floating_duration.urls')),
    path('chapter34-treasury-futures/', include('chapter34_treasury_futures.urls')),
    path('chapter35-pricing-conventions/', include('chapter35_pricing_conventions.urls')),
    path('chapter36-more-conventions/', include('chapter36_more_conventions.urls')),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
        path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
        
        # QuantLib Cookbook
        
        # Administration - Redirection directe vers le login
        path('admin/', lambda request: redirect('admin_login')),
        path('admin/dashboard/', separate_admin_views.admin_dashboard, name='admin_dashboard'),
        path('admin/login/', separate_admin_views.admin_login, name='admin_login'),
        path('admin/logout/', separate_admin_views.admin_logout_view, name='admin_logout'),
        path('admin/profile/', separate_admin_views.admin_profile, name='admin_profile'),
        path('admin/notifications/', separate_admin_views.admin_notifications, name='admin_notifications'),
        path('admin/users/', separate_admin_views.admin_users, name='admin_users'),
        path('admin/users/<int:user_id>/details/', separate_admin_views.user_details, name='user_details'),
        path('admin/toggle-user/<int:user_id>/', separate_admin_views.toggle_user_status, name='toggle_user_status'),
        path('admin/delete-user/<int:user_id>/', separate_admin_views.delete_user, name='delete_user'),
        path('admin/calculations/', separate_admin_views.admin_calculations, name='admin_calculations'),
        path('admin/calculations/<int:calculation_id>/details/', separate_admin_views.calculation_details, name='calculation_details'),
        path('admin/calculations/<int:calculation_id>/retry/', separate_admin_views.retry_calculation, name='retry_calculation'),
        path('admin/calculations/<int:calculation_id>/delete/', separate_admin_views.delete_calculation, name='delete_calculation'),
        path('admin/logs/', separate_admin_views.admin_logs, name='admin_logs'),
        path('admin/chapters/', separate_admin_views.admin_chapters, name='admin_chapters'),
        # Redirections pour les anciennes URLs supprimées
        path('admin/models/', lambda request: redirect('admin_dashboard')),
        path('admin/settings/', lambda request: redirect('admin_dashboard')),
        path('admin/toggle-user/<int:user_id>/', separate_admin_views.toggle_user_status, name='admin_toggle_user'),
        path('admin/delete-calculation/<int:analysis_id>/', separate_admin_views.delete_analysis, name='admin_delete_calculation'),
        path('admin/api/chart-data/', separate_admin_views.get_chart_data, name='admin_chart_data'),
        path('admin/api/view-calculation/<int:calculation_id>/', separate_admin_views.view_calculation_details, name='admin_view_calculation'),
        path('admin/api/rerun-calculation/<int:calculation_id>/', separate_admin_views.rerun_calculation_action, name='admin_rerun_calculation'),
        path('admin/api/view-user/<int:user_id>/', separate_admin_views.view_user_details, name='admin_view_user'),
        path('admin/delete-user/<int:user_id>/', separate_admin_views.delete_user_action, name='admin_delete_user'),
        # Notifications API
        path('admin/api/notifications/count/', separate_admin_views.get_notifications_count, name='admin_notifications_count'),
        path('admin/api/notifications/mark-read/<int:notification_id>/', separate_admin_views.mark_notification_read, name='admin_mark_notification_read'),
        path('admin/api/notifications/mark-all-read/', separate_admin_views.mark_all_notifications_read, name='admin_mark_all_notifications_read'),
        path('admin/api/notifications/archive/<int:notification_id>/', separate_admin_views.archive_notification, name='admin_archive_notification'),
        path('admin/api/notifications/create/', separate_admin_views.create_notification, name='admin_create_notification'),
        
        # Redirections des anciennes URLs admin-separate vers admin
        path('admin-separate/', lambda request: redirect('admin_home')),
        path('admin-separate/dashboard/', lambda request: redirect('admin_dashboard')),
        path('admin-separate/login/', lambda request: redirect('admin_login')),
        path('admin-separate/logout/', lambda request: redirect('admin_logout')),
        path('admin-separate/users/', lambda request: redirect('admin_users')),
        path('admin-separate/calculations/', lambda request: redirect('admin_calculations')),
        path('admin-separate/logs/', lambda request: redirect('admin_logs')),
        path('admin-separate/chapters/', lambda request: redirect('admin_chapters')),
]