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

def add_collection_manual(request):
    return render(request, 'views/layouts/pages/add_collection_manual.html')

def add_collection_student(request):
    return render(request, 'views/layouts/pages/add_collection_student.html')

def view_receipts(request):
    return render(request, 'views/layouts/pages/view_receipts.html')

def show_receipt(request):
    return render(request, 'views/layouts/pages/show_receipt.html')

def cleared_students(request):
    return render(request, 'views/layouts/pages/cleared_students.html')

def sis_payments(request):
    return render(request, 'views/layouts/pages/sis_payments.html')

def or_setup(request):
    return render(request, 'views/layouts/pages/or_setup.html')

def accountable_forms_report(request):
    return render(request, 'views/layouts/pages/accountable_forms_report.html')

def certification_report(request):
    return render(request, 'views/layouts/pages/certification_report.html')

def monthly_collection_report(request):
    return render(request, 'views/layouts/pages/monthly_collection_report.html')

def summary_collection_report(request):
    return render(request, 'views/layouts/pages/summary_collection_report.html')

def cash_receipt_record_report(request):
    return render(request, 'views/layouts/pages/cash_receipt_record_report.html')

def deposits_pending(request):
    return render(request, 'views/layouts/pages/deposits_pending.html')


def deposits_deposited(request):
    return render(request, 'views/layouts/pages/deposits_deposited.html')


def admin_dashboard(request):
    return render(request, 'views/layouts/pages/admin_dashboard.html')


def add_user(request):
    return render(request, 'views/layouts/pages/add_user.html')

def edit_user(request):
    return render(request, 'views/layouts/pages/edit_user.html')


def react_deact(request):
    return render(request, 'views/layouts/pages/react_deact.html')


def email(request):
    return render(request, 'views/layouts/pages/email.html')


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

def error_403(request):
    return render(request, 'views/layouts/pages/error_403.html')

def gt_fname(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_FNAME_CMS", (request.session['uname'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def activity_log(request):
    return render(request, 'views/layouts/pages/activity_log.html')

def transaction_log(request):
    return render(request, 'views/layouts/pages/transaction_log.html')
    
def get_income_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_INCOME_TYPE")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)
  
def get_fund_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_FUND_TYPE")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_UACS_data_table(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_UACS_TABLE")
    data = cursor.fetchall()
    return render(request, 'views/layouts/pages/setup_uacs.html', {"response": data})

def reload_UACS_data_table(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_UACS_TABLE")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def change_status_uacs(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_STATUS_UACS", (request.POST['code'], request.POST['new_status']))
    return HttpResponse("")

def update_uacs(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_UACS_TABLE"
                    ,(request.POST['id']
                    ,request.POST['old_code']
                    ,request.POST['new_code']
                    ,request.POST['fnd_type']
                    ,request.POST['inc_type']
                    ,request.POST['desc_name']
                    ))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_uacs_list(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_UACS_TABLE"
                    ,(request.POST['fndtype']
                    ,request.POST['inctype']
                    ,request.POST['o_code']
                    ,request.POST['code']
                    ,request.POST['desc']
                    ))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_uacs_fund_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_UACS_FUND"
                    ,(request.POST['fund_code']
                    ,request.POST['fund_desc']
                    ))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_uacs_inc_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_UACS_INC"
                    ,(request.POST['inc_desc'],))
    return HttpResponse("")

def deact_uacs_inc_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_DEACT_INC_TYPE"
                    ,(request.POST['inctype'],))
    return HttpResponse("")

def deact_uacs_fund_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_DEACT_FUND_TYPE"
                    ,(request.POST['fndtype'],))
    return HttpResponse("")

def get_specific_fund(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SPECIFIC_FUND"
                    ,(request.POST['fndtype'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_specific_income(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SPECIFIC_INCOME"
                    ,(request.POST['inctype'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def update_uacs_fund_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_FUND_TYPE"
                    ,(request.POST['fndtype_orig']
                    ,request.POST['fndtype_upd']
                    ,request.POST['fndcode']))
    return HttpResponse("")

def update_uacs_inc_type(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_INC_TYPE"
                    ,(request.POST['inctype_orig']
                    ,request.POST['inctype_upd']))
    return HttpResponse("")

def load_user_data(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ALL_USERS")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def update_user_data(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_USER_DATA"
                    ,(request.POST['vID']
                    ,request.POST['fname']
                    ,request.POST['mname']
                    ,request.POST['lname']
                    ,request.POST['role']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_user_data2(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ALL_USERS2")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def deactivate_user(request):
    cursor = connection.cursor()
    cursor.callproc("SP_DEACT_USER"
                    ,(request.POST['act_id']
                    ,request.POST['act']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_uacs_code(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ALL_UACS_CODE")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)