from __future__ import with_statement
from django.conf import settings
from django.shortcuts import render, redirect, resolve_url
from django.db import IntegrityError, connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from fpdf import *
import re
from datetime import datetime
# from pyzbar import pyzbar
# import qrcode
import string

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

def view_sis_payments(request):
    return render(request, 'views/layouts/pages/view_sis_payments.html')

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


def change_pass(request):
    return render(request, 'views/layouts/pages/change_pass.html')

def change_pass_admin(request):
    return render(request, 'views/layouts/pages/change_pass_admin.html')

def sis_payments(request):
    return render(request, 'views/layouts/pages/sis_payments.html')

def add_stud(request):
    return render(request, 'views/layouts/pages/add_stud.html')

def add_educ_level(request):
    return render(request, 'views/layouts/pages/add_educ_level.html')

def add_course(request):
    return render(request, 'views/layouts/pages/add_course.html')

def add_user_btn_click(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_USER_CMS", (
        request.POST['fname'],
        request.POST['mname'],
        request.POST['lname'],
        request.POST['uname'],
        request.POST['receiver'],
        request.POST['psword'],
        request.POST['roleid'],
        request.POST['img_filename']
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
        img = ''
        for row in data:
            uname = row[0]
            role = row[1]
            img = row[2]
        request.session['uname'] = uname
        request.session['role'] = role
        request.session['img'] = img
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

def gt_profile_img(request):
    data = request.session['img']
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
    cursor.callproc("SP_SELECT_ALL_UACS_CODE"
                    ,(request.POST['incomeType'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_uacs_code_sis(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SIS_UACS_CODE")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_or_set(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_OR_SET"
                    ,(request.POST['startVal']
                    ,request.POST['endVal']))
    return HttpResponse("")

def get_current_or(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_CURRENT_OR")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_ending_or(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ENDING_OR")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_last_upd(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_LAST_UPD")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_student_name(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_STUDENT_NAME"
                    ,(request.POST['studno'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def insert_collection(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_COLLECTION"
                    ,(request.POST['or_num']
                    ,request.POST['assessed']
                    ,request.POST['collected']
                    ,request.POST['studno']
                    ,request.POST['client']
                    ,request.POST['educ_level']
                    ,request.POST['userID']
                    ,request.POST['is_direct']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_receipt_table(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ALL_RECEIPTS")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def insert_collection_breakdown(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_COLLECTION_BREAKDOWN"
                    ,(request.POST['or_num']
                    ,request.POST['desc']
                    ,request.POST['nature']
                    ,request.POST['amt']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_specific_collection(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SPECIFIC_COLLECTION"
                    ,(request.POST['or_num'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_specific_collection_breakdown(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SPECIFIC_COLLECTION_BREAKDOWN"
                    ,(request.POST['or_num'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_receipts_donut(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_RECEIPT_DONUT")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_sis_payments(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SIS_PAYMENTS_DONE")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_sis_payments2(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SIS_PAYMENTS_PENDING")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_specific_sis_done(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SPECIFIC_SIS_DONE"
                    ,(request.POST['or_num'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_specific_sis_client(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SPECIFIC_SIS_CLIENT"
                    ,(request.POST['or_num'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_sis_bar_chart(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SIS_BAR_CHART"
                    ,(request.POST['filt'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_collection_history(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_COLLECTION_LOG"
                    ,(request.POST['date_start']
                    ,request.POST['date_end']
                    ,request.POST['code']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_collection_history2(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_COLLECTION_PENDING"
                    ,(request.POST['date_start']
                    ,request.POST['date_end']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def deposits_pending(request):
    return render(request, 'views/layouts/pages/deposits_pending.html')

def deposits_deposited(request):
    return render(request, 'views/layouts/pages/deposits_deposited.html')

def save_for_remittance(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SAVE_FOR_REMITTANCE"
                    ,(request.POST['or_num'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def insert_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_DEPOSIT"
                    ,(request.POST['or_num']
                    ,request.POST['group_id']
                    ,request.POST['status']
                    ,request.POST['date_dep']
                    ,request.POST['user_id']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False) 

def load_scheduled_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SCHEDULED_DEPOSITS")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_current_group_id(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_CURRENT_GROUP_ID")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def remove_sched_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_REMOVE_SCHED_DEPOSIT"
                    ,(request.POST['group_id'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def resched_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_SCHED_DATE"
                    ,(request.POST['new_date']
                    ,request.POST['group_id']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_deposited(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_DEPOSITED")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def done_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_DONE_DEPOSIT"
                    ,(request.POST['group_id'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_acct_forms_dash(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ACCOUNTABLE_FORMS_REPORT"
                    ,(request.POST['start']
                    ,request.POST['end']
                    ,'CARD'))
    data = cursor.fetchall()
    import csv
    csv_rowlist = data
    with open(r'CASHIERING\views\layouts\textfiles\acc_obj.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(csv_rowlist)
    return JsonResponse(data, safe=False)

def load_or_monthly_report(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_OR_MONTHLY_REPORT"
                   ,(request.POST['start']
                   ,request.POST['end']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_cert_table(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_CERT_TABLE"
                    ,(request.POST['start']
                    ,request.POST['end']))
    data = cursor.fetchall()
    import csv
    csv_rowlist = data
    with open(r'CASHIERING\views\layouts\textfiles\cert_obj.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(csv_rowlist)
    return JsonResponse(data, safe=False)

def load_monthly_collection_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MONTHLY_COLLECTION"
                   ,(request.POST['year'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_monthly_collection_deposit2(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MONTHLY_DEPOSIT"
                   ,(request.POST['year'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_radar_chart(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_RADAR_CHART"
                    ,(request.POST['month']
                    ,request.POST['year']))
    data = cursor.fetchall()
    import csv
    csv_rowlist = data
    with open(r'CASHIERING\views\layouts\textfiles\sum_obj.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(csv_rowlist)
    return JsonResponse(data, safe=False)

def load_cash_receipt_cards(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_CASH_RECEIPT_CARDS"
                    ,(request.POST['month']
                    ,request.POST['year']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_dashboard_cards(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_DASHBOARD_CARDS"
                   ,(request.POST['year'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_dashboard_bar_graph(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MONTHLY_COLLECTION"
                   ,(request.POST['year'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_dashboard_line_graph(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MONTHLY_DEPOSIT")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_admin_dashboard_cards(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_ADMIN_DASHBOARD_CARDS")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_email_credentials():
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_EMAIL_CREDENTIALS")
    data = cursor.fetchall()
    return data

def send_password(request):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.application import MIMEApplication

    cred = get_email_credentials()
    # setup credentials
    sender = cred[0][0]
    password = cred[0][1]

    receiver = request.POST['receiver']
    
    # header
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Login Credentials'
    msg['From'] = 'PUPQC Cashiering Admin'
    msg['To'] = request.POST['fullname']
    # end header

    # message
    message1 = 'You can now login to your Cashiering account.<br>We recommend that you change your password after logging in.<br>Thank you!<br>'
    message2 = '<br>Username: ' + request.POST['uname'] + '<br>Password: ' + request.POST['pass']
    # body
    msgText = MIMEText('<b>%s</b>' % (message1 + '<br>' + message2), 'html')
    msg.attach(msgText)
    # if with image attachment
    imgFile = "CASHIERING/static/assets/img/logo/PUPLogo.png"
    imgRename = " "
    with open(imgFile, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename= imgRename)
    msg.attach(img)
    # end body

    # send message
    try:
        # server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587) # Outlook SMTP
        server = smtplib.SMTP('smtp.gmail.com:587') # Gmail SMTP
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except:
        pass
    return JsonResponse('email sent', safe=False)

def set_email(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SET_CASHIER_EMAIL"
                    ,(request.POST['email']
                    ,request.POST['pass']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_sumcol_cards(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SUMCOL_CARDS"
                    ,(request.POST['month']
                    ,request.POST['year']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_nature_col(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_NATURE_COL"
                    ,(request.POST['uacs'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_new_nature(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_NEW_NATURE"
                    ,(request.POST['uacs']
                    ,request.POST['nature'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def remove_nature(request):
    cursor = connection.cursor()
    cursor.callproc("SP_REMOVE_NATURE"
                    ,(request.POST['name'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def update_nature(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_NATURE"
                    ,(request.POST['old_name']
                    ,request.POST['new_name']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_coldep_card(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_COLDEP_CARD"
                    ,(request.POST['month']
                    ,request.POST['year']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_coldep_group(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_COLLECTION_GROUP"
                    ,(request.POST['month']
                    ,request.POST['year']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_top_contrib(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_TOP_CONTRIB"
                    ,(request.POST['month']
                    ,request.POST['year']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

# def createQr(report_id):
#     # data to encode
#     data = report_id
#     # instantiate QRCode object
#     qr = qrcode.QRCode(version=3, box_size=10, border=4)
#     # add data to the QR code
#     qr.add_data(data)
#     # compile the data into a QR code array
#     qr.make()
#     # transfer the array into an actual image
#     img = qr.make_image(fill_color="black", back_color="white") #binaligtad ko kasi d mabasa ng scanner
#     file_loc = "CASHIERING/static/assets/img/QR-code/" + data + '.png'
#     # save it to a file 
#     img.save(file_loc)
#     ret = []
#     ret.append(file_loc[10:])
#     ret.append(data)
#     return data

def load_cert_pdf(request):
    total = "{0:,.2f}".format(float(request.POST['total_dep']))
    is_loadCertPDF1 = int(request.POST['is_loadCertPDF1'])
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    # month_l_day = calendar.monthrange(year,month)[1]  # this is to get the last day of the month
    if is_loadCertPDF1 == 1:
        month_f_day = request.POST['start_day']
        month_l_day = request.POST['end_day']
        report_id = 'CR-' + str(month) + '-' + str(month_f_day) + '-' + str(month_l_day) + '-' + str(year) 
    else:
        start = request.POST['starts']
        end = request.POST['ends']
        strtR = datetime.strptime(str(start), r"%b. %d, %Y").date()
        endR = datetime.strptime(str(end), r"%b. %d, %Y").date()
        report_id = 'CR-' + str(strtR) + '-' + str(endR)
    month_object = datetime.strptime(str(month), "%m")
    or_start = request.POST['or_start']
    or_end = request.POST['or_end']
    cashier = request.POST['cashier_name']
    
    # createQr(report_id)
    class PDF(FPDF):
        def __init__(self, orientation = 'P', unit = 'mm', format = 'Legal'): # other format: Letter, A4
            # Call parent constructor
            FPDF.__init__(self, orientation, unit, format)
            # Initialization
            self.b = 0
            self.i = 0
            self.u = 0
            self.href = ''
            self.page_links = {}
        # Page header
        def header(self):
            # PUP Logo
            # self.image(r'CASHIERING\static\assets\img\logo\PUPLogo.png', 15, 8, 30, 30)
            # QR Code
            # self.image('CASHIERING/static/assets/img/QR-code/' + report_id + '.png', 168, 8, 30, 30)
            # Arial bold 13
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'Polytechnic University of the Philippines', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 13)
            self.cell(0, 0, 'Quezon City Branch', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 12)
            self.cell(0, 0, 'Cashier\'s Office', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'REVOLVING FUND', 0, 0, 'C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position from bottom
            self.set_y(-15)
            # Text color in gray
            self.set_text_color(128)
            # Arial 8 Italic
            self.set_font('Arial', 'I', 9)
            # Footer line
            self.line(10, 340, 200, 340)
            # Line break
            self.ln(5)
            # Page number and other notes
            self.cell(0, 0, 'Page ' + str(self.page_no())  + '/{nb}', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 0, 'Report ID. ' + report_id, 0, 0, 'L')
            self.cell(0, 0, 'Date Generated: ' + str(datetime.now()), 0, 0, 'R')

        # Load data
        def load_data(self, name):
            # Read file lines
            data = []
            with open(name) as file:
                for line in file:
                    data += [line[:-1].split(';')]
            return data

        # Better table
        def improved_table(self, header, data):
            # Data before table
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Account Current: ', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.cell(0, 0, 'LBP ACCOUNT NO. 0682-1020-47', 0, 0, 'R')
            self.ln(20)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Beginning Balance:', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.cell(0, 0, '0.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Add: ', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            if is_loadCertPDF1 == 1:
                self.text(30, 81.2,'Collection per this report ' + month_object.strftime("%B") + ' ' + str(month_f_day) + '-' + str(month_l_day) +', ' + str(year))
            else:
                self.text(30, 81.2,'Collection per this report ' + str(start) + ' to ' + str(end))
            self.cell(0, 0, total, 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Total: ', 0, 0, 'L')
            self.cell(0, 0, total, 0, 0, 'R')
            self.ln(10)
            # Column widths
            w = [58, 58, 58]
            # Header
            self.set_font('Arial', 'B', 12)
            for i in range(0, len(header)):
                self.cell(w[i], 7, header[i], 1, 0, 'C')
            self.ln()
            # Data
            self.set_font('Arial', '', 12)
            for row in data:
                self.cell(w[0], 6, row[0], 'LR', 0, 'C')
                self.cell(w[1], 6, row[1], 'LR', 0, 'C')
                self.cell(w[2], 6, "{0:,.2f}".format(float(row[2])), 'LR', 0, 'R')
                self.ln()
            # Closure line
            self.cell(sum(w), 0, '', 'T')
            self.ln(20)
            self.cell(0, 0, 'Total Deposits: ', 0, 0, 'L')
            self.cell(0, 0, total, 0, 0, 'R')
            self.ln(5)
            self.cell(0, 0, 'Add Balance:', 0, 0, 'L')
            self.cell(0, 0, '0.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 0, 'TOTAL:', 0, 0, 'L')
            self.cell(0, 0, total, 0, 0, 'R')
            # Text String
            self.set_font('Arial', '', 11)
            self.ln(20)
            self.set_fill_color(255,255,240)
            self.multi_cell(w=0, h=5, txt='I hereby certify on my official oath that the above is a true statement of all collections and deposits had by me during the period stated above for which Official Receipts Nos. '+ str(or_start) +'-'+ str(or_end) +' inclusive, were actually issued by me in the amounts shown thereon. I also certify that I have not received money from whatever source without saving issued the necessary Official Receipt in Acknowledgement thereof. Collections received by sub-collectors are recorded above in lump-sum opposite their respective report numbers. I certify further that the balance shown above agrees with the balance appearing in my Cash Receipt Record.', border=0, align='J', fill=1, split_only=False)
            self.ln(10)
            # Arial 11 Bold
            self.set_font('Arial', 'B', 11) 
            self.cell(300, 10, 'Prepared & certified correct:', 0, 0, 'C')
            self.ln(10)
            self.cell(300, 10, 'Ms. ' + cashier, 0, 0, 'C')
            # Arial 11 Normal
            self.set_font('Arial', '', 11) 
            self.ln(5)
            self.cell(300, 10, 'Collecting Officer', 0, 0, 'C')


    pdf = PDF()
    # Column titles
    header = ['Date', 'RA Deposit Slip No.', 'Amount']
    # Data loading
    data = pdf.load_data(r'CASHIERING\views\layouts\textfiles\cert_obj.txt')
    pdf.set_font('Arial', '', 12)
    pdf.set_margins(left=20, top=20)
    pdf.set_auto_page_break(1, 30)
    pdf.add_page()
    pdf.improved_table(header, data)
    pdf.alias_nb_pages()
    pdf.output(r'CASHIERING\views\layouts\reports\certification_report.pdf', 'F')

    import webbrowser
    webbrowser.open_new(r'CASHIERING\views\layouts\reports\certification_report.pdf')
    return JsonResponse('OK', safe=False)

def load_sum_pdf(request):
    total = "{0:,.2f}".format(float(request.POST['total_col']))
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    # month_l_day = calendar.monthrange(year,month)[1]  # this is to get the last day of the month
    month_l_day = request.POST['end_day']
    month_object = datetime.strptime(str(month), "%m")
    cashier = request.POST['cashier']
    report_id = 'SR-' + str(month) + '-1-' + str(month_l_day) + '-' + str(year) 
    # createQr(report_id)
    class PDF(FPDF):
        def __init__(self, orientation = 'P', unit = 'mm', format = 'Legal'): # other format: Letter, A4
            # Call parent constructor
            FPDF.__init__(self, orientation, unit, format)
            # Initialization
            self.b = 0
            self.i = 0
            self.u = 0
            self.href = ''
            self.page_links = {}
        # Page header
        def header(self):
            # PUP Logo
            # self.image(r'CASHIERING\static\assets\img\logo\PUPLogo.png', 15, 8, 30, 30)
            # QR Code
            # self.image('CASHIERING/static/assets/img/QR-code/' + report_id + '.png', 168, 8, 30, 30)
            # Arial bold 13
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'Polytechnic University of the Philippines', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 13)
            self.cell(0, 0, 'Quezon City Branch', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 12)
            self.cell(0, 0, 'Cashier\'s Office', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'SUMMARY OF COLLECTION REPORT', 0, 0, 'C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position from bottom
            self.set_y(-15)
            # Text color in gray
            self.set_text_color(128)
            # Arial 8 Italic
            self.set_font('Arial', 'I', 9)
            # Footer line
            self.line(10, 340, 200, 340)
            # Line break
            self.ln(5)
            # Page number and other notes
            self.cell(0, 0, 'Page ' + str(self.page_no())  + '/{nb}', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 0, 'Report ID. ' + report_id, 0, 0, 'L')
            self.cell(0, 0, 'Date Generated: ' + str(datetime.now()), 0, 0, 'R')

        # Load data
        def load_data(self, name):
            # Read file lines
            data = []
            with open(name) as file:
                for line in file:
                    data += [line[:-1].split(';')]
            return data

        # Better table
        def improved_table(self, header, data):
            # Data before table
            self.set_font('Arial', 'U', 12)
            self.cell(0, 0, 'Month of ' + month_object.strftime("%B") + ' 1-'+ str(month_l_day) +', ' + str(year), 0, 0, 'C')
            self.ln(10)
            # Column widths
            w = [58, 68, 48]
            # Header
            self.set_font('Arial', 'B', 12)
            for i in range(0, len(header)):
                self.cell(w[i], 7, header[i], 1, 0, 'C')
            self.ln()
            # Data
            self.set_font('Arial', '', 12)
            for row in data:
                self.cell(w[0], 7, row[0], 'LR', 0, 'C')
                self.cell(w[1], 7, string.capwords(row[1]), 'LR', 0, 'C') 
                self.cell(w[2], 7, "{0:,.2f}".format(float(row[2])), 'LR', 0, 'R')
                self.ln()
            # Closure line
            self.cell(sum(w), 0, '', 'T')
            self.ln(10)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 0, 'TOTAL:', 0, 0, 'L')
            self.cell(0, 0, total, 0, 0, 'R')
            # Text String
            self.set_font('Arial', '', 11)
            self.ln(10)
            self.set_fill_color(255,255,240)
            self.multi_cell(w=0, h=5, txt='I hereby certify on my official oath that the above is a true statement of all collections and deposits had by me during the period stated above for which Official Receipts Nos. inclusive, were actually issued by me in the amounts shown thereon. I also certify that I have not received money from whatever source without saving issued the necessary Official Receipt in Acknowledgement thereof. Collections received by sub-collectors are recorded above in lump-sum opposite their respective report numbers. I certify further that the balance shown above agrees with the balance appearing in my Cash Receipt Record.', border=0, align='J', fill=1, split_only=False)
            self.ln(10)
            # Arial 11 Bold
            self.set_font('Arial', 'B', 11) 
            self.cell(300, 10, 'Prepared & certified correct:', 0, 0, 'C')
            self.ln(10)
            self.cell(300, 10, 'Ms. ' + cashier, 0, 0, 'C')
            # Arial 11 Normal
            self.set_font('Arial', '', 11) 
            self.ln(5)
            self.cell(300, 10, 'Collecting Officer', 0, 0, 'C')


    pdf = PDF()
    # Column titles
    header = ['Account Code', 'Nature of Collection', 'Amount']
    # Data loading
    data = pdf.load_data(r'CASHIERING\views\layouts\textfiles\sum_obj.txt')
    pdf.set_font('Arial', '', 12)
    pdf.set_margins(left=20, top=20)
    pdf.set_auto_page_break(1, 25)
    pdf.add_page()
    pdf.improved_table(header, data)
    pdf.alias_nb_pages()
    pdf.output(r'CASHIERING\views\layouts\reports\summary_report.pdf', 'F')

    import webbrowser
    webbrowser.open_new(r'CASHIERING\views\layouts\reports\summary_report.pdf')
    return JsonResponse('OK', safe=False)

def load_cash_pdf(request):
    class PDF(FPDF):
        # Page header
        def header(self):
            # PUP Logo
            # self.image(r'CASHIERING\static\assets\img\logo\PUPLogo.png', 15, 8, 30, 30)
            # QR Code
            # self.image(r'CASHIERING\static\assets\img\QR-code\qrsample.png', 168, 8, 30, 30)
            # Arial bold 13
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'Polytechnic University of the Philippines', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 13)
            self.cell(0, 0, 'Quezon City Branch', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 12)
            self.cell(0, 0, 'Cashier\'s Office', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'REVOLVING FUND', 0, 0, 'C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position from bottom
            self.set_y(-15)
            # Text color in gray
            self.set_text_color(128)
            # Arial 8 Italic
            self.set_font('Arial', 'I', 9)
            # Footer line
            self.line(10, 280, 200, 280)
            # Line break
            self.ln(5)
            # Page number and other notes
            self.cell(0, 0, 'Page ' + str(self.page_no())  + '/{nb}', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 0, 'Report No. 00000001', 0, 0, 'L')
            self.cell(0, 0, 'Date Generated: ' + str(datetime.now()), 0, 0, 'R')

        # Load data
        def load_data(self, name):
            # Read file lines
            data = []
            with open(name) as file:
                for line in file:
                    data += [line[:-1].split(';')]
            return data

        # Better table
        def improved_table(self, header, data):
            # Data before table
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Account Current: ', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.cell(0, 0, 'LBP ACCOUNT NO. 0682-1020-47', 0, 0, 'R')
            self.ln(20)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Beginning Balance:', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.cell(0, 0, '0.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Add: ', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.text(26, 81.2,'Collection per this report May 1-31, 2021')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Total: ', 0, 0, 'L')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            self.ln(10)
            # Column widths
            w = [60, 60, 60]
            # Header
            self.set_font('Arial', '', 12)
            for i in range(0, len(header)):
                self.cell(w[i], 7, header[i], 1, 0, 'C')
            self.ln()
            # Data
            for row in data:
                self.cell(w[0], 6, row[0], 'LR', 0, 'C')
                self.cell(w[1], 6, row[1], 'LR', 0, 'C')
                self.cell(w[2], 6, row[2], 'LR', 0, 'R')
                self.ln()
            # Closure line
            self.cell(sum(w), 0, '', 'T')
            self.ln(20)
            self.cell(0, 0, 'Total Deposits: ', 0, 0, 'L')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            self.ln(5)
            self.cell(0, 0, 'Add Balance:', 0, 0, 'L')
            self.cell(0, 0, '0.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 0, 'TOTAL:', 0, 0, 'L')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            # Text String
            self.set_font('Arial', '', 11)
            self.ln(20)
            self.set_fill_color(255,255,240)
            self.multi_cell(w=0, h=5, txt='I hereby certify on my official oath that the above is a true statement of all collections and deposits had by me during the period stated above for which Official Receipts Nos. 0265393-0265546 inclusive, were actually issued by me in the amounts shown thereon. I also certify that I have not received money from whatever source without saving issued the necessary Official Receipt in Acknowledgement thereof. Collections received by sub-collectors are recorded above in lump-sum opposite their respective report numbers. I certify further that the balance shown above agrees with the balance appearing in my Cash Receipt Record.', border=0, align='J', fill=1, split_only=False)
            self.ln(10)
            # Arial 11 Bold
            self.set_font('Arial', 'B', 11) 
            self.cell(0, 10, 'Prepared & certified correct:', 0, 0, 'R')
            self.ln(10)
            self.cell(0, 10, 'Ms. MERLY B. GONZALBO', 0, 0, 'R')
            # Arial 11 Normal
            self.set_font('Arial', '', 11) 
            self.ln(5)
            self.cell(0, 10, 'Collecting Officer         ', 0, 0, 'R')


    pdf = PDF()
    # Column titles
    # header = ['Date', 'RA Deposit Slip No.', 'Amount']
    # Data loading
    # data = pdf.load_data(r'CASHIERING\views\layouts\textfiles\sum_obj.txt')
    pdf.set_font('Arial', '', 12)
    pdf.set_margins(left=15, top=20)
    pdf.set_auto_page_break(1, 20)
    pdf.add_page()
    # pdf.improved_table(header, data)
    pdf.alias_nb_pages()
    pdf.output(r'CASHIERING\views\layouts\reports\cash_receipt_report.pdf', 'F')

    import webbrowser
    webbrowser.open_new(r'CASHIERING\views\layouts\reports\cash_receipt_report.pdf')
    return JsonResponse('OK', safe=False)

def load_mon_pdf(request):
    class PDF(FPDF):
        # Page header
        def header(self):
            # PUP Logo
            # self.image(r'CASHIERING\static\assets\img\logo\PUPLogo.png', 15, 8, 30, 30)
            # QR Code
            # self.image(r'CASHIERING\static\assets\img\QR-code\qrsample.png', 168, 8, 30, 30)
            # Arial bold 13
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'Polytechnic University of the Philippines', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 13)
            self.cell(0, 0, 'Quezon City Branch', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 12)
            self.cell(0, 0, 'Cashier\'s Office', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'REVOLVING FUND', 0, 0, 'C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position from bottom
            self.set_y(-15)
            # Text color in gray
            self.set_text_color(128)
            # Arial 8 Italic
            self.set_font('Arial', 'I', 9)
            # Footer line
            self.line(10, 280, 200, 280)
            # Line break
            self.ln(5)
            # Page number and other notes
            self.cell(0, 0, 'Page ' + str(self.page_no())  + '/{nb}', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 0, 'Report No. 00000001', 0, 0, 'L')
            self.cell(0, 0, 'Date Generated: ' + str(datetime.now()), 0, 0, 'R')

        # Load data
        def load_data(self, name):
            # Read file lines
            data = []
            with open(name) as file:
                for line in file:
                    data += [line[:-1].split(';')]
            return data

        # Better table
        def improved_table(self, header, data):
            # Data before table
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Account Current: ', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.cell(0, 0, 'LBP ACCOUNT NO. 0682-1020-47', 0, 0, 'R')
            self.ln(20)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Beginning Balance:', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.cell(0, 0, '0.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Add: ', 0, 0, 'L')
            self.set_font('Arial', '', 11)
            self.text(26, 81.2,'Collection per this report May 1-31, 2021')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 11)
            self.cell(0, 0, 'Total: ', 0, 0, 'L')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            self.ln(10)
            # Column widths
            w = [60, 60, 60]
            # Header
            self.set_font('Arial', '', 12)
            for i in range(0, len(header)):
                self.cell(w[i], 7, header[i], 1, 0, 'C')
            self.ln()
            # Data
            for row in data:
                self.cell(w[0], 6, row[0], 'LR', 0, 'C')
                self.cell(w[1], 6, row[1], 'LR', 0, 'C')
                self.cell(w[2], 6, row[2], 'LR', 0, 'R')
                self.ln()
            # Closure line
            self.cell(sum(w), 0, '', 'T')
            self.ln(20)
            self.cell(0, 0, 'Total Deposits: ', 0, 0, 'L')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            self.ln(5)
            self.cell(0, 0, 'Add Balance:', 0, 0, 'L')
            self.cell(0, 0, '0.00', 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 0, 'TOTAL:', 0, 0, 'L')
            self.cell(0, 0, '258,284.00', 0, 0, 'R')
            # Text String
            self.set_font('Arial', '', 11)
            self.ln(20)
            self.set_fill_color(255,255,240)
            self.multi_cell(w=0, h=5, txt='I hereby certify on my official oath that the above is a true statement of all collections and deposits had by me during the period stated above for which Official Receipts Nos. 0265393-0265546 inclusive, were actually issued by me in the amounts shown thereon. I also certify that I have not received money from whatever source without saving issued the necessary Official Receipt in Acknowledgement thereof. Collections received by sub-collectors are recorded above in lump-sum opposite their respective report numbers. I certify further that the balance shown above agrees with the balance appearing in my Cash Receipt Record.', border=0, align='J', fill=1, split_only=False)
            self.ln(10)
            # Arial 11 Bold
            self.set_font('Arial', 'B', 11) 
            self.cell(0, 10, 'Prepared & certified correct:', 0, 0, 'R')
            self.ln(10)
            self.cell(0, 10, 'Ms. MERLY B. GONZALBO', 0, 0, 'R')
            # Arial 11 Normal
            self.set_font('Arial', '', 11) 
            self.ln(5)
            self.cell(0, 10, 'Collecting Officer         ', 0, 0, 'R')


    pdf = PDF()
    # Column titles
    # header = ['Date', 'RA Deposit Slip No.', 'Amount']
    # Data loading
    # data = pdf.load_data(r'CASHIERING\views\layouts\textfiles\sum_obj.txt')
    pdf.set_font('Arial', '', 12)
    pdf.set_margins(left=15, top=20)
    pdf.set_auto_page_break(1, 20)
    pdf.add_page()
    # pdf.improved_table(header, data)
    pdf.alias_nb_pages()
    pdf.output(r'CASHIERING\views\layouts\reports\mon_coldep_report.pdf', 'F')

    import webbrowser
    webbrowser.open_new(r'CASHIERING\views\layouts\reports\mon_coldep_report.pdf')
    return JsonResponse('OK', safe=False)

def load_acc_pdf(request):
    # total = "{0:,.2f}".format(float(request.POST['total_dep']))
    is_loadAccPDF1 = int(request.POST['is_loadAccPDF1'])
    cashier = request.POST['cashier_name']
    if is_loadAccPDF1 == 1:
        month = int(request.POST['month'])
        year = int(request.POST['year'])
        # month_l_day = calendar.monthrange(year,month)[1]  # this is to get the last day of the month
        month_f_day = request.POST['start_day']
        month_l_day = request.POST['end_day']
        month_object = datetime.strptime(str(month), "%m")
        report_id = 'AF-' + str(month) + '-1-' + str(month_l_day) + '-' + str(year) 
    else:
        strt = request.POST['start_date']
        end = request.POST['end_date']   
        strtR = datetime.strptime(str(strt), r"%b. %d, %Y").date()
        endR = datetime.strptime(str(end), r"%b. %d, %Y").date()
        report_id = 'AF-' + str(strtR) + '-' + str(endR)
    # createQr(report_id)
    class PDF(FPDF):
        def __init__(self, orientation = 'L', unit = 'mm', format = 'Legal'): # other format: Letter, A4
            # Call parent constructor
            FPDF.__init__(self, orientation, unit, format)
            # Initialization
            self.b = 0
            self.i = 0
            self.u = 0
            self.href = ''
            self.page_links = {}
        # Page header
        def header(self):
            # PUP Logo
            # self.image(r'CASHIERING\static\assets\img\logo\PUPLogo.png', 15, 8, 30, 30)
            # QR Code
            # self.image('CASHIERING/static/assets/img/QR-code/' + report_id + '.png', 315, 8, 30, 30)
            # Arial bold 13
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'Polytechnic University of the Philippines', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 13)
            self.cell(0, 0, 'Quezon City Branch', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', '', 12)
            self.cell(0, 0, 'Cashier\'s Office', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'B', 13)
            self.cell(0, 0, 'REPORT OF ACCOUNTABILITY FOR ACCOUNTABLE FORMS', 0, 0, 'C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position from bottom
            self.set_y(-15)
            # Text color in gray
            self.set_text_color(128)
            # Arial 8 Italic
            self.set_font('Arial', 'I', 9)
            # Footer line
            self.line(10, 280, 200, 280)
            # Line break
            self.ln(5)
            # Page number and other notes
            self.cell(0, 0, 'Page ' + str(self.page_no())  + '/{nb}', 0, 0, 'C')
            self.ln(5)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 0, 'Report No. ' + report_id, 0, 0, 'L')
            self.cell(0, 0, 'Date Generated: ' + str(datetime.now()), 0, 0, 'R')

        # Load data
        def load_data(self, name):
            # Read file lines
            data = []
            with open(name) as file:
                for line in file:
                    data += [line[:-1].split(';')]
            return data

        # Dummy Table
        def dummy_table(self, header):
            # Data before table
            self.set_font('Arial', 'U', 12)
            if is_loadAccPDF1:
                self.cell(0, 0, 'Month of ' + month_object.strftime("%B") + ' ' + str(month_f_day) + '-' + str(month_l_day) +', ' + str(year), 0, 0, 'C')
            else:
                self.cell(0, 0, strt + ' to ' + end, 0, 0, 'C')
            self.ln(10)
            # Column widths
            w = [50, 70, 70, 70, 70]
            # Header
            self.set_font('Arial', 'B', 12)
            for i in range(0, len(header)):
                self.cell(w[i], 7, header[i], 1, 0, 'C')
            self.ln()

        # Dummy Table 2
        def dummy_table2(self, header):
            # Column widths
            w = [50, 22, 48, 22, 48, 22, 48, 22, 48]
            # Header
            self.set_font('Arial', 'B', 10)
            for i in range(0, len(header)):
                self.cell(w[i], 7, header[i], 1, 0, 'C')
            self.ln()

        # Real table
        def improved_table(self, header, data):
            # Column widths
            w = [50, 22, 24, 24, 22, 24, 24, 22, 24, 24, 22, 24, 24]
            # Header
            self.set_font('Arial', 'B', 12)
            for i in range(0, len(header)):
                self.cell(w[i], 7, header[i], 1, 0, 'C')
            self.ln()
            # Data
            self.set_font('Arial', '', 12)
            for row in data:
                self.cell(w[0], 7, 'WITH FACE VALUE', 'LR', 0, 'C')
                self.cell(w[1], 7, str(int(float(row[8]))), 'LR', 0, 'C')
                self.cell(w[2], 7, row[1], 'LR', 0, 'C')
                self.cell(w[3], 7, row[7], 'LR', 0, 'C')
                self.cell(w[4], 7, '', 'LR', 0, 'C')
                self.cell(w[5], 7, '', 'LR', 0, 'C')
                self.cell(w[6], 7, '', 'LR', 0, 'C')
                self.cell(w[7], 7, str(int(float(row[0]))), 'LR', 0, 'C')
                self.cell(w[8], 7, row[1], 'LR', 0, 'C')
                self.cell(w[9], 7, row[2], 'LR', 0, 'C')
                self.cell(w[10], 7, str(int(float(row[9]))), 'LR', 0, 'C')
                self.cell(w[11], 7, str(int(row[2]) + 1), 'LR', 0, 'C')
                self.cell(w[12], 7, row[7], 'LR', 0, 'C')
                self.ln()
            self.cell(w[0], 7, 'WITHOUT FACE VALUE', 'LR', 0, 'C')
            self.cell(w[1], 7, '', 'LR', 0, 'C')
            self.cell(w[2], 7, '', 'LR', 0, 'C')
            self.cell(w[3], 7, '', 'LR', 0, 'C')
            self.cell(w[4], 7, '', 'LR', 0, 'C')
            self.cell(w[5], 7, '', 'LR', 0, 'C')
            self.cell(w[6], 7, '', 'LR', 0, 'C')
            self.cell(w[7], 7, '', 'LR', 0, 'C')
            self.cell(w[8], 7, '', 'LR', 0, 'C')
            self.cell(w[9], 7, '', 'LR', 0, 'C')
            self.cell(w[10], 7, '', 'LR', 0, 'C')
            self.cell(w[11], 7, '', 'LR', 0, 'C')
            self.cell(w[12], 7, '', 'LR', 0, 'C')
            self.ln()
            # Closure line
            self.cell(sum(w), 0, '', 'T')
            self.ln(20)
            self.cell(0, 0, 'Beginning Balance: ', 0, 0, 'L')
            self.cell(0, 0, str(int(float(data[0][8]))), 0, 0, 'R')
            self.ln(5)
            self.cell(0, 0, 'Quantity Issued:', 0, 0, 'L')
            self.cell(0, 0, str(int(float(data[0][0]))), 0, 0, 'R')
            self.ln(5)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 0, 'Ending Balance:', 0, 0, 'L')
            self.cell(0, 0, str(int(float(data[0][9]))), 0, 0, 'R')
            # Text String
            self.set_font('Arial', '', 11)
            self.ln(20)
            self.set_fill_color(255,255,240)
            self.multi_cell(w=0, h=5, txt='I hereby  certify that the foregoing is a true statement of all accountable forms received, issued and transferred by me during the period above-stated and that the beginning and ending balances are correct.', border=0, align='J', fill=1, split_only=False)
            self.ln(10)
            # Arial 11 Bold
            self.set_font('Arial', 'B', 11) 
            self.cell(600, 10, 'Prepared & certified correct:', 0, 0, 'C')
            self.ln(10)
            self.cell(600, 10, cashier, 0, 0, 'C')
            # Arial 11 Normal
            self.set_font('Arial', '', 11) 
            self.ln(5)
            self.cell(600, 10, 'Collecting Officer', 0, 0, 'C')

    pdf = PDF()
    # Column titles
    dummy_header = ['Accountable Forms', 'Beginning Balance', 'Receipt', 'Issuance', 'Ending Balance']
    dummy_header2 = ['', '', 'Inclusive Serial Nos.', '', 'Inclusive Serial Nos.', '', 'Inclusive Serial Nos.', '', 'Inclusive Serial Nos.']
    header = ['Face Value', 'Qty', 'From', 'To', 'Qty', 'From', 'To', 'Qty', 'From', 'To', 'Qty', 'From', 'To']
    # Data loading
    data = pdf.load_data(r'CASHIERING\views\layouts\textfiles\acc_obj.txt')
    pdf.set_font('Arial', '', 12)
    pdf.set_margins(left=15, top=20)
    pdf.set_auto_page_break(1, 20)
    pdf.add_page()
    pdf.dummy_table(dummy_header)
    pdf.dummy_table2(dummy_header2)
    pdf.improved_table(header, data)
    pdf.alias_nb_pages()
    pdf.output(r'CASHIERING\views\layouts\reports\accountable_report.pdf', 'F')

    import webbrowser
    webbrowser.open_new(r'CASHIERING\views\layouts\reports\accountable_report.pdf')
    return JsonResponse('OK', safe=False)

def get_orstart_orend(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ORSTART_OREND"
                    ,(request.POST['start']
                    ,request.POST['end'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_student_with_studno(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_STUDENT_WITH_STUDNO"
                ,(request.POST['studno']
                ,request.POST['fname']
                ,request.POST['mname']
                ,request.POST['lname']
                ,request.POST['course']
                ,request.POST['yr']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_student_without_studno(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_STUDENT_WITHOUT_STUDNO"
                ,(request.POST['fname']
                ,request.POST['mname']
                ,request.POST['lname']
                ,request.POST['course']
                ,request.POST['yr']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def search_last_name(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_STUD_FULLNAME"
                ,(request.POST['str'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def search_last_name_nostudno(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_STUD_FULLNAME_NOSTUDNO"
                ,(request.POST['str'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_pending_deposits(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_PENDING_DEPOSITS")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_pending(request):
    cursor = connection.cursor()
    cursor.callproc("SP_GET_PENDING"
                ,(request.POST['p_date'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def done_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_DONE_DEPOSIT"
                ,(request.POST['p_date'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def save_to_folder(request):
    from PIL import Image
    import cv2
    import base64
    import io
    import numpy as np

    imgdata = base64.b64decode(str(request.POST['img_src']))
    image = Image.open(io.BytesIO(imgdata))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    filename = request.POST['file_name']
    req_from = request.POST['req_from']
    if req_from == 'add-user':
        file_loc = "CASHIERING/static/assets/img/uploads/profile_pictures/" + filename
    else:
        file_loc = "CASHIERING/static/assets/img/uploads/deposits/" + filename
    cv2.imwrite(file_loc, img)
    return JsonResponse(file_loc, safe=False)

def update_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_DEPOSIT"
                    ,(request.POST['date_dep']
                    ,request.POST['group_id']
                    ,request.POST['user_id']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def delete_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_DELETE_DEPOSIT"
                    ,(request.POST['group_id'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def check_or_set(request):
    cursor = connection.cursor()
    cursor.callproc("SP_CHECK_OR_SET")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def change_pass_now(request):
    cursor = connection.cursor()
    cursor.callproc("SP_CHANGE_PASS_NOW"
                    ,(request.POST['new_pass']
                    ,request.session['uname'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def check_old_pass(request):
    cursor = connection.cursor()
    cursor.callproc("SP_CHECK_OLD_PASS"
                    ,(request.POST['old_pass']
                    ,request.session['uname'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_sis_tbl(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SIS_UACS")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def remove_sis(request):
    cursor = connection.cursor()
    cursor.callproc("SP_REMOVE_SIS"
                  ,(request.POST['uacs'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_sis_uacs(request):
    cursor = connection.cursor()
    cursor.callproc("SP_ADD_SIS"
                  ,(request.POST['uacs'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def check_if_sis_payment_done(request):
    cursor = connection.cursor()
    cursor.callproc("SP_CHECK_SIS_PAYMENT_DONE")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_manual_col(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MANUAL_COL_TODAY")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_sis_col(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_SIS_COL_TODAY")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def get_direct_col(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_DIRECT_DEP_COL_TODAY")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def add_daily_col_report(request):
    cursor = connection.cursor()
    cursor.callproc("SP_INSERT_DAILY_COL_REPORT"
                    ,(request.POST['thou']
                    ,request.POST['fiveh']
                    ,request.POST['twoh']
                    ,request.POST['oneh']
                    ,request.POST['fif']
                    ,request.POST['twen']
                    ,request.POST['ten']
                    ,request.POST['fivep']
                    ,request.POST['onep']
                    ,request.POST['twenc']
                    ,request.POST['user_id']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def save_educ_level(request):
    cursor = connection.cursor()
    cursor.callproc("SP_UPDATE_EDUC_LEVEL"
                    ,(request.POST['desc_b4']
                    ,request.POST['desc_new']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_educ_level(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_EDUC_LEVEL")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def remove_educ_level(request):
    cursor = connection.cursor()
    cursor.callproc("SP_REMOVE_EDUC_LEVEL"
                    ,(request.POST['desc'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)