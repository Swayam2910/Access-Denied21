
from flask import Flask, redirect , url_for, request, session, render_template,flash
import json
import smtplib
import pandas as pd
import numpy as np
from csv import reader,writer
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

#from twilio.rest import Client
#from flask import CURSE
app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'Oh So Secret'


def send_an_email():
    toaddr = 'ramgopalg92@gmail.com'    
    me = 'swayam.dheer2020@vitstudent.ac.in' 
    subject = "Query Successfully Submitted"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = toaddr
    msg.preamble = "test "
    text='''
            Your query has been successfully submitted.
            Hereby Attached the pdf of the query recorded by the system.
        '''
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("query_letter.pdf", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="query_letter.pdf"')
    msg.attach(part)

    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    print("S is",s)
    s.login(me, password = 'Urd291174@')
       #s.send_message(msg)
    s.sendmail(me, toaddr, msg.as_string())
    s.quit()
    #except:
    #   print ("Error: unable to send email")


def validate(filename):
    open_file=open(filename,encoding="UTF-8")
    read_file=reader(open_file)
    list_file=list(read_file)
    print(list_file)
    keyset={}
    for row in list_file:
        if row!=[]:
            print('row is',row)
            user=row[0]
            passw=row[1]
            type1=row[2]
            if user not in keyset:
                keyset[user]=[passw,type1]
    return keyset
def getlist(filename):
    open_file=open(filename,encoding="UTF-8")
    read_file=reader(open_file)
    list_file=list(read_file)
    alist={}
    for row in list_file:
        if row!=[]:
            name=row[0]
            if name not in alist:
                alist[name]=[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]]
    return alist
def getuid(filename):
    open_file=open(filename,encoding="UTF-8")
    read_file=reader(open_file)
    list_file=list(read_file)
    alist=[]
    for row in list_file:
        if row!=[]:
            alist.append(row[0])
    return alist
@app.route('/')
def launcher():
    return render_template('new_login.html')

@app.route('/input_login')
def input_login():
    return render_template('login1.html')
#Login System using Aadhar UID


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        uid = request.form['Username']
        password=request.form['Password']
        dataset=validate('data.csv')
        print(dataset)
        print(uid)
        if(uid in dataset):
            alist=dataset[uid]### alist[0]--> Password    alist[1]---> type
            print(alist)
            if(password==alist[0]):
                print("List is",alist)
                if(alist[1]=='Doctor'):
                    
                    return redirect(url_for('input'))   ### link for doctor.html
                else:
                    return redirect(url_for('input2'))  ### link for municipal.html
            else:
                return("You have Entered Wrong Id or Password")
        else:
            return ("You have Entered Wrong Id or Password")
            
    else:
        print("Request is",request)
        uid = request.args.get('Username')
        password=request.args.get('Password')
        dataset=validate('data.csv')
        print("Data is",dataset)
        return redirect(url_for('input'))

    
@app.route('/newid')
def newid():
    return render_template('reg.html')
@app.route('/forgotpass')
def forgotpass():
    return render_template('changepass.html')


@app.route('/changepassw')
def changepassw():
    if request.method=='POST':
        print("Post")
    else:
        uid1=request.args.get('uid')
        password=request.args.get('psw')
        password_repeat=request.args.get('psw-repeat')
        checklist=getuid("data.csv")
        if uid1 in checklist:
            if(password==password_repeat):
                df = pd.read_csv("data.csv")
                df.set_value(checklist.index(uid1)-1, "Password",int(password))
                df.to_csv("data.csv",index=False)
                flash('Password Successfully Changed')
                return render_template('changepass.html')
            else:
                flash('Password Does not match Re-enter the Details')
                return render_template('changepass.html')
        else:
            flash('Enter Aadhar Number Does Not Exist/Not in the Database')
            return render_template('changepass.html')

@app.route('/makeid')
def makeid():
    if request.method=='POST':
        fullname=request.form['Fullname']
        username=request.form['Username']
        email=request.form['Email']
        phone_number=request.form['Phone number']
        password=request.form['psw']
        password_repeat=request.form['psw-repeat']
        gender=request.form['Gender']
        occupation=request.form['occupation']
    
        return 'You have successfully registered'
    else:
        print("Request Arg",request)
        username=request.args.get('Username')
        mobile=request.args.get('Phone number')
        password=request.args.get('psw')
        password_repeat=request.args.get('psw-repeat')
        occupation=request.args.get('occupation')
        if(password==password_repeat):
            alist1=[username,password,occupation]
            with open('data.csv', 'a') as writeFile:
                writer11 = writer(writeFile)
                writer11.writerow(alist1)
            return 'You have registered successfully'
        else:
            flash('Password Does not match Re-enter the Details')
            return render_template('reg.html')
        

@app.route('/success/<uID>')
def success(uID):
    return ("Registered UID : %s" % uID)

@app.route('/input2')
def input2():
    return render_template('municipal.html')

@app.route('/query')
def query():
    return render_template('query.html')


@app.route('/querynode')
def querynode():
    if request.method=='POST':
        print("This here")
    else:
        uid=request.args.get('fname')
        name=request.args.get('lname')
        typeofquery=request.args.get('country')
        issue=request.args.get('subject')

        doc = SimpleDocTemplate("query_letter.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        Story=[]
        formatted_time = time.ctime()

        logo='python_logo.png'
 
        im = Image(logo, 3*inch, 3*inch)     #### Adding Image here
        Story.append(im)
 
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=12>Time of Submission :- %s</font>' % formatted_time
 
        Story.append(Paragraph(ptext, styles["Normal"]))     ### Adding time here
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Dear %s:</font>' % name.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
 
        ptext = '<font size=12>The type of Query Submitted is :- %s.</font>' % (typeofquery)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Description :- %s.</font>' % (issue)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        
        ptext = '<font size=12><b>Thank you very much and we look forward to serving you.</b></font>'
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Sincerely,</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1,12))
        ptext = '<font size=12>Swayam Dheer/Ramgopal Garudkar/Karthik Kishore</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        doc.build(Story)
        send_an_email()
        print("Get here")
    return "Your Query is Submitted"

# Data Collector Node
@app.route('/input')
def input():
    return render_template('doctor.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/datatx', methods = ['POST', 'GET'])
def data_tx():
    if request.method == 'POST':
        c=request.form['search']
        return render_template("login.html")

    else:
        data= request.args.get('search')
        list_name=getlist('ud.csv')
        if data in list_name:
            return render_template('result.html',var1=data,var2=list_name[data][0],var3=list_name[data][1],var4=list_name[data][2],var5=list_name[data][3],var6=list_name[data][4],var7=list_name[data][5],var8=list_name[data][6],var9=list_name[data][7],var10=list_name[data][8])
        else:
            flash('The Given Name is Not in the Database')
            return redirect(url_for('input'))

@app.route('/fta', methods = ['POST', 'GET'])
def fta_tx1():
    toaddr = 'ramgopalg92@gmail.com'    
    me = 'swayam.dheer2020@vitstudent.ac.in' 
    subject = "Appointment Scheduled for a Specialist"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = toaddr
    msg.preamble = "test "
    text='''
        Respected Sir/Maam,
        
            Your Appointment has been scheduled.
            Date of Appointment: 21st-March-2021
            Location-Reliance Greens,Motikhavadi
            Time of Appointment: 9:30am
            Contact for any queries: 9843567210

        PS:- Please be avaialable prior 30 minutes the given time of appointment.

    '''


    msg.attach(MIMEText(text))
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login("swayam.dheer2020@vitstudent.ac.in","Urd291174@")
    s.sendmail("swayam.dheer2020@vitstudent.ac.in","ramgopalg92@gmail.com",msg.as_string())
    s.quit()
    return "The Appointment is Scheduled"


if __name__=='__main__':
    app.run(debug=False)
