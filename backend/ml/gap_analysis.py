"""
Compares a user's current skills with the required skills
for their chosen career goal and returns the missing ones.
"""

CAREER_SKILL_MAP = {
    'data_scientist': [
        'python', 'machine learning', 'statistics', 'sql',
        'data visualization', 'pandas', 'numpy', 'deep learning'
    ],
    'web_developer': [
        'html', 'css', 'javascript', 'react',
        'nodejs', 'sql', 'git', 'rest api'
    ],
    'ai_engineer': [
        'python', 'deep learning', 'nlp', 'pytorch',
        'tensorflow', 'machine learning', 'mathematics', 'cloud'
    ],
    'mobile_developer': [
        'java', 'kotlin', 'swift', 'react native',
        'flutter', 'sql', 'git', 'rest api'
    ],
    'cybersecurity': [
        'networking', 'linux', 'python', 'cryptography',
        'ethical hacking', 'sql', 'cloud security', 'risk management'
    ],
    'cloud_engineer': [
        'aws', 'azure', 'linux', 'docker',
        'kubernetes', 'python', 'networking', 'terraform'
    ],
    'fullstack_developer': [
        'html', 'css', 'javascript', 'react',
        'python', 'sql', 'rest api', 'git', 'docker'
    ],
}


def analyze_skill_gaps(user_skills: list, career_goal: str) -> list:
    """
    Parameters
    ----------
    user_skills : list of dicts  [{'skill_name': 'python', 'proficiency': 4}, ...]
    career_goal : str            e.g. 'data_scientist'

    Returns
    -------
    list of str  — skills the user is missing for their career goal
    """
    goal_key = career_goal.lower().replace(' ', '_').replace('-', '_')
    required = CAREER_SKILL_MAP.get(goal_key, [])

    if not required:
        # unknown career goal → return empty list (no gap analysis possible)
        return []

    current = {s['skill_name'].lower().strip() for s in user_skills}
    gaps    = [skill for skill in required if skill not in current]
    return gaps