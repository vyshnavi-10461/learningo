from flask import Blueprint, request, jsonify
from models import db, User, UserSkill

skills_bp = Blueprint('skills', __name__)


@skills_bp.route('/skills', methods=['POST'])
def save_skills():
    data = request.get_json()
    user_id = data.get('user_id')
    skills  = data.get('skills', [])   # [{"skill_name": "python", "proficiency": 4}, ...]

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # delete old skills and replace
    UserSkill.query.filter_by(user_id=user_id).delete()
    for s in skills:
        skill = UserSkill(
            user_id     = user_id,
            skill_name  = s['skill_name'].lower().strip(),
            proficiency = int(s.get('proficiency', 1))
        )
        db.session.add(skill)

    # also update career goal if provided
    if data.get('career_goal'):
        user.career_goal = data['career_goal']

    db.session.commit()
    return jsonify({'message': f'{len(skills)} skills saved successfully'}), 200


@skills_bp.route('/skills/<int:user_id>', methods=['GET'])
def get_skills(user_id):
    skills = UserSkill.query.filter_by(user_id=user_id).all()
    return jsonify({'skills': [s.to_dict() for s in skills]}), 200