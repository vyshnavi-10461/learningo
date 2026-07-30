from flask import Blueprint, request, jsonify
from models import db, User, UserSkill, Course
from ml.gap_analysis  import analyze_skill_gaps
from ml.recommender   import recommend_courses

recommend_bp = Blueprint('recommend', __name__)


@recommend_bp.route('/recommend', methods=['POST'])
def get_recommendations():
    data    = request.get_json()
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # fetch skills
    user_skills = UserSkill.query.filter_by(user_id=user_id).all()
    skills_list = [{'skill_name': s.skill_name, 'proficiency': s.proficiency} for s in user_skills]

    # skill gap analysis
    gaps = analyze_skill_gaps(skills_list, user.career_goal)

    # fetch all courses from DB
    courses = Course.query.all()
    courses_list = [c.to_dict() for c in courses]

    # ML recommendation
    recommended = recommend_courses(gaps, courses_list)

    return jsonify({
        'gaps': gaps,
        'courses': recommended,
        'career_goal': user.career_goal
    }), 200


@recommend_bp.route('/courses', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    return jsonify({'courses': [c.to_dict() for c in courses]}), 200