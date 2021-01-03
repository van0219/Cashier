"""CASHIER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from CASHIERING import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_collection_manual', views.add_collection_manual, name='add_collection_manual'),
    path('add_collection_student', views.add_collection_student, name='add_collection_student'),
    path('view_receipts', views.view_receipts, name='view_receipts'),
    path('show_receipt', views.show_receipt, name='show_receipt'),
    path('cleared_students', views.cleared_students, name='cleared_students'),
    path('sis_payments', views.sis_payments, name='sis_payments'),
    path('or_setup', views.or_setup, name='or_setup'),
    path('accountable_forms_report', views.accountable_forms_report, name='accountable_forms_report'),
    path('certification_report', views.certification_report, name='certification_report'),
    path('monthly_collection_report', views.monthly_collection_report, name='monthly_collection_report'),
    path('summary_collection_report', views.summary_collection_report, name='summary_collection_report'),
    path('cash_receipt_record_report', views.cash_receipt_record_report, name='cash_receipt_record_report'),
    path('deposits_pending', views.deposits_pending, name='deposits_pending'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('add_user', views.add_user, name='add_user'),
    path('edit_user', views.edit_user, name='edit_user'),
    path('react_deact', views.react_deact, name='react_deact'),
    path('email', views.email, name="email"),
    path('account', views.account, name="account"),
    path('add_user_btn_click', views.add_user_btn_click, name="add_user_btn_click"),
    path('check_username', views.check_username, name="check_username"),
    path('check_credentials', views.check_credentials, name="check_credentials"),
    path('', views.logout, name="logout"),
    path('get_session', views.get_session, name="get_session"),
    path('error_403', views.error_403, name="error_403"),
    path('gt_fname', views.gt_fname, name="gt_fname"),
    path('activity_log', views.activity_log, name="activity_log"),
    path('transaction_log', views.transaction_log, name="transaction_log"),
    path('get_income_type', views.get_income_type, name="get_income_type"),
    path('get_fund_type', views.get_fund_type, name="get_fund_type"),
    path('get_UACS_data_table', views.get_UACS_data_table, name="get_UACS_data_table"),
    path('change_status_uacs', views.change_status_uacs, name="change_status_uacs"),
    path('update_uacs', views.update_uacs, name="update_uacs"),
    path('add_uacs_list', views.add_uacs_list, name="add_uacs_list"),
    path('add_uacs_fund_type', views.add_uacs_fund_type, name="add_uacs_fund_type"),
    path('add_uacs_inc_type', views.add_uacs_inc_type, name="add_uacs_inc_type"),                                          
]
