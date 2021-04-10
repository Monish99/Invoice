import mysql
from django.shortcuts import HttpResponse, render
from mysql.connector import Error
from .inv import someRandom
from .sndMail import det


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


def trainerBankDet(n):
    que = "SELECT * FROM trainer where Name='" + n + "'"
    TBD = read_query(conn, que)
    print(TBD)
    return TBD


conn = create_connection("localhost", "root", "", "genesis")
q = "SELECT Name from collage"
q1 = "SELECT Name from trainer"
res = str(read_query(conn, q1))
colName = str(read_query(conn, q))
l = colName.split("'")
cn = []
for i in range(len(l)):
    if i % 2 == 1:
        cn.append(l[i])
tn = []
l1 = res.split("'")
for i in range(len(l1)):
    if i % 2 == 1:
        tn.append(l1[i])
print("\n", colName)


def calcDays(sd, ed):
    st = sd.split("-")
    d = int(st[2])
    m = int(st[1])
    et = ed.split("-")
    da = int(et[2])
    mo = int(et[1])
    nod = da - d
    if m != mo:
        mAbs = (mo - m) * 30
        nod = mAbs + nod
    return nod

def home(request):
    return render(request, "home.html", {'colName': cn, 'trName': tn})


def display(request):
    trainerName = request.GET["trName"]
    collegeName = request.GET["colName"]
    domain = request.GET["dom"]
    #noOfDays = request.GET["Day"]
    start_date = request.GET["SD"]
    end_date = request.GET["ED"]
    t_hrs = request.GET["TH"]
    mode = request.GET["mode"]
    print(start_date, "\n", end_date)
    noOfDays = calcDays(start_date, end_date)
    print(noOfDays)
    print("type of NOD", type(noOfDays))
    #result = "Duration of the training " + str(noOfDays)
    #TBD = trainerBankDet(trainerName)
    someRandom(trainerName, collegeName, mode, noOfDays, start_date)
    det(trainerName, collegeName, t_hrs, noOfDays, mode, start_date, end_date)
    return render(request, "home.html", {'message': 'Email Sent'})






