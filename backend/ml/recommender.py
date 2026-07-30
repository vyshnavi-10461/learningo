"""
TF-IDF + Cosine Similarity course recommender.
Falls back to keyword matching when the course list is empty.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def recommend_courses(skill_gaps: list, all_courses: list, top_n: int = 5) -> list:
    """
    Parameters
    ----------
    skill_gaps   : list of str   — missing skills from gap analysis
    all_courses  : list of dicts — Course.to_dict() records
    top_n        : int           — number of courses to return

    Returns
    -------
    list of dicts (top_n course records with an added 'score' field)
    """
    if not all_courses:
        return []

    if not skill_gaps:
        # no gaps → return highest-rated courses
        df = pd.DataFrame(all_courses)
        df = df.sort_values('rating', ascending=False)
        return df.head(top_n).to_dict('records')

    df = pd.DataFrame(all_courses)

    # build TF-IDF matrix on the skills_covered text
    vectorizer   = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['skills_covered'].fillna(''))

    # user query = joined gap skills
    user_query = ' '.join(skill_gaps)
    user_vec   = vectorizer.transform([user_query])

    # cosine similarity between user query and every course
    scores        = cosine_similarity(user_vec, tfidf_matrix).flatten()
    df['score']   = scores

    # sort by score desc, then by rating
    df = df.sort_values(['score', 'rating'], ascending=[False, False])

    top = df.head(top_n).to_dict('records')
    return top