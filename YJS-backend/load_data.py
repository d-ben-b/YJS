import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from server import server, db, Course  # 引入 server 和 Course 類別

DEBUG = False  # 控制是否進行資料表刪除重建（測試用）

# 獲取資料庫 URI
db_uri = server.config['SQLALCHEMY_DATABASE_URI']
database_name = db_uri.rsplit('/', 1)[-1]  # 提取資料庫名稱


# 創建資料庫（如果不存在）
def create_database():
    engine = create_engine(db_uri.rsplit('/', 1)[0])  # 去掉資料庫名稱
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name};"))
        print(f"Database '{database_name}' created successfully.")


# 初始化資料庫（刪除舊資料表並創建新資料表）
def initialize_database():
    with server.app_context():
        if DEBUG:
            db.drop_all()  # 僅在測試環境中刪除舊資料表
            print("Dropped all existing tables.")
        db.create_all()  # 創建新資料表
        print("Database and tables initialized successfully.")


# 從 JSON 檔案載入課程資料
def load_courses_from_json():
    with open('./demo_courses.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)

    with server.app_context():
        for course_data in courses:
            # 檢查資料是否已存在
            existing_course = Course.query.filter_by(
                course_id=course_data['course_id']).first()
            if not existing_course:
                # 如果資料不存在，新增資料
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

        # 提交資料到資料庫
        db.session.commit()
        print("Data loaded into the database.")


if __name__ == '__main__':
    # 1. 創建資料庫
    if DEBUG:
        create_database()
    # 2. 初始化資料庫（建立資料表）
    initialize_database()
    # 3. 載入資料
    load_courses_from_json()
