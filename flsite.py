from flask import Flask,flash, render_template,url_for,request,flash,session,redirect,abort, g
from FDataBase import FDataBase
app = Flask(__name__)
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app.config['SECRET_KEY'] = '1234567890qwerty'
DATABASE = '/tmp/flsite.db'
DEBUG = True
app.config.from_object(__name__) # загрузка конфигурации непосредствено из приложения(__name__ ссылается на текущий файл)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

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
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=dbase.getMenu())


@app.route('/login')
def login():
    return render_template('login.html', menu=dbase.getMenu(), title='Авторизация')


@app.route("/register")
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash('успешно зарегистрированы', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в БД', 'error')
        else:
            flash('Неверно заполнены поля', 'error')

    return render_template("register.html",menu=dbase.getMenu(), title='Регистрация')


if __name__ == '__main__':
    app.run(debug=True)




