from flask import Flask, render_template, request
import urllib.request
from bs4 import BeautifulSoup
import bs4
import pandas as pd

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
@App.route('/currency_converter', methods = ['POST','GET'])
def currency_converter():
    f_form = t_form = []
    address = "https://www.x-rates.com/calculator/"
    soup = BeautifulSoup(urllib.request.urlopen(address).read(), "html.parser")
    fromcurr = "Enter From Currency"
    tocurr = "Enter To Currency"
    from_form = soup.find("select",attrs={"id":"from"})
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

    to_form = soup.find("select", attrs={"id":"to"})
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

            
    
    return render_template("currency_converter.html", answer=amount_final, amount=amount, from_form=f_form, to_form=t_form , from_select=fromcurr, to_select=tocurr)

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
    
    
    
    
    
    
@App.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    App.debug=True
    App.run()
