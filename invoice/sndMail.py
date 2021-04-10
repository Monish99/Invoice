import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import mysql
from mysql.connector import Error


def create_connection(hn, un, pw, dbn):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hn,
            user=un,
            passwd=pw,
            database=dbn
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def read_query(con, que):
    cursor = con.cursor()
    result = None
    try:
        cursor.execute(que)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error:", err)


def det(tn, cn, NoHrs, NoD, mode, stD, eDT):
    conn = create_connection("localhost", "root", "", "genesis")

    # Selecting PAy from trainer table
    q = "SELECT Payment from trainer where Name='" + tn + "'"
    res = str(read_query(conn, q))
    paa = res.split("(")
    paya = paa[1].split(",")
    pay = paya[0]

    # Fetching Food col from DB
    q = "SELECT Food from collage where Name='" + cn + "'"
    res = str(read_query(conn, q))
    fo = res.split("'")
    food = fo[1]

    # Fetching email of the trainer
    q = "SELECT Email from trainer where Name='" + tn + "'"
    res = str(read_query(conn, q))
    #print(res)
    ma = res.split("'")
    mail = ma[1]
    #print(mail, "type", type(mail))

    send_test_mail(cn, pay, NoHrs, NoD, mode, stD, eDT, food, mail)


def send_test_mail(cn, pay, NoHrs, NoD, mode, stD, eDT, food, mail):
    # setting up the email
    sender_email = "teamvoid35@gmail.com"
    receiver_email = mail
    msg = MIMEMultipart()
    msg['Subject'] = 'Confirmation Mail'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    # formatting the email as req
    colName = "Name of the college : " + cn
    fee = "Remuneration " + pay + "/- per day incl of TDS"
    hrs = "Total number of hours : " + NoHrs
    days = "Totoal number of days : " + str(NoD)
    mod = "Mode of training : " + mode
    da = "Date : " + stD + " to " + eDT
    foo = "Food : " + food
    msgText = MIMEText('Greeting from Genesis!!!\n This is an email confirmation post of our telephonic conversation '
                       'about you associating with Genesis for our forthcoming project on the contractual basis. '
                       'PBF the details about the project.\n\n ' + colName + "\n" + fee + "\n" + hrs + "\n" + days + "\n" + mod + "\n" + da + "\n" + foo + "\n")
    msg.attach(msgText)
    # Attaching the Docx file
    pdf = MIMEApplication(open("invoice.pdf", 'rb').read())
    pdf.add_header('Content-Disposition', 'attachment', filename="invoice.pdf")
    msg.attach(pdf)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("teamvoid35@gmail.com", "Gmail@123")
        s.sendmail("teamvoid35@gmail.com", "monishraj350@gmail.com", msg.as_string())
        s.quit()
    except Exception as e:
        print(e)



