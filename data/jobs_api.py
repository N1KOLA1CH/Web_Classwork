import flask
from flask import jsonify, make_response, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs_list = db_sess.query(Jobs).all()
    result = jsonify(
        {
            'jobs': [
                item.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                   'collaborators', 'start_date', 'end_date',
                                   'is_finished'))
                for item in jobs_list
            ]
        }
    )
    db_sess.close()
    return result


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)

    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'id', 'team_leader', 'job', 'work_size',
                'collaborators', 'start_date', 'end_date',
                'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    if 'id' in request.json:
        if db_sess.query(Jobs).get(request.json['id']):
            return make_response(jsonify({'error': 'Id already exists'}), 400)
    jobs = Jobs(
        id=request.json.get('id'),
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        work_size=request.json['work_size']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_jobs(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    fields = ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']
    if not all(key in request.json for key in fields):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']

    db_sess.commit()
    return jsonify({'success': 'OK'})
