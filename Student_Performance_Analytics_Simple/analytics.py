import pandas as pd
import numpy as np

from models import Grade


def get_grade_dataframe():
    grades = Grade.query.all()

    rows = []

    for grade in grades:
        rows.append({
            "student": grade.student.name,
            "student_email": grade.student.email,
            "course": grade.course.name,
            "course_code": grade.course.code,
            "score": grade.score,
            "date": grade.date
        })

    if not rows:
        return pd.DataFrame(
            columns=[
                "student", "student_email", "course",
                "course_code", "score", "date"
            ]
        )

    return pd.DataFrame(rows)


def get_analytics(course_code=None, student_email=None):
    df = get_grade_dataframe()

    if course_code:
        df = df[df["course_code"] == course_code]

    if student_email:
        df = df[df["student_email"] == student_email]

    if df.empty:
        return {
            "data": df,
            "average": 0,
            "median": 0,
            "std": 0,
            "course_average": pd.DataFrame(),
            "ranking": pd.DataFrame()
        }

    average = float(np.mean(df["score"]))
    median = float(np.median(df["score"]))
    std = float(np.std(df["score"]))

    course_average = (
        df.groupby(["course", "course_code"])["score"]
        .mean()
        .reset_index(name="average_score")
    )

    ranking = df.copy()
    ranking["rank"] = (
        ranking.groupby("course")["score"]
        .rank(method="dense", ascending=False)
    )

    ranking = ranking.sort_values(["course", "rank"])

    return {
        "data": df,
        "average": round(average, 2),
        "median": round(median, 2),
        "std": round(std, 2),
        "course_average": course_average,
        "ranking": ranking
    }
