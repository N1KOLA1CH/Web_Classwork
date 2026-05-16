import flask
from flask import jsonify, make_response, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users_list = db_sess.query(User).all()
    result = jsonify(
        {
            'users': [
                item.to_dict(only=('id', 'surname', 'name', 'age',
                                   'position', 'speciality', 'address',
                                   'email', 'modified_date', 'city_from'))
                for item in users_list
            ]
        }
    )
    db_sess.close()
    return result


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        db_sess.close()
        return make_response(jsonify({'error': 'Not found'}), 404)
    result = jsonify(
        {
            'users': user.to_dict(only=(
                'id', 'surname', 'name', 'age',
                'position', 'speciality', 'address',
                'email', 'modified_date', 'city_from'))
        }
    )
    db_sess.close()
    return result


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    fields = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']
    if not all(key in request.json for key in fields):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    if 'id' in request.json:
        if db_sess.query(User).get(request.json['id']):
            db_sess.close()
            return make_response(jsonify({'error': 'Id already exists'}), 400)
    if db_sess.query(User).filter(User.email == request.json['email']).first():
        db_sess.close()
        return make_response(jsonify({'error': 'Email already exists'}), 400)

    user = User(
        id=request.json.get('id'),
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    user.set_password(request.json['password'])

    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        db_sess.close()
        return make_response(jsonify({'error': 'Not found'}), 404)
    if not request.json:
        db_sess.close()
        return make_response(jsonify({'error': 'Empty request'}), 400)

    fields = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email']
    if not all(key in request.json for key in fields):
        db_sess.close()
        return make_response(jsonify({'error': 'Bad request'}), 400)

    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email'],
    user.city_from = request.json['city_from']

    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        db_sess.close()
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})
