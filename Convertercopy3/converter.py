from flask import Flask, render_template, request, redirect, url_for, session, logging,flash
import urllib.request
from bs4 import BeautifulSoup
import bs4
import pandas as pd
import sqlite3 as sql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import html5lib
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "registrationfinal.db")

App = Flask(__name__)
url = 'https://www.x-rates.com/table/?from=USD&amount=1'
tables = pd.read_html(url)
usd_table = tables[1]
url1 = 'https://www.x-rates.com/table/?from=EUR&amount=1'
tables1 = pd.read_html(url1)
euro_table = tables1[1]
url2 = 'https://www.x-rates.com/table/?from=GBP&amount=1'
tables2 = pd.read_html(url2)
gbp_table = tables2[1]
url3 = 'https://www.x-rates.com/table/?from=SGD&amount=1'
tables3 = pd.read_html(url3)
sgd_table = tables3[1]
url4 = 'https://www.x-rates.com/table/?from=CHF&amount=1'
tables4 = pd.read_html(url4)
swiss_table = tables4[1]
url5 = 'https://www.x-rates.com/table/?from=RUB&amount=1'
tables5 = pd.read_html(url5)
rub_table = tables5[1]
url6 = 'https://www.x-rates.com/table/?from=AUD&amount=1'
tables6 = pd.read_html(url6)
aud_table = tables6[1]
url7 = 'https://www.x-rates.com/table/?from=IDR&amount=1'
tables7 = pd.read_html(url7)
idr_table = tables7[1]
url8 = 'https://www.x-rates.com/table/?from=CNY&amount=1'
tables8 = pd.read_html(url8)
cny_table = tables8[1]
with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS students")
    cur.execute("CREATE TABLE students(amount INT, from_curr TEXT, to_curr TEXT, amount_final INT)")



@App.route('/')
def index():
    return render_template('index.html')
    
@App.route('/currencyconverter', methods = ['POST','GET'])
def currencyconverter():
    f_form = t_form = []
    address = "https://www.x-rates.com/calculator/"
    soup = BeautifulSoup(urllib.request.urlopen(address).read(), "html.parser")
    fromcurr = "Enter From Currency"
    tocurr = "Enter To Currency"
    from_form = soup.find("select",attrs={"name":"from"})
    if from_form is not None:
        from_form=from_form.contents
    else:
        pass
    if from_form is not None:
        for _ in from_form:
            if type(_) is not bs4.element.NavigableString:
                f_form.append(_.string)
    else:
        pass

    to_form = soup.find("select", attrs={"name":"to"})
    if to_form is not None:
        to_form.contents
    else:
        pass
    if to_form is not None:
        for _ in to_form:
            if type(_) is not bs4.element.NavigableString:
                t_form.append(_.string)
    else:
        pass

    if request.method == 'GET':
        amount = ""
        amount_final = ""
    else :
        amount = "".join(request.form.getlist('Amount'))
        if len(amount)==0:
            amount_final="Invalid input"
        if amount.isdigit() == False:
            amount_final="Invalid input"
        else:
            for s in [int(s) for s in amount.split() if amount.isdigit()]:
                if(s==0):
                    amount_final="Cannot input 0"
                else:
                    fromcurr = "".join(request.form.getlist('From'))
                    tocurr = "".join(request.form.getlist('To'))
                    new_address = "https://www.x-rates.com/calculator/?from="+fromcurr+"&to="+tocurr+"&amount="+amount
                    new_soup = BeautifulSoup(urllib.request.urlopen(new_address).read(), "html.parser")
                    amount_final = str(new_soup.find("span",{"class":"ccOutputRslt"}).contents[0])
                    with sql.connect("database.db") as con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO students (amount,from_curr,to_curr,amount_final) VALUES (?,?,?,?)",(amount,fromcurr,tocurr,amount_final))
                        con.commit()

                        
    return render_template('currencyconverter.html', answer=amount_final, amount=amount, from_form=f_form, to_form=t_form , from_select=fromcurr, to_select=tocurr)
    con.close()

@App.route('/setdefault', methods = ['POST','GET'])
def setdefault():
    def_form=[]
    address = "https://www.x-rates.com/calculator/"
    soup = BeautifulSoup(urllib.request.urlopen(address).read(), "html.parser")
    defaultcurr= "Select your Default Currency"

    default_form=soup.find("select",attrs={"name":"from"})
    if default_form is not None:
        default_form=default_form.contents
    else:
        pass
    if default_form is not None:
        for _ in default_form:
            if type(_) is not bs4.element.NavigableString:
                def_form.append(_.string)
    else:
        pass
    if request.method == 'POST':
        defaultcurr= "".join(request.form.getlist('Default'))
    with sql.connect("defaulttable.db") as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS setdefault")
        con.execute("CREATE TABLE setdefault(selected_default_curr varchar(50))")
        cur.execute("INSERT INTO setdefault (selected_default_curr) VALUES(?)",[defaultcurr])
        con.commit()
    return render_template('setdefault.html',default_form=def_form,default_select=defaultcurr)
    con.close()

@App.route('/setdefaultcrypt', methods = ['POST','GET'])
def setdefaultcrypt():
    crypt_form=["Bitcoin","Ethereum","Ripple","Litecoin","Bitcoin-Cash"]
    defaultcrypt= "Select your Default CryptoCurrency"
    if request.method == 'POST':
        defaultcrypt= "".join(request.form.getlist('Crypt'))
    with sql.connect("defaulttablefinal.db") as con:
       cur = con.cursor()
       cur.execute("DROP TABLE IF EXISTS setdefault")
       con.execute("CREATE TABLE setdefault(selected_default_crypt varchar (50))")
       cur.execute("INSERT INTO setdefault (selected_default_crypt) VALUES(?)",[defaultcrypt])
       con.commit()
    return render_template('setdefaultcrypt.html',crypt_form=crypt_form,crypt_select=defaultcrypt)
    con.close()
@App.route('/listdefault')
def listdefault():
   con = sql.connect("defaulttable.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("SELECT * FROM setdefault")
   
   rows = cur.fetchall();
   con = sql.connect("defaulttablefinal.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("SELECT * FROM setdefault")
   
   rowss = cur.fetchall();
   return render_template("listdefault.html",rows = rows,rowss=rowss)

@App.route('/usd')
def usd():

    return render_template('usd.html',  tables=[usd_table.to_html(classes='data')], titles=usd_table.columns.values)
    
@App.route('/euro')
def euro():

    return render_template('euro.html',  tables1=[euro_table.to_html(classes='data')], titles=euro_table.columns.values)
@App.route('/pound')
def pound():

    return render_template('pound.html',  tables2=[gbp_table.to_html(classes='data')], titles=gbp_table.columns.values)
@App.route('/sgd')
def sgd():

    return render_template('sgd.html',  tables3=[sgd_table.to_html(classes='data')], titles=sgd_table.columns.values)
@App.route('/chf')
def chf():

    return render_template('chf.html',  tables4=[swiss_table.to_html(classes='data')], titles=swiss_table.columns.values)
@App.route('/rub')
def rub():

    return render_template('rub.html',  tables5=[rub_table.to_html(classes='data')], titles=rub_table.columns.values)
@App.route('/aud')
def aud():

    return render_template('aud.html',  tables6=[aud_table.to_html(classes='data')], titles=aud_table.columns.values)
@App.route('/idr')
def idr():

    return render_template('idr.html',  tables7=[idr_table.to_html(classes='data')], titles=idr_table.columns.values)
@App.route('/cny')
def cny():

    return render_template('cny.html',  tables8=[cny_table.to_html(classes='data')], titles=cny_table.columns.values)
@App.route('/usd2')
def usd2():

    return render_template('usd2.html',  tables=[usd_table.to_html(classes='data')], titles=usd_table.columns.values)
    
@App.route('/euro2')
def euro2():

    return render_template('euro2.html',  tables1=[euro_table.to_html(classes='data')], titles=euro_table.columns.values)
@App.route('/pound2')
def pound2():

    return render_template('pound2.html',  tables2=[gbp_table.to_html(classes='data')], titles=gbp_table.columns.values)
@App.route('/sgd2')
def sgd2():

    return render_template('sgd2.html',  tables3=[sgd_table.to_html(classes='data')], titles=sgd_table.columns.values)
@App.route('/chf2')
def chf2():

    return render_template('chf2.html',  tables4=[swiss_table.to_html(classes='data')], titles=swiss_table.columns.values)
@App.route('/rub2')
def rub2():

    return render_template('rub2.html',  tables5=[rub_table.to_html(classes='data')], titles=rub_table.columns.values)
@App.route('/aud2')
def aud2():

    return render_template('aud2.html',  tables6=[aud_table.to_html(classes='data')], titles=aud_table.columns.values)
@App.route('/idr2')
def idr2():

    return render_template('idr2.html',  tables7=[idr_table.to_html(classes='data')], titles=idr_table.columns.values)
@App.route('/cny2')
def cny2():

    return render_template('cny2.html',  tables8=[cny_table.to_html(classes='data')], titles=cny_table.columns.values)

    
@App.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("SELECT * FROM students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@App.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        with sql.connect(db_path) as con:
            cur = con.cursor()
        x = cur.execute("SELECT username FROM register WHERE username=:username", {"username":username}).fetchone()
        if x is not None:
            flash("That username is already taken, please choose another")
            return render_template('register.html', form=form)
            
        else:
        
            cur.execute("INSERT INTO register(name, email, username, password) VALUES(?, ?, ?, ?)", (name, email, username, password))

                # Commit to DB
            con.commit()

                # Close connection
            con.close()

            flash('You are now registered and can log in', 'success')


        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@App.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        with sql.connect(db_path) as con:
            cur = con.cursor()

        result = cur.execute("SELECT * FROM register WHERE username = ?", [username])

        if result is not None:
            
            data = cur.fetchone()
            if data is None:
                error = 'Username not found'
                return render_template('login.html', error=error)
            password = data[4]

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            cur.close()


    return render_template('login.html')
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@App.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@App.route('/dashboard')
@is_logged_in
def dashboard():
        return render_template('dashboard.html')
        
@App.route('/currencyconverter2', methods = ['POST','GET'])
def currencyconverter2():
    with sql.connect("defaulttable.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM setdefault")
        rows=cur.fetchall()
        for row in rows:
            a= row[0]
    aud="AUD"
    cad="CAD"
    chf="CHF"
    cny="CNY"
    dkk="dkk"
    eur="EUR"
    gbp="GBP"
    hkd="HKD"
    huf="HUF"
    inr="INR"
    jpy="JPY"
    mxn="MXN"
    myr="MYR"
    nok="NOK"
    nzd="NZD"
    php="PHP"
    rub="RUB"
    sek="SEK"
    sgd="SGD"
    thb="THB"
    g="TRY"
    usd="USD"
    zar="ZAR"
    if a==aud:
        a=0
    if a==cad:
        a=1
    if a==chf:
        a=2
    if a==cny:
        a=3
    if a==dkk:
        a=4
    if a==eur:
        a=5
    if a==gbp:
        a=6
    if a==hkd:
        a=7
    if a==huf:
        a=8
    if a==inr:
        a=9
    if a==jpy:
        a=10
    if a==mxn:
        a=11
    if a==myr:
        a=12
    if a==nok:
        a=13
    if a==nzd:
        a=14
    if a==php:
        a=15
    if a==rub:
        a=16
    if a==sek:
        a=17
    if a==sgd:
        a=18
    if a==thb:
        a=19
    if a==g:
        a=20
    if a==usd:
        a=21
    if a==zar:
        a=22
    f_form = t_form = []
    address = "https://www.x-rates.com/calculator/"
    soup = BeautifulSoup(urllib.request.urlopen(address).read(), "html.parser")
    from_form = soup.find("select",attrs={"name":"from"})
    if from_form is not None:
        from_form=from_form.contents
    else:
        pass
    if from_form is not None:
        for _ in from_form:
            if type(_) is not bs4.element.NavigableString:
                f_form.append(_.string)
    else:
        pass
    to_form = soup.find("select", attrs={"name":"to"})
    if to_form is not None:
        to_form.contents
    else:
        pass
    if to_form is not None:
        for _ in to_form:
            if type(_) is not bs4.element.NavigableString:
                t_form.append(_.string)
    else:
        pass

    if request.method == 'GET':
        amount = ""
        amount_final = ""
    else :
        amount = "".join(request.form.getlist('Amount'))
        if len(amount)==0:
            amount_final="Invalid input"
        if amount.isdigit() == False:
            amount_final="Invalid input"
        else:
            for s in [int(s) for s in amount.split() if amount.isdigit()]:
                if(s==0):
                    amount_final="Cannot input 0"
                else:
                    fromcurr = "".join(request.form.getlist('From'))
                    tocurr = "".join(request.form.getlist('To'))
                    new_address = "https://www.x-rates.com/calculator/?from="+fromcurr+"&to="+tocurr+"&amount="+amount
                    new_soup = BeautifulSoup(urllib.request.urlopen(new_address).read(), "html.parser")
                    amount_final = str(new_soup.find("span",{"class":"ccOutputRslt"}).contents[0])
                    with sql.connect("database.db") as con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO students (amount,from_curr,to_curr,amount_final) VALUES (?,?,?,?)",(amount,fromcurr,tocurr,amount_final))
                        con.commit()
                      
                        
                            
                
    return render_template('currencyconverter2.html', answer=amount_final, amount=amount, from_form=f_form, to_form=t_form, a=a )
    con.close()
@App.route('/cryptocurrencyconverter', methods = ['POST','GET'])
def cryptocurrencyconverter():
    f_form = t_form = []
    fromcurr = "Enter From Currency"
    tocurr = "Enter To Currency"
    f_form=['Bitcoin', 'Ethereum','Ripple', 'Litecoin', 'Bitcoin-Cash','USD','EUR','GBP','RUB','SGD','HKD']


    t_form=['Bitcoin', 'Ethereum','Ripple', 'Litecoin', 'Bitcoin-Cash','USD','EUR','GBP','RUB','SGD','HKD']

    if request.method == 'GET':
        amount = ""
        amount_final = ""
    else :
        amount = "".join(request.form.getlist('Amount'))
        if len(amount)==0:
            amount_final="Invalid input"
        if amount.isdigit() == False:
            amount_final="Invalid input"
        else:
            for s in [int(s) for s in amount.split() if amount.isdigit()]:
                if(s==0):
                    amount_final="Cannot input 0"
                else:
                    fromcurr = "".join(request.form.getlist('From'))
                    tocurr = "".join(request.form.getlist('To'))
                    new_address = "https://walletinvestor.com/converter/"+fromcurr+"/"+tocurr+"/"+amount
                    new_soup = BeautifulSoup(urllib.request.urlopen(new_address).read(), "html.parser")
                    amount_final = str(new_soup.find("span",{"class":"converter-title-amount"}).contents[0])
    return render_template('cryptocurrencyconverter.html', answer=amount_final, amount=amount, from_form=f_form, to_form=t_form , from_select=fromcurr, to_select=tocurr)

@App.route('/cryptocurrencyconverter2', methods = ['POST','GET'])
def cryptocurrencyconverter2():
    with sql.connect("defaulttablefinal.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM setdefault")
        rows=cur.fetchall()
        for row in rows:
            a= row[0]
    btc="Bitcoin"
    eth="Ethereum"
    rip="Ripple"
    ltc="Litecoin"
    btcc="Bitcoin-Cash"
    if a==btc:
        a=0
    if a==eth:
        a=1
    if a==rip:
        a=2
    if a==ltc:
        a=3
    if a==btcc:
        a=4
    
    f_form = t_form = []
    
    fromcurr = "Enter From Currency"
    f_form=['Bitcoin', 'Ethereum','Ripple', 'Litecoin', 'Bitcoin-Cash','USD','EUR','GBP','RUB','SGD','HKD']


    t_form=['Bitcoin', 'Ethereum','Ripple', 'Litecoin', 'Bitcoin-Cash','USD','EUR','GBP','RUB','SGD','HKD']

    if request.method == 'GET':
        amount = ""
        amount_final = ""
    else :
        amount = "".join(request.form.getlist('Amount'))
        if len(amount)==0:
            amount_final="Invalid input"
        if amount.isdigit() == False:
            amount_final="Invalid input"
        else:
            for s in [int(s) for s in amount.split() if amount.isdigit()]:
                if(s==0):
                    amount_final="Cannot input 0"
                else:
                    fromcurr = "".join(request.form.getlist('From'))
                    tocurr = "".join(request.form.getlist('To'))
                    new_address = "https://walletinvestor.com/converter/"+fromcurr+"/"+tocurr+"/"+amount
                    new_soup = BeautifulSoup(urllib.request.urlopen(new_address).read(), "html.parser")
                    amount_final = str(new_soup.find("span",{"class":"converter-title-amount"}).contents[0])
    return render_template('cryptocurrencyconverter2.html', answer=amount_final, amount=amount, from_form=f_form, to_form=t_form , from_select=fromcurr, a=a)


@App.route('/list2')
def list2():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("SELECT * FROM students")
   
   rows = cur.fetchall();
   return render_template("list2.html",rows = rows)
if __name__ == '__main__':
    App.secret_key='flask'
    App.debug=True
    App.run()
