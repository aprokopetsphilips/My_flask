from flask import Flask, render_template,url_for,request,flash

app = Flask(__name__)

app.config['SECRET_KEY'] = '1234567890qwerty'

menu = [{'name':'Установка', 'url': 'install-flask'},
        {'name':'Первое приложение', 'url': 'first-app'},
        {'name':'Обратная связь', 'url': 'contact'}
        ]


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', menu=menu, title='О сайте')
@app.route('/contact', methods=['POST','GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Не смог')

    return render_template('contact.html', title = 'Обратная связь', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)
