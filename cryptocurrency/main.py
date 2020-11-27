import flask, flask_login, os, cryptocurrency, json, base64, cryptocode

Blockchain = cryptocurrency.Blockchain()
json.dump(Blockchain.blockchain, open('blockchain.json', 'w'), indent=4)

login_manager = flask_login.LoginManager()
app = flask.Flask(__name__)
app.secret_key = os.urandom(12).hex()
login_manager.init_app(app)

users = json.load(open('users.json', 'r'))

def data_encrypt(data):
    return cryptocode.encrypt(data, base64.b64decode(eval(f"b'{open('key.txt', 'r').read()}'")).decode('utf-8'))

def data_decrypt(data):
    return cryptocode.decrypt(data, base64.b64decode(eval(f"b'{open('key.txt', 'r').read()}'")).decode('utf-8'))

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == users[email]['password']
    return user

@app.errorhandler(404)
def page_not_found(e):
    return '''
<h1>404 Not Found</h1>
<p>Oops! The requested URL was not found on the server.</p>
'''

@app.errorhandler(401)
def login_redirect(e):
    return flask.redirect(flask.url_for('login'))

class User(flask_login.UserMixin):
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    email = flask.request.form['email']
    if email in users:
        if flask.request.form['password'] == data_decrypt(users[email]['password']):
            user = User()
            user.id = email
            if flask.request.form['remember']:
                flask_login.login_user(user, remember=True)
            else:
                flask_login.login_user(user)
            return flask.redirect(flask.url_for('home'))

    return '''
<div class="alert">
  <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
  <strong>Incorrect email or password.</strong>
</div>''' + flask.render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global users
    if flask.request.method == 'GET':
        return flask.render_template('signup.html')
    if flask.request.form['email'] not in users:
        if flask.request.form['name'] != '' and flask.request.form['email'] != '' and flask.request.form['password'] != '':
            users[flask.request.form['email']] = {'password': data_encrypt(flask.request.form['password']), 'name': flask.request.form['name'], 'balance': data_encrypt(str(0))}
            json.dump(users, open('users.json', 'w'), indent=4)
            user = User()
            user.id = flask.request.form['email']
            flask_login.login_user(user, remember=True)
            return flask.redirect(flask.url_for('home'))
    else:
        return '''
<div class="alert">
  <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
  <strong>Sorry! This email is already used.</strong>
</div>''' + flask.render_template('signup.html')

@app.route('/')
@flask_login.login_required
def home():
    return flask.render_template('index.html', user_balance=data_decrypt(users[flask_login.current_user.id]['balance']))

@app.route('/mine')
@flask_login.login_required
def mine():
    return flask.render_template('mine.html')

@app.route('/transaction', methods=['GET', 'POST'])
@flask_login.login_required
def transaction():
    if flask.request.method == 'GET':
        return flask.render_template('transaction.html', user_email=[flask_login.current_user.id][0], user_balance=data_decrypt(users[flask_login.current_user.id]['balance']))
    if flask.request.form['to'] in users:
        if flask.request.form['amount'] != '0':
            cryptocurrency.Transaction(flask.request.form['from'], flask.request.form['to'], flask.request.form['amount'], Blockchain)
            return flask.render_template('home.html')
        else:
            return '''
<div class="alert">
  <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
  <strong>Please use a number bigger than 0.</strong>
</div>''' + flask.render_template('transaction.html', user_email=[flask_login.current_user.id][0], user_balance=data_decrypt(users[flask_login.current_user.id]['balance']))
    else:
        return '''
<div class="alert">
  <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
  <strong>Email not found.</strong>
</div>''' + flask.render_template('transaction.html', user_email=[flask_login.current_user.id][0], user_balance=data_decrypt(users[flask_login.current_user.id]['balance']))

@app.route('/buy')
@flask_login.login_required
def buy():
    return flask.render_template('buy.html')

app.run(debug=True, port=5000)

