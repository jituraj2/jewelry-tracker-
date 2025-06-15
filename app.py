from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this to something secure

USER_FILE = 'users.json'

# Ensure users.json exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('index.html', user=session['user'])

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        user = users.get(email)

        if user and user['password'] == password:
            session['user'] = email
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        profile = request.form.get('profile') or ''

        users = load_users()

        if email in users:
            flash("User already exists!", "error")
            return redirect(url_for('signup'))

        users[email] = {
            'name': name,
            'mobile': mobile,
            'password': password,
            'profile': profile
        }

        save_users(users)
        session['user'] = email
        flash("Signup successful!", "success")
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        users = load_users()

        if email in users:
            users[email]['password'] = new_password
            save_users(users)
            flash("Password reset successful!", "success")
            return redirect(url_for('signin'))
        else:
            flash("User not found!", "error")
            return redirect(url_for('reset'))

    return render_template('reset.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('signin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
