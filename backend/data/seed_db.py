"""
Run this ONCE to load courses.csv into the database.
  cd backend
  python data/seed_db.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from app    import create_app
from models import db, Course

app = create_app()

with app.app_context():
    db.create_all()

    # clear existing courses
    Course.query.delete()
    db.session.commit()

    csv_path = os.path.join(os.path.dirname(__file__), 'courses.csv')
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
    print(f"✅ Seeded {len(df)} courses into database.")