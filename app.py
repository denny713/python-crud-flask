from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import hashlib
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

password = 'p@ssw0rd'
encoded_pass = quote(password, safe='')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_pass}@localhost/crud_demo'
db = SQLAlchemy(app)

class Akun(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=1)
    username = db.Column(db.String(10), nullable=False, unique=True)
    nama = db.Column(db.String(50))
    password = db.Column(db.String(64), nullable=False)
    status = db.Column(db.Integer, default=1)

@app.route('/')
def index():
    users = Akun.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    nama = request.form['nama']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    user = Akun(username=username, nama=nama, password=password)
    db.session.add(user)
    db.session.commit()
    flash('User added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    user = Akun.query.get(id)
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
    user = Akun.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)