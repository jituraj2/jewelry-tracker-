from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'  # Change this securely

USER_FILE = 'users.json'
# Create file if it’s missing
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Home / Dashboard
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('index.html')

# Sign In
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
        return render_template('signin.html', error="Invalid email or password.")
    return render_template('signin.html')

# Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        users = load_users()

        if email in users:
            return render_template('signup.html', error="User already exists.")

        users[email] = {
            'name': request.form['name'],
            'mobile': request.form['mobile'],
            'password': request.form['password'],
            'profile': ''  # Add later if needed
        }
        save_users(users)

        session['user'] = email  # auto-login
        return redirect(url_for('index'))
    return render_template('signup.html')

# Reset Password
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email']
        new_pass = request.form['new_password']
        users = load_users()

        if email in users:
            users[email]['password'] = new_pass
            save_users(users)
            return redirect(url_for('signin'))
        return render_template('reset.html', error="User not found")
    return render_template('reset.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('signin'))

# Launch
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
