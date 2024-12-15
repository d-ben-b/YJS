from flask_cors import CORS
from flask import Flask, jsonify, request  
from flask_sqlalchemy import SQLAlchemy
from models import db, Course, Role, Training, WorkItem, TrainingType, User,Department,Unit

# 初始化 Flask 應用和資料庫
server = Flask(__name__)
CORS(server)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@testdb.cjyecqcoe2uq.ap-southeast-2.rds.amazonaws.com/testdb'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(server)

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
        'training_type_name': course.training_type_name,
        'department_name': course.department_name,
        'unit_name': course.unit_name
    }


@server.route('/api/courses', methods=['GET'])
def get_courses():
    """
    獲取課程列表或單個課程詳情。
    
    請求參數:
    - course_id: 可選，若提供則返回該課程的詳細資訊。

    回應:
    - 成功: 返回課程列表或單個課程的 JSON 資料。
    - 失敗: 返回錯誤資訊。
    """
    try:
        course_id = request.args.get('course_id')

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
            TrainingType.training_type_name,
            Department.department_name,
            Unit.unit_name
        ).join(Role, Course.role_id == Role.role_id) \
         .join(Training, Course.training_id == Training.training_id) \
         .join(WorkItem, Training.work_item_id == WorkItem.work_item_id) \
         .join(TrainingType, Training.training_type_id == TrainingType.training_type_id) \
         .join(User, Course.user_id == User.user_id) \
         .join(Department, User.department_id == Department.department_id) \
         .join(Unit, User.unit_id == Unit.unit_id)

        # 如果有 course_id，返回單個課程詳情
        if course_id:
            course = query.filter(Course.course_id == course_id).first()
            if not course:
                return jsonify({'error': f'Course with id {course_id} not found'}), 404
            return jsonify(format_course(course))

        # 如果沒有 course_id，返回所有課程
        courses = query.all()
        return jsonify([format_course(course) for course in courses])

    except Exception as e:
        # 錯誤處理
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

# 啟動應用
if __name__ == '__main__':
    with server.app_context():
        db.create_all()  # 創建資料表
    server.run(debug=True)

