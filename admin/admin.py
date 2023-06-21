from flask import Blueprint,render_template, url_for, flash,request,redirect,session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static') # 'admin'-имя blueprint,добавляется к именам методов определенных внутри blueprint, __name__-определяет где искать следующие папки, template_folder='templates', static_folder='static'

def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

@admin.route('/')
def index():
    return "admin"

@admin.route('/login')
def index():
    if request.method == "POST":
        if request.form['user'] == 'Andrey' and request.form['psw'] == '00000':
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