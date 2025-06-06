from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Load user data
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)
        else:
            users = []

        user = next((u for u in users if u['email'] == email and u['password'] == password), None)

        if user:
            session['user'] = email
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

