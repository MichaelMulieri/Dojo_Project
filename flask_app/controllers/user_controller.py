from crypt import methods
from urllib import response
from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.pedal import Pedal
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import os
from decouple import config
from dotenv import load_dotenv
load_dotenv()
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@app.route('/')
def reg_log():
    return render_template('reg_log.html')

@app.route('/register', methods=['POST'])
def save_user():
    if not User.validate_user(request.form):
        return redirect('/')  
    data={
        "first_name" :request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    user = User.get_one(data)
    return render_template('welcome.html', user = user)

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/build')

@app.route('/build')
def build_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    all_pedals = Pedal.show_all_pedals()
    user = User.get_one(data)
    return render_template('build_page.html', user = user, all_pedals = all_pedals)

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    users_pedals = Pedal.show_pedals_by_user(data)
    pedal_price = Pedal.calculate_total(data)
    sales_tax = Pedal.calculate_tax(data)
    grand_total = Pedal.grand_total(data)
    return render_template('checkout.html', grand_total = grand_total, sales_tax = sales_tax, pedal_price = pedal_price, user = user, users_pedals = users_pedals)

@app.route('/purchase')
def submit_purchase():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }            
    user = User.get_one(data)
    grand_total = Pedal.grand_total(data)
    message = Mail(from_email = 'Dreamboardcustoms@gmail.com',
                to_emails= f'{user.email}',
                subject = 'Your recent Dream Board Customs order info',
                plain_text_content = f'Your total is {grand_total}',
                html_content = f'<p>Your total is ${grand_total}.00. Thanks for your support!</p>')
    try :
        sg = SendGridAPIClient(os.getenv('KEY'))
        print(os.getenv('KEY'))
        response = sg.send(message)
    except Exception as e:
        print(message)
    return render_template('submit_purchase.html', user = user, grand_total = grand_total)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')