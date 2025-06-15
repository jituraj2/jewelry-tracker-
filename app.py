from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to something secure

USER_FILE = 'users.json'

# Create users.json if not exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

# Load users from JSON
def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

# Save users to JSON
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

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
        users = load_users()
        user = users.get(email)

        if user and user['password'] == password:
            session['user'] = email
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error="Invalid credentials")
    
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
            return render_template('signup.html', error="User already exists")

        users[email] = {
            'name': name,
            'mobile': mobile,
            'password': password,
            'profile': profile
        }

        save_users(users)
        session['user'] = email  # Auto-login after signup
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
            return redirect(url_for('signin'))
        else:
            return render_template('reset.html', error="User not found")

    return render_template('reset.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
