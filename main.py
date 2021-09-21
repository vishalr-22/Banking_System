from flask import Flask, render_template, request, url_for, redirect, flash
from dbservice import dbservice
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "super secret key"

db = dbservice()

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/homepage')
def homepage2():
    return render_template('homepage.html')


@app.route('/view_cust',methods=['POST','GET'])
def view_cust():
    table = 'Customer'
    data = db.fetch_column_data(table, ['Cust_ID','Name','Balance'])
    return render_template('view_customers.html', data = data)


@app.route('/view_1cust/<id>',methods=['POST','GET'])
def view_1cust(id):
    table = 'Customer'
    id = int(id)
    data = db.fetch_column_data(table, ['Cust_ID','Name','Balance'], condition_name = 'Cust_id', condition_value = id)
    return render_template('view_1cust.html',data = data)


@app.route('/single_cust_payment/<id>',methods=['POST','GET'])
def single_cust_payment(id):
    if request.method=='POST':
        table = 'Customer'
        id = int(id)
        amount = request.form.get('amount')
        data1 = db.fetch_column_data(table, ['Balance'], condition_name = 'Cust_id', condition_value = id)
        data1 = int(data1[0][0]) +int(amount)
        db.transfer_1cust(table, id, data1)
        data = db.fetch_column_data(table, ['Cust_ID','Name','Balance'], condition_name = 'Cust_id', condition_value = id)
        return render_template('view_1cust.html',data = data, text = 'Payment Successful!')


@app.route('/transfer',methods=['POST','GET'])
def transfer():
    if request.method=='POST':
        table1 = 'Customer'
        table2 = 'transaction'
        payee = request.form.get('payee')
        payer = request.form.get('payer')
        amount = request.form.get('amount')
        data = [payee,payer,amount]
        t = db.transfer(table1, table2,  data)
        if t == 0:
            return render_template('transfer.html',text='Insufficient Balance!')    
        elif t == 1:
            return render_template('transfer.html',text='Payment Successful!')
        else:
            return render_template('transfer.html',text='Unexpected Error!')
    
    return render_template('transfer.html')


@app.route('/transaction',methods=['POST','GET'])
def transaction():
    table = 'Transaction'
    data = db.fetch_column_data(table, ['Trans_ID', 'Payee', 'Payer','Amount','Status'])
    
    return render_template('transaction.html', data = data)

