import json
from flask_sqlalchemy import SQLAlchemy
from server import server, db, Course  # 引入 app 和 db 以及 Course 類別

# 讀取 demo 資料並存入資料庫


def load_courses_from_json():
    with open('./demo_courses.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)

    for course_data in courses:
        # 將每一筆資料寫入資料庫
        course = Course(
            course_id=course_data['course_id'],
            training_id=course_data['training_id'],
            course_name=course_data['course_name'],
            course_date_start=course_data['course_date_start'],
            course_date_end=course_data['course_date_end'],
            course_time_start=course_data['course_time_start'],
            course_time_end=course_data['course_time_end'],
            course_content=course_data['course_content'],
            user_id=course_data['user_id']
        )
        db.session.add(course)

    # 提交到資料庫
    db.session.commit()


if __name__ == '__main__':
    with server.app_context():
        load_courses_from_json()
        print("Data loaded into the database.")
