from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

# ── route blueprints ──────────────────────────────────────────────────────────
from routes.auth       import auth_bp
from routes.skills     import skills_bp
from routes.recommend  import recommend_bp
from routes.progress   import progress_bp
from routes.dashboard  import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    JWTManager(app)
    db.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp,      url_prefix='/api')
    app.register_blueprint(skills_bp,    url_prefix='/api')
    app.register_blueprint(recommend_bp, url_prefix='/api')
    app.register_blueprint(progress_bp,  url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')

    # create tables on first run
    with app.app_context():
      db.create_all()
      print("✅ Database tables created.")
    
      from models import Course
      import pandas as pd
      import os
    
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

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)