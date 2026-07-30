from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    password     = db.Column(db.String(200), nullable=False)
    career_goal  = db.Column(db.String(100), default='')
    interests    = db.Column(db.Text, default='')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    skills       = db.relationship('UserSkill',    backref='user', lazy=True, cascade='all, delete-orphan')
    progress     = db.relationship('UserProgress', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'career_goal': self.career_goal,
            'interests': self.interests
        }


class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name  = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.Integer, default=1)   # 1-5

    def to_dict(self):
        return {'id': self.id, 'skill_name': self.skill_name, 'proficiency': self.proficiency}


class Course(db.Model):
    __tablename__ = 'courses'
    id             = db.Column(db.Integer, primary_key=True)
    title          = db.Column(db.String(200), nullable=False)
    platform       = db.Column(db.String(50),  default='')
    skills_covered = db.Column(db.Text,         default='')
    level          = db.Column(db.String(20),   default='beginner')
    url            = db.Column(db.String(500),  default='')
    rating         = db.Column(db.Float,        default=4.0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'platform': self.platform,
            'skills_covered': self.skills_covered,
            'level': self.level,
            'url': self.url,
            'rating': self.rating
        }


class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    course_id      = db.Column(db.Integer, db.ForeignKey('courses.id'),  nullable=False)
    status         = db.Column(db.String(20), default='not_started')   # not_started / in_progress / done
    completion_pct = db.Column(db.Integer,    default=0)
    updated_at     = db.Column(db.DateTime,   default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship('Course', backref='progress_records', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course_title': self.course.title if self.course else '',
            'platform': self.course.platform if self.course else '',
            'status': self.status,
            'completion_pct': self.completion_pct
        }