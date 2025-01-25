from flask import *
from random import randint
from face_detection import *
from face_reg import *
import sqlite3 as sql
from datetime import datetime
app = Flask(__name__)
app.secret_key="panda"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        bname = request.form['bname']
        aadhar = request.form['aadhar']
        def random_with_N_digits(n):    
            range_start = 10**(n-1)
            range_end = (10**n)-1
            return randint(range_start, range_end)
        a=random_with_N_digits(16)
        pin = random_with_N_digits(4)
        print(pin)
        get(username)
        con = sql.connect('bank.db')
        cur =con.cursor()
        cur.execute('insert into register(acc_no,pin,name,email,username,password,phone,bname,aadhar,amount) values(?,?,?,?,?,?,?,?,?,?)',(a,pin,name,email,username,password,phone,bname,aadhar,5000))
        con.commit()
        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        print(name)
        password = request.form['password']
        con  = sql.connect('bank.db')
        cur = con.cursor()
        cur.execute('select username,password,acc_no,pin from register where username=? and password=?',(name,password))
        data = list(cur.fetchone())
        p = data[3]
        ano = data[2]
        
        print(data)
        con.commit()
        ac = face_reg(name)
        print(ac)
        if ac == 'Unauthorized':
            return render_template('login.html',error='error')
        elif ac == 'Authorized':
            session['name'] =name
            session['pin'] = p
            session['ano'] = ano
            print(type(session['ano']))
            print(type(session['pin']))
            print('auth')
            return render_template('home.html',name=name,acc_no=data[2],pin=data[3] )
        elif ac=='Invalid User':
            return render_template('login.html',invalid='invalid')
    return render_template('login.html')


@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        acc_no = request.form['acc_no']
        f_name = request.form['name']
        session['f_name'] = f_name
        r_name = request.form['r_name']
        session['r_name'] = r_name
        to_acc = request.form['to_acc']
        amount = request.form['amount']
        pin = request.form['pin']
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        ac = face_reg(f_name)
        print("ac = ",ac)
        print(type(acc_no))
        print(type(pin))
        # con = sql.connect('bank.db')
        # cur = con.cursor()
        # res = cur.execute("select acc_no,pin from register where acc_no =?",(acc_no))
        # con.commit()  
        # print("res= ",res) 
        cd = (str(session['ano'])).strip()
        xy = (str(session['pin'])).strip()
        ab = acc_no.strip()
        lm = pin.strip()
        print(type(cd))
        if ac == 'Authorized':
            if cd == ab and xy == lm:
                con = sql.connect('bank.db')   
                cur1 = con.cursor()
                cur1.execute("insert into Transaction1 (f_acc,f_name,r_name,to_acc,amount,date) values (?,?,?,?,?,?)",(acc_no,f_name,r_name,to_acc,amount,date))
                cur2 = con.cursor()
                cur2.execute("update register set amount=amount-?  where acc_no=?",(amount,acc_no))
                cur3 = con.cursor()
                cur3.execute("update register set amount=amount+?  where acc_no=?",(amount,to_acc))
                con.commit()
                return render_template('home.html',authorized='authorized')
            else:
                return render_template('home.html',invalid_access='invalid_access')
        elif ac == 'Unauthorized':
            return render_template('home.html',unauthorized='unauthorized') 
        elif ac == 'Invalid User':
            return render_template('home.html',Invalid='Invalid User')        
        return render_template('home.html')
    else:
        return render_template('home.html',name=session['name'],acc_no=session['ano'],pin=session['pin'])


@app.route("/check_balance")
def check_balance():
    balance = str(session['ano'])
    con = sql.connect("bank.db")
    # con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select amount from register where acc_no = ?",(balance,))
    res = cur.fetchone()
    con.commit()
    print(res)
    am = float(res[0])
    print(balance)
    return render_template("check_balance.html",res=am,acc=balance)

@app.route("/transaction_details")
def transaction_details():
    ac = session['ano']
    con = sql.connect("bank.db")
    cur2 = con.cursor()
    cur2.execute("select f_name,r_name,amount from Transaction1 where to_acc = ? or f_acc = ?",(ac,ac,))
    res2 = cur2.fetchall()
    con.commit()
    f_name = session['name']
    # r_name = session['r_name']
    det = []
    for i in res2:
        if i[1] == f_name:
            det.append([i[0],i[2],'credited'])
        elif i[0] == f_name:
            det.append([i[1],i[2],'debited'])
        print(i)
    print(det)
    return render_template("transaction_details.html",res = det) 

if __name__ == '__main__':
    app.run(debug=True)