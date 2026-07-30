"""
Run this once to fix broken course URLs.
  cd backend
  python fix_urls.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app    import create_app
from models import db, Course

FIXES = {
    'Data Science with Python':          'https://www.edx.org/learn/python/mit-introduction-to-computational-thinking-and-data-science',
    'Full Stack Web Development':        'https://www.edx.org/learn/web-development',
    'Statistics for Data Science':       'https://www.edx.org/learn/statistics',
    'Pandas and NumPy for Data Analysis':'https://www.udemy.com/course/data-analysis-with-pandas/',
    'Computer Vision with OpenCV':       'https://www.udemy.com/course/python-opencv-numpy-guide/',
}

app = create_app()
with app.app_context():
    fixed = 0
    for title, new_url in FIXES.items():
        course = Course.query.filter_by(title=title).first()
        if course:
            course.url = new_url
            fixed += 1
            print(f"✅ Fixed: {title}")
        else:
            print(f"⚠️  Not found: {title}")
    db.session.commit()
    print(f"\n✅ Done — fixed {fixed} course URLs.")