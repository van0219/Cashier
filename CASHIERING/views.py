from django.conf import settings
from django.shortcuts import render, redirect, resolve_url
from django.db import IntegrityError, connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# Create your views here.

def login(request):
    return render(request, 'views/layouts/pages/login.html')

def dashboard(request):
    return render(request, 'views/layouts/pages/dashboard.html')

@login_required
def add_collection_manual(request):
    return render(request, 'views/layouts/pages/add_collection_manual.html')

@login_required
def add_collection_student(request):
    return render(request, 'views/layouts/pages/add_collection_student.html')

@login_required
def view_receipts(request):
    return render(request, 'views/layouts/pages/view_receipts.html')

@login_required
def show_receipt(request):
    return render(request, 'views/layouts/pages/show_receipt.html')

@login_required
def cleared_students(request):
    return render(request, 'views/layouts/pages/cleared_students.html')

@login_required
def sis_payments(request):
    return render(request, 'views/layouts/pages/sis_payments.html')

@login_required
def or_setup(request):
    return render(request, 'views/layouts/pages/or_setup.html')

@login_required
def accountable_forms_report(request):
    return render(request, 'views/layouts/pages/accountable_forms_report.html')

@login_required
def certification_report(request):
    return render(request, 'views/layouts/pages/certification_report.html')

@login_required
def monthly_collection_report(request):
    return render(request, 'views/layouts/pages/monthly_collection_report.html')

@login_required
def summary_collection_report(request):
    return render(request, 'views/layouts/pages/summary_collection_report.html')

@login_required
def cash_receipt_record_report(request):
    return render(request, 'views/layouts/pages/cash_receipt_record_report.html')

@login_required
def deposits_pending(request):
    return render(request, 'views/layouts/pages/deposits_pending.html')

@login_required
def deposits_deposited(request):
    return render(request, 'views/layouts/pages/deposits_deposited.html')

@login_required
def admin_dashboard(request):
    return render(request, 'views/layouts/pages/admin_dashboard.html')

@login_required
def add_user(request):
    return render(request, 'views/layouts/pages/add_user.html')

@login_required
def edit_user(request):
    return render(request, 'views/layouts/pages/edit_user.html')

@login_required
def react_deact(request):
    return render(request, 'views/layouts/pages/react_deact.html')

@login_required
def setup_uacs(request):
    return render(request, 'views/layouts/pages/setup_uacs.html')

@login_required
def email(request):
    return render(request, 'views/layouts/pages/email.html')

@login_required
def account(request):
    return render(request, 'views/layouts/pages/account.html')

def add_user_btn_click(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_USER_CMS", (
        request.POST['fname'],
        request.POST['mname'],
        request.POST['lname'],
        request.POST['uname'],
        request.POST['psword'],
        request.POST['roleid'],
    ))
    return HttpResponse("")

def check_username(request):
    cursor = connection.cursor()
    cursor.callproc("SP_CHECK_UNAME_CMS", (request.POST['uname'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def check_credentials(request):
    cursor = connection.cursor()
    cursor.callproc("SP_CHECK_CREDENTIALS", (request.POST['uname'], request.POST['pword'],))
    data = cursor.fetchall()
    if data:
        uname = ''
        role = ''
        for row in data:
            uname = row[0]
            role = row[1]
        request.session['uname'] = uname
        request.session['role'] = role
    return JsonResponse(data, safe=False)

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'uname' in request.session:
        del request.session['uname']
    return render(request, 'views/layouts/pages/login.html')

def get_session(request):
    role = request.session.get('role')
    return JsonResponse(role, safe=False)

@login_required
def error_403(request):
    return render(request, 'views/layouts/pages/error_403.html')

def gt_fname(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_FNAME_CMS", (request.session['uname'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)