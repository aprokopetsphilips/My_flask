import sqlite3

from flask import Blueprint,render_template, url_for, flash,request,redirect,session, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static') # 'admin'-имя blueprint,добавляется к именам методов определенных внутри blueprint, __name__-определяет где искать следующие папки, template_folder='templates', static_folder='static'


menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.listusers', 'title': 'Список пользователей'},
        {'url': '.listpubs', 'title': 'Список статей'},
        {'url': '.logout', 'title': 'Выйти'}]


db = None
@admin.before_request # устнанавливает соединение с БД до выполнения запроса
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Админ панель')

@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    if request.method == "POST":
        if request.form['user'] == 'andrey' and request.form['psw'] == 'andrey':
            login_admin()
            return redirect(url_for('.index')) # точка указывает что index нужно брать из текущей директории
        else:
            flash('Неверная пара логин/пароль', 'error')

    return render_template('admin/login.html', title='Админ-панель')

@admin.route('/logout', methods=['POST','GET'])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))

@admin.route('/list-pubs')
def listpubs():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            list = cur.fetchall() # через fetchall() получаем список словарей
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/listpubs.html', title='Список статей', menu=menu, list=list)

@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/listusers.html', title='Список пользователей', menu=menu, list=list)