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

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

