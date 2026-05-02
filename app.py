import json
import os
import random

from flask import Flask, render_template, redirect, request

from data import db_session
from data.users import User
from forms.login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index/<title>')
def index(title='Заготовка'):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    prof_lower = prof.lower()
    if 'инженер' in prof_lower or 'строитель' in prof_lower:
        title = 'Инженерные тренажеры'
        img = 'ing.png'
    else:
        title = 'Научные симуляторы'
        img = 'sci.png'

    return render_template('training.html', title=title, img=img)


@app.route('/list_prof/<lst>')
def list_prof(lst):
    professions = [
        'инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
        'инженер по терраформированию', 'климатолог',
        'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
        'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
        'киберинженер', 'штурман', 'пилот дронов'
    ]
    return render_template('list_prof.html', lst=lst, professions=professions)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    param = {
        'title': 'Анкета',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': 'True'
    }
    return render_template('auto_answer.html', **param)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/distribution')
def distribution():
    astronauts = [
        'Ридли Скотт', 'Энди Уир', 'Марк Уотни',
        'Венката Капур', 'Тедди Сандерс', 'Шон Бин'
    ]
    return render_template('distribution.html', astronauts=astronauts, title='Размещение')


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    return render_template('table.html', title='Оформление каюты',
                           sex=sex, age=age)


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    img_dir = 'static/img/landscapes'
    if request.method == 'POST':
        f = request.files['file']
        if f:
            f.save(os.path.join(img_dir, f.filename))
    images = os.listdir(img_dir)
    return render_template('galery.html', images=images)


@app.route('/member')
def member():
    with open('templates/crew.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    random_member = random.choice(data['crew'])
    return render_template('member.html', member=random_member)

def main():
    app.run()


if __name__ == '__main__':
    main()