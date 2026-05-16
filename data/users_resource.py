from flask_restful import reqparse, abort, Resource

from data import db_session
from data.users import User


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('city_from', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.get(User, user_id)
    session.close()
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        result = {'user': user.to_dict(
            only=('surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'email'))}
        session.close()
        return result

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        result = {'success': 'OK'}
        session.close()
        return result


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        result = {'users': [item.to_dict(
            only=('surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'email')) for item in users]}
        session.close()
        return result

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        result = {'id': user.id}
        session.close()
        return result