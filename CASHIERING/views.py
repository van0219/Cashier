from __future__ import with_statement
from django.conf import settings
from django.shortcuts import render, redirect, resolve_url
from django.db import IntegrityError, connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from fpdf import *
from datetime import datetime

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


def account(request):
    return render(request, 'views/layouts/pages/account.html')

def sis_payments(request):
    return render(request, 'views/layouts/pages/sis_payments.html')

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
    cursor.callproc("SP_SELECT_ALL_UACS_CODE"
                    ,(request.POST['incomeType'],))
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
                    ,request.POST['userID']))
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
                    ,request.POST['date_end']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_collection_history2(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_COLLECTION_PENDING"
                    ,(request.POST['date_start']
                    ,request.POST['date_end']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def deposits(request):
    return render(request, 'views/layouts/pages/deposits.html')

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
                    ,request.POST['date_sched']
                    ,request.POST['notes']
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
                    ,(request.POST['group_id']
                    ,request.POST['slip_num']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_acct_forms_dash(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_ACCOUNTABLE_FORMS_REPORT"
                    ,(request.POST['month']
                    ,'CARD'))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_or_monthly_report(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_OR_MONTHLY_REPORT")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_cert_table(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_CERT_TABLE"
                    ,(request.POST['month'],))
    data = cursor.fetchall()
    import csv
    csv_rowlist = data
    with open(r'C:\Users\Van Anthony Silleza\CASHIER\CASHIERING\views\layouts\textfiles\cert_obj.txt', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(csv_rowlist)
    return JsonResponse(data, safe=False)

def load_monthly_collection_deposit(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MONTHLY_COLLECTION")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_monthly_collection_deposit2(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MONTHLY_DEPOSIT")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_radar_chart(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_RADAR_CHART"
                    ,(request.POST['month'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_cash_receipt_cards(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_CASH_RECEIPT_CARDS"
                    ,(request.POST['month'],))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_dashboard_cards(request):
    cursor = connection.cursor()
    cursor.callproc("SP_LOAD_DASHBOARD_CARDS")
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_dashboard_bar_graph(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_MONTHLY_COLLECTION")
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
    imgFile = "CASHIERING/static/assets/img/logo/key.png"
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
                    ,(request.POST['month'],))
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
                    ,(request.POST['month']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_coldep_group(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_COLLECTION_GROUP"
                    ,(request.POST['month']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_top_contrib(request):
    cursor = connection.cursor()
    cursor.callproc("SP_SELECT_TOP_CONTRIB"
                    ,(request.POST['month']))
    data = cursor.fetchall()
    return JsonResponse(data, safe=False)

def load_cert_pdf(request):
    class PDF(FPDF):
        # Page header
        def header(self):
            # PUP Logo
            self.image(r'CASHIERING\static\assets\img\logo\PUPLogo.png', 15, 8, 30, 30)
            # QR Code
            self.image(r'CASHIERING\static\assets\img\QR-code\qrsample.png', 168, 8, 30, 30)
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
    header = ['Date', 'RA Deposit Slip No.', 'Amount']
    # Data loading
    data = pdf.load_data(r'CASHIERING\views\layouts\textfiles\cert_obj.txt')
    pdf.set_font('Arial', '', 12)
    pdf.set_margins(left=15, top=20)
    pdf.set_auto_page_break(1, 20)
    pdf.add_page()
    pdf.improved_table(header, data)
    pdf.alias_nb_pages()
    pdf.output(r'CASHIERING\views\layouts\reports\certification_report.pdf', 'F')

    import webbrowser
    webbrowser.open_new(r'CASHIERING\views\layouts\reports\certification_report.pdf')
    return JsonResponse('OK', safe=False)

