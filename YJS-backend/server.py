from flask_cors import CORS
from flask import Flask, jsonify, request
from models import db, Course, Role, Training, WorkItem, TrainingType, User, Account, Department, Unit

# 初始化 Flask 應用和資料庫
server = Flask(__name__)
CORS(server)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@testdb.cjyecqcoe2uq.ap-southeast-2.rds.amazonaws.com/testdb'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(server)

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

# 定義 API 路由


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

@server.route('/api/toggle_account', methods=['POST'])
def toggle_account():
    """
    啟用或停用使用者帳號。

    請求資料:
    - user_id: 使用者的 ID
    - action: 'enable' 或 'disable'，表示要啟用或停用帳號

    回應:
    - 成功: 返回包含訊息的 JSON
    - 失敗: 返回包含錯誤訊息的 JSON
    """
    data = request.get_json()
    user_id = data.get('user_id')
    action = data.get('action') # 'enable' 或 'disable'

    if not user_id or not action:
        return jsonify({'message': '缺少使用者 ID 或操作'}), 400

    #user = User.query.get(user_id)
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({'message': '找不到使用者'}), 404
    
    if action == 'enable':
        user.account_enabled = True
        message = '帳號已啟用'
    elif action == 'disable':
        user.account_enabled = False
        message = '帳號已停用'
    else:
        return jsonify({'message': '未知操作'}), 400
    
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'message': '更新失敗', 'error': str(e)}), 500
    return jsonify({'message': message}), 200

@server.route('/api/change_password', methods=['POST'])
def change_password():
    """
    更改使用者帳號的密碼。

    請求資料:
    - account: 帳號名稱
    - current_password: 當前密碼
    - new_password: 新密碼

    回應:
    - 成功: 返回包含訊息的 JSON
    - 失敗: 返回包含錯誤訊息的 JSON
    """
    data = request.get_json()
    account = data.get('account')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not account or not current_password or not new_password:
        return jsonify({'message': '缺少帳號、舊密碼或新密碼'}), 400

    account = db.session.get(Account, account)
    if account is None:
        return jsonify({'message': '找不到帳號'}), 404  # 登入中理論上不應該出現此錯誤

    if not account.check_password(current_password):
        return jsonify({'message': '密碼錯誤'}), 403

    account.set_password(new_password)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'message': '更新失敗', 'error': str(e)}), 500
    return jsonify({'message': '密碼已變更'}), 200

@server.route('/api/get_list', methods=['GET'])
def get_list():
    """
    根據角色名稱獲取使用者列表。

    請求參數:
    - role_name: 角色名稱

    回應:
    - 成功: 返回包含使用者列表的 JSON
    - 失敗: 返回包含錯誤訊息的 JSON
    """
    role_name = request.args.get('role_name')   # 取得 role_name 參數

    if not role_name:
        return jsonify({'message': '缺少角色名稱參數'}), 400

    # 檢查 role_name 是否存在
    role = db.session.query(Role).filter_by(role_name=role_name).first()
    if not role:
        return jsonify({'message': '角色名稱不存在'}), 404

    # 查詢所有為 role_name 的 user
    users = db.session.query(User).join(Role).filter(Role.role_name == role_name).all()

    # 將查詢結果轉為 dict
    users_list = [
        {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'gender': user.gender,
            'country': user.country,
            'department_name': user.department.department_name if user.department else None,
            'unit_name': user.unit.unit_name if user.unit else None,
            'account_enabled': user.account_enabled
        } 
        for user in users
    ]

    return jsonify(users_list), 200

# 啟動應用
if __name__ == '__main__':
    with server.app_context():
        db.create_all()  # 創建資料表
    server.run(debug=True)

