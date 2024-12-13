from flask_cors import CORS
from flask import Flask, jsonify, request  
from flask_sqlalchemy import SQLAlchemy

# 初始化 Flask 應用和資料庫
server = Flask(__name__)
CORS(server)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@testdb.cjyecqcoe2uq.ap-southeast-2.rds.amazonaws.com/testdb'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(server)

# 定義 Role 表
class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), nullable=False)
    role_type = db.Column(db.String(30), nullable=False)

    courses = db.relationship('Course', backref='role', lazy=True)

    def __repr__(self):
        return f'<Role {self.role_name}>'

# 定義 Training 表
class Training(db.Model):
    __tablename__ = 'training'

    training_id = db.Column(db.Integer, primary_key=True)
    training_type_id = db.Column(db.Integer, db.ForeignKey('training_type.training_type_id'), nullable=False)
    department_id = db.Column(db.Integer, nullable=False)
    unit_id = db.Column(db.Integer, nullable=False)
    work_station_id = db.Column(db.Integer, nullable=False)
    work_item_id = db.Column(db.Integer,db.ForeignKey('work_item.work_item_id') ,nullable=False)

    courses = db.relationship('Course', backref='training', lazy=True)

    def __repr__(self):
        return f'<Training {self.training_id}>'

# 定義 WorkItem 表
class WorkItem(db.Model):
    __tablename__ = 'work_item'
    work_item_id = db.Column(db.Integer, primary_key=True)
    work_item_name = db.Column(db.String(30), nullable=False)
    work_station_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<WorkItem {self.work_item_name}>'
    
# 定義 TrainingType 表
class TrainingType(db.Model):
    __tablename__ = 'training_type'
    training_type_id = db.Column(db.Integer, primary_key=True)
    training_type_name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<TrainingType {self.training_type_name}>'
    
# 定義 Course 表
class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey('training.training_id'), nullable=False)
    course_name = db.Column(db.String(30), nullable=False)
    course_date_start = db.Column(db.Date, nullable=False)
    course_date_end = db.Column(db.Date, nullable=False)
    course_time_start = db.Column(db.Time, nullable=False)
    course_time_end = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)

    def __repr__(self):
        return f'<Course {self.course_name}>'

# 格式化課程資料的輔助函數
def format_course(course):
    return {
        'course_id': course.course_id,
        'training_id': course.training_id,
        'course_name': course.course_name,
        'course_date_start': course.course_date_start.isoformat(),
        'course_date_end': course.course_date_end.isoformat(),
        'course_time_start': course.course_time_start.strftime('%H:%M:%S'),
        'course_time_end': course.course_time_end.strftime('%H:%M:%S'),
        'user_id': course.user_id,
        'role_id': course.role_id,
        'role_name': course.role_name,
        'role_type': course.role_type,
        'work_item_id': course.work_item_id,
        'work_item_name': course.work_item_name,
        'training_type_name': course.training_type_name
    }


@server.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        # 獲取查詢參數中的 course_id
        course_id = request.args.get('course_id', None)

        # 構建查詢
        query = db.session.query(
            Course.course_id,
            Course.training_id,
            Course.course_name,
            Course.course_date_start,
            Course.course_date_end,
            Course.course_time_start,
            Course.course_time_end,
            Course.user_id,
            Role.role_id,
            Role.role_name,
            Role.role_type,
            Training.work_item_id,
            WorkItem.work_item_name,
            TrainingType.training_type_name
        ).join(Role, Course.role_id == Role.role_id) \
         .join(Training, Course.training_id == Training.training_id) \
         .join(WorkItem, Training.work_item_id == WorkItem.work_item_id) \
         .join(TrainingType, Training.training_type_id == TrainingType.training_type_id)

        # 如果有 course_id，過濾特定課程
        if course_id:
            course = query.filter(Course.course_id == course_id).first()
            if not course:
                return jsonify({'error': f'Course with id {course_id} not found'}), 404
            # 單一課程格式化
            return jsonify({
                'course_id': course.course_id,
                'training_id': course.training_id,
                'course_name': course.course_name,
                'course_date_start': course.course_date_start.isoformat(),
                'course_date_end': course.course_date_end.isoformat(),
                'course_time_start': course.course_time_start.strftime('%H:%M:%S'),
                'course_time_end': course.course_time_end.strftime('%H:%M:%S'),
                'user_id': course.user_id,
                'role_id': course.role_id,
                'role_name': course.role_name,
                'role_type': course.role_type,
                'work_item_id': course.work_item_id,
                'work_item_name': course.work_item_name,
                'training_type_name': course.training_type_name
            })

        # 如果沒有 course_id，返回所有課程
        courses = query.all()
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
                'user_id': course.user_id,
                'role_id': course.role_id,
                'role_name': course.role_name,
                'role_type': course.role_type,
                'work_item_id': course.work_item_id,
                'work_item_name': course.work_item_name,
                'training_type_name': course.training_type_name
            })

        return jsonify(courses_data)
    except Exception as e:
        # 打印錯誤日誌
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

# 啟動應用
if __name__ == '__main__':
    with server.app_context():
        db.create_all()  # 創建資料表
    server.run(debug=True)

