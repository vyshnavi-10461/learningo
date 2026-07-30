from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
import pandas as pd
import os

from routes.auth       import auth_bp
from routes.skills     import skills_bp
from routes.recommend  import recommend_bp
from routes.progress   import progress_bp
from routes.dashboard  import dashboard_bp

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    app.config.from_object(Config)

    CORS(app)
    JWTManager(app)
    db.init_app(app)

    app.register_blueprint(auth_bp,      url_prefix='/api')
    app.register_blueprint(skills_bp,    url_prefix='/api')
    app.register_blueprint(recommend_bp, url_prefix='/api')
    app.register_blueprint(progress_bp,  url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/skills')
    def skills():
        return render_template('skills.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/progress')
    def progress():
        return render_template('progress.html')

    with app.app_context():
        db.create_all()
        print("✅ Database tables created.")

        from models import Course

        if Course.query.count() == 0:
            csv_path = os.path.join(os.path.dirname(__file__), 'data', 'courses.csv')
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                for _, row in df.iterrows():
                    course = Course(
                        title          = row['title'],
                        platform       = row['platform'],
                        skills_covered = row['skills_covered'],
                        level          = row['level'],
                        url            = row['url'],
                        rating         = float(row['rating'])
                    )
                    db.session.add(course)
                db.session.commit()
                print(f"✅ Auto-seeded {len(df)} courses.")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)