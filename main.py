import requests
from flask import Flask, render_template, redirect, abort, request, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session, jobs_api, users_api
from data.category import Category
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.departament import DepartmentForm
from forms.job import JobsForm
from forms.login import LoginForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


def init_data_users():
    session = db_session.create_session()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap"
    user.city_from = "Moscow"

    user1 = User(
        surname="Las",
        name="Parker",
        age=23,
        position="medic",
        speciality="research engineer",
        address="module_1",
        email="las@mars.org",
        hashed_password="jab",
        city_from="Washington", )

    user2 = User(
        surname="Sco",
        name="Dley",
        age=21,
        position="rid",
        speciality="research engineer",
        address="module_1",
        email="ssssf@mars.org",
        hashed_password="hel",
        city_from="Madrid")

    user3 = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="sc@mars.org",
        hashed_password="password",
        city_from="Cheboksary")

    session.add(user)
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()


def init_data_jobs():
    db_sess = db_session.create_session()
    job1 = Jobs(team_leader=1, job='deployment of residential modules 1 and 2',
                work_size=15, is_finished=False, collaborators='1, 2')
    job2 = Jobs(team_leader=2, job=' of residential modules 1 and 2',
                work_size=15, is_finished=False, collaborators='1, 2')
    job3 = Jobs(team_leader=3, job='sincist',
                work_size=15, is_finished=False, collaborators='3, 2')
    job4 = Jobs(team_leader=4, job='deployment of work',
                work_size=15, is_finished=True, collaborators='4, 2')

    db_sess.add(job1)
    db_sess.add(job2)
    db_sess.add(job3)
    db_sess.add(job4)
    db_sess.commit()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            city_from=form.city_from.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def init_data_with_categories():
    db_sess = db_session.create_session()
    if not db_sess.query(Category).first():
        c1 = Category(name="1")
        c2 = Category(name="2")
        c3 = Category(name="3")
        db_sess.add_all([c1, c2, c3])
        db_sess.commit()

    all_jobs = db_sess.query(Jobs).all()
    all_cats = db_sess.query(Category).all()

    if len(all_jobs) >= 4 and len(all_cats) >= 3:
        if not all_jobs[0].categories:
            all_jobs[0].categories.append(all_cats[2])
        if not all_jobs[1].categories:
            all_jobs[1].categories.append(all_cats[0])
        if not all_jobs[2].categories:
            all_jobs[2].categories.append(all_cats[2])
        if not all_jobs[3].categories:
            all_jobs[3].categories.append(all_cats[1])
        db_sess.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobsForm()
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    form.category.choices = [(c.id, c.name) for c in categories]
    users = db_sess.query(User).all()
    form.team_leader.choices = [(u.id, f"{u.surname} {u.name}") for u in users]
    if request.method == 'GET':
        form.team_leader.data = current_user.id
    if form.validate_on_submit():
        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        selected_category = db_sess.query(Category).get(form.category.data)
        if selected_category:
            job.categories.append(selected_category)
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Adding a Job', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()

    if not job:
        abort(404)

    if int(job.team_leader) != int(current_user.id) and int(current_user.id) != 1:
        abort(403)
    users = db_sess.query(User).all()
    form.team_leader.choices = [(u.id, f"{u.surname} {u.name}") for u in users]

    categories = db_sess.query(Category).all()
    form.category.choices = [(c.id, c.name) for c in categories]

    if request.method == "GET":
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
        if job.categories:
            form.category.data = job.categories[0].id

    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.categories.clear()
        selected_category = db_sess.query(Category).get(form.category.data)
        if selected_category:
            job.categories.append(selected_category)

        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).filter(Department.id == id).first()
    if dept:
        if dept.chief == current_user.id or current_user.id == 1:
            db_sess.delete(dept)
            db_sess.commit()
        else:
            db_sess.close()
            abort(403)
    else:
        db_sess.close()
        abort(404)
    db_sess.close()
    return redirect('/departments')


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()

    if job:
        if int(job.team_leader) == int(current_user.id) or int(current_user.id) == 1:
            db_sess.delete(job)
            db_sess.commit()
        else:
            abort(403)
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def list_departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('departments.html', departments=departments)


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.chief.choices = [(u.id, f"{u.surname} {u.name}") for u in users]
    if request.method == 'GET':
        form.chief.data = current_user.id

    if form.validate_on_submit():

        if db_sess.query(Department).filter(Department.email == form.email.data).first():
            return render_template('add_department.html',
                                   form=form, message="Такой email уже зарегистрирован за другим отделом")

        dept = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(dept)
        db_sess.commit()
        return redirect('/departments')

    return render_template('add_department.html', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    dept = db_sess.query(Department).filter(Department.id == id).first()

    if not dept:
        abort(404)

    if int(dept.chief) != int(current_user.id) and int(current_user.id) != 1:
        abort(403)

    users = db_sess.query(User).all()
    form.chief.choices = [(u.id, f"{u.surname} {u.name}") for u in users]

    if request.method == "GET":
        form.title.data = dept.title
        form.chief.data = dept.chief
        form.members.data = dept.members
        form.email.data = dept.email

    if form.validate_on_submit():
        dept.title = form.title.data
        dept.chief = form.chief.data
        dept.members = form.members.data
        dept.email = form.email.data
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Editing Department', form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    response = requests.get(f'http://localhost:8080/api/users/{user_id}')
    if not response or response.status_code == 404:
        abort(404)

    user_data = response.json().get('users')
    city = user_data.get('city_from')

    if not city:
        return 'У данного колониста не указан родной город.'

    geocoder_api_server = 'https://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        'apikey': 'edfadee6-4727-487f-9a6c-130b10dc0514',
        'geocode': city,
        'format': 'json'
    }

    geo_response = requests.get(geocoder_api_server, params=geocoder_params)

    if not geo_response or geo_response.status_code != 200:
        return 'Ошибка геокодирования города.'

    json_coord = geo_response.json()
    features = json_coord['response']['GeoObjectCollection']['featureMember']
    if not features:
        return 'Город не найден на картах.'

    toponym = features[0]['GeoObject']
    toponym_cordinates = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_cordinates.split(' ')

    map_url = (
        f'https://static-maps.yandex.ru/1.x/?'
        f'll={toponym_longitude},{toponym_lattitude}&'
        f'z=12&'
        f'l=sat'
    )

    return render_template('nostalgy.html', user=user_data, map_url=map_url)


def main():
    db_session.global_init("db/mars_explorer.db")
    # init_data_users()
    # init_data_jobs()
    # init_data_with_categories()
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
