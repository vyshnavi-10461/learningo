from flask import Blueprint, request, jsonify
from models import db, UserProgress, Course
from datetime import datetime

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/progress/<int:user_id>', methods=['GET'])
def get_progress(user_id):
    records = UserProgress.query.filter_by(user_id=user_id).all()
    return jsonify({'progress': [r.to_dict() for r in records]}), 200


@progress_bp.route('/progress/update', methods=['PUT'])
def update_progress():
    data      = request.get_json()
    user_id   = data.get('user_id')
    course_id = data.get('course_id')
    status    = data.get('status', 'not_started')
    pct       = int(data.get('completion_pct', 0))

    # auto-set pct based on status
    if status == 'done':
        pct = 100
    elif status == 'not_started':
        pct = 0

    record = UserProgress.query.filter_by(user_id=user_id, course_id=course_id).first()
    if record:
        record.status         = status
        record.completion_pct = pct
        record.updated_at     = datetime.utcnow()
    else:
        record = UserProgress(
            user_id        = user_id,
            course_id      = course_id,
            status         = status,
            completion_pct = pct
        )
        db.session.add(record)

    db.session.commit()
    return jsonify({'message': 'Progress updated', 'progress': record.to_dict()}), 200