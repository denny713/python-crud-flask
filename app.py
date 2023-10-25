from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:p@ssw0rd@localhost/crud_demo'
db = SQLAlchemy(app)

from models import User

db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    nama = request.form['nama']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    user = User(username=username, nama=nama, password=password)
    db.session.add(user)
    db.session.commit()
    flash('User added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get(id)
    user.username = request.form['username']
    user.nama = request.form['nama']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    user.password = password
    user.status = int(request.form['status'])
    db.session.commit()
    flash('User updated successfully', 'success')
    return redirect(url_for('index'))

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)