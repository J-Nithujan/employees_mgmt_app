# File: views.py
# Author: Nithujan Jegatheeswaran
# Brief: 
# Version: 19.03.2022

from flask import Flask, request, redirect, url_for, render_template, session
from .model.utils import *
import base64

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        if check_login(request.form['email'], request.form['password']):
            # Successfully logged in
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        else:
            # Login failed
            return render_template('login.html')
    else:
        # First visit on the login page
        return render_template('login.html')


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/index/')
def index():
    data = get_index_data(session['email'])
    session['firstname'] = data['firstname']
    session['lastname'] = data['lastname']
    if data['department'] == 'Human Ressources':
        session['is_hr_employee'] = True
    else:
        session['is_hr_employee'] = False
    return render_template('index.html', data=data, is_hr_employee=session['is_hr_employee'], email=session['email'])


@app.route('/tasks_list/<email>/')
def tasks_list(email):
    tasks = get_tasks_list(email)
    return render_template('tasks_list.html', email=session['email'], list=tasks)


@app.route('/new_task/')
@app.route('/new_task/', methods=['POST'])
def new_task():
    if request.method == 'POST':
        msg_list = add_task(request.form, session['email'])
        if msg_list:
            return render_template('new_task.html', email=session['email'], errors=msg_list, form=request.form)
        else:
            return redirect(url_for('tasks_list', email=session['email']))
    else:
        return render_template('new_task.html', email=session['email'])


@app.route('/edit_task/<task_id>')
@app.route('/edit_task/', methods=['POST'])
def edit_task(task_id):
    if request.method == 'POST':
        update_task(request.form, task_id)
        return redirect(url_for('tasks_list', email=session['email']))
    else:
        task = get_selected_task(task_id)
        return render_template('edit_task.html', email=session['email'], data=task)
    pass


@app.route('/payslips/')
def payslips():
    # TODO: payslips page and model functions
    pass
