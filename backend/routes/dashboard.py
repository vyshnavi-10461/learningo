from flask import Blueprint, jsonify
from models import User, UserSkill, UserProgress
from ml.gap_analysis import analyze_skill_gaps
from ml.recommender  import recommend_courses
from models import Course

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard/<int:user_id>', methods=['GET'])
def get_dashboard(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # skills
    user_skills = UserSkill.query.filter_by(user_id=user_id).all()
    skills_list = [{'skill_name': s.skill_name, 'proficiency': s.proficiency} for s in user_skills]

    # gaps + recommendations
    gaps        = analyze_skill_gaps(skills_list, user.career_goal)
    courses     = [c.to_dict() for c in Course.query.all()]
    recommended = recommend_courses(gaps, courses)

    # progress stats
    progress_records = UserProgress.query.filter_by(user_id=user_id).all()
    total       = len(progress_records)
    done        = sum(1 for r in progress_records if r.status == 'done')
    in_progress = sum(1 for r in progress_records if r.status == 'in_progress')
    not_started = total - done - in_progress

    return jsonify({
        'user':          user.to_dict(),
        'skills':        skills_list,
        'gaps':          gaps,
        'courses':       recommended,
        'progress_stats': {
            'total':       total,
            'done':        done,
            'in_progress': in_progress,
            'not_started': not_started
        }
    }), 200