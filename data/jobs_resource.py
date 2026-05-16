from flask_restful import reqparse, abort, Resource

from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.get(Jobs, job_id)
    session.close()
    if not job:
        abort(404, message=f'Job {job_id} not found')


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.get(Jobs, job_id)
        result = {'job': job.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'is_finished')
        )}
        session.close()
        return result

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.get(Jobs, job_id)
        session.delete(job)
        session.commit()
        result = {'success': 'OK'}
        session.close()
        return result


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        result = {'jobs': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'is_finished')
        ) for item in jobs]}
        session.close()
        return result

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()
        result = {'id': job.id}
        session.close()
        return result
