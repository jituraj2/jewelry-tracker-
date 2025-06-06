from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/reset')
def reset():
    return render_template('reset.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Load users
        with open('users.json', 'r') as f:
            users = json.load(f)

        user = next((u for u in users if u['email'] == email and u['password'] == password), None)

        if user:
            session['user'] = user['email']
            return redirect(url_for('index'))  # 🔁 Redirect to the main page
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for('signin'))

    return render_template('signin.html')

