from crypt import methods
from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
import pprint
from flask_app.models.user import User
from flask_app.models.pedal import Pedal

@app.route('/save/pedal', methods=["POST"])
def save_pedal():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"],
        "pedal_id" : request.form['pedal_id']
    }
    Pedal.save_pedal(data)
    return redirect('/build')

@app.route('/your/board/<int:id>')
def show_user_board(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    users_pedals = Pedal.show_pedals_by_user(data)
    this_user = User.get_one(data)
    return render_template('your_board.html', users_pedals = users_pedals, this_user = this_user)

@app.route('/demo/vid/<int:id>')
def demo_vid(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id'],
        "user_id" : session['user_id'],
        "pedal_id" : id
    }
    user = User.get_one(data)
    this_pedal_vid = Pedal.show_one_pedal_by_id(data)
    return render_template('demo_vid.html', user = user, this_pedal_vid = this_pedal_vid)

@app.route('/destroy/<int:id>')
def destroy(id):
    data = {
        "pedal_id":id,
        "user_id" : session['user_id']
    }
    print(data)
    Pedal.destroy(data)
    return redirect(f'/your/board/{id}')
