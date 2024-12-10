from flask_cors import CORS
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# 初始化 Flask 應用和資料庫
server = Flask(__name__)
CORS(server)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://project_user:password@localhost/mydb'  # 替換成你的 MySQL 設定
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# 定義資料表
class Course(db.Model):
    __tablename__ = 'courses'  # 表格名稱

    course_id = db.Column(db.Integer, primary_key=True)  # 主鍵
    training_id = db.Column(db.Integer, nullable=False)  # 外鍵
    course_name = db.Column(db.String(100), nullable=False)
    course_date_start = db.Column(db.Date, nullable=False)
    course_date_end = db.Column(db.Date, nullable=False)
    course_time_start = db.Column(db.Time, nullable=False)
    course_time_end = db.Column(db.Time, nullable=False)
    course_content = db.Column(db.Text)  # 課程內容
    user_id = db.Column(db.Integer, nullable=False)  # 外鍵（講師ID）

    def __repr__(self):
        return f'<Course {self.course_name}>'

# 定義一個 GET 路由來返回課程資料
@server.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    courses_data = []
    for course in courses:
        courses_data.append({
            'course_id': course.course_id,
            'training_id': course.training_id,
            'course_name': course.course_name,
            'course_date_start': course.course_date_start.isoformat(),
            'course_date_end': course.course_date_end.isoformat(),
            'course_time_start': course.course_time_start.strftime('%H:%M:%S'),
            'course_time_end': course.course_time_end.strftime('%H:%M:%S'),
            'course_content': course.course_content,
            'user_id': course.user_id
        })
    return jsonify(courses_data)

# 啟動應用
if __name__ == '__main__':
    server.run(debug=True)
