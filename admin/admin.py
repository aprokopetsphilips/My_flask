from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static') # 'admin'-имя blueprint,добавляется к именам методов определенных внутри blueprint, __name__-определяет где искать следующие папки, template_folder='templates', static_folder='static'

@admin.route('/')
def index():
    return "admin"