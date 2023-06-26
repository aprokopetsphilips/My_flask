from flask import Flask,flash, render_template,url_for,request,flash,session,redirect,abort, g
from FDataBase import FDataBase
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm
from admin.admin import admin # мпорт именно переменной для Blueprint
# settings
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY= '1234567890qwerty'
MAX_CONTENT_LENGHT = 1024*1024

app = Flask(__name__)
app.config.from_object(__name__) # загрузка конфигурации непосредствено из приложения(__name__ ссылается на текущий файл)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.register_blueprint(admin, url_prefix='/admin') # url_prefix необяз. параметр позволяет добавлять к домену его автоматом,а затем уже будет идти URL blueprint

login_manager = LoginManager(app)
login_manager.login_view = 'login' # перенаправляет если для просмотра требуется авторизация
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'
@login_manager.user_loader
def load_user(user_id):
    print('load user')
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return  g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()
@app.route('/')
def index():
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())

@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'],request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи res is empty', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи block', category='error')
    return render_template('add_post.html',menu = dbase.getMenu(), title='Добавление статьи' )

@app.route('/post/<alias>')
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=dbase.getMenu())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit(): # проверяет тип запроса и делает валидацию по параметрам из forms
        user = dbase.getUserByEmail(form.email.data) # данные по полю из объекта в forms
        if user and check_password_hash(user['psw'],form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            print(rm)
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))

        flash('Неверная пара логин/пароль', 'error')

    return render_template('login.html', menu=dbase.getMenu(), title='Авторизация', form=form)




@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if request.method == 'POST':
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(form.name.data, form.email.data, hash)
            if res:
                flash('успешно зарегистрированы', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в БД', 'error')
        else:
            flash('Неверно заполнены поля', 'error')

    return render_template("register.html",menu=dbase.getMenu(), title='Регистрация',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user() # модуль из flask login
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a><p>user info: {current_user.get_id()}"""





if __name__ == '__main__':
    app.run(debug=True)




