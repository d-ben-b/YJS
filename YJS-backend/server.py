"""
This module defines a Flask application with several API routes for managing courses, work items, images, and user accounts.
Blueprints:
- menus_bp: Blueprint for menu-related routes.
Flask Application:
- server: The main Flask application instance.
Configurations:
- SQLALCHEMY_DATABASE_URI: Database connection URI.
- SQLALCHEMY_TRACK_MODIFICATIONS: Disable modification tracking.
- MAX_CONTENT_LENGTH: Maximum upload file size (16MB).
Functions:
- allowed_file(filename): Check if the file extension is allowed.
- format_course(course): Format course data into a dictionary.
API Routes:
- /api/courses [GET]: Get a list of courses or details of a single course.
- /api/all_values [GET]: Get unique values for specified fields.
- /api/courses/<int:course_id> [DELETE]: Delete a specified course.
- /api/courses/<int:course_id> [PUT]: Update a specified course, including file upload handling.
- /api/courses [POST]: Create a new course, including file upload handling.
- /api/work_item_images [GET]: Get images by work item ID.
- /api/work_item_image [GET]: Get a single work item image by ID.
- /api/work_item_image [DELETE]: Delete a single work item image by ID.
- /api/menus [GET]: Get a hierarchical menu structure of departments, units, workstations, and work items.
- /api/toggle_account [POST]: Enable or disable a user account.
- /api/change_password [POST]: Change the password of a user account.
- /api/get_list [GET]: Get a list of users based on role name.
Error Handling:
- Returns JSON error messages and appropriate HTTP status codes for various exceptions.
Initialization:
- Creates database tables if they do not exist when the application starts.
"""
from flask_cors import CORS
from flask import Flask, jsonify, request, make_response,Blueprint
from models import db, Course, Role, WorkItem, TrainingType, User, Account, \
    Department, Unit, WorkItemImage, Workstation, Quiz
import base64

menus_bp = Blueprint('menus', __name__)

# 初始化 Flask 應用和資料庫
server = Flask(__name__)
CORS(server)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@testdb.cjyecqcoe2uq.ap-southeast-2.rds.amazonaws.com/testdb'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 設為 False 以禁用警告
server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上傳檔案大小為16MB
db.init_app(server)

# 定義允許上傳的檔案類型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 格式化課程資料的輔助函數
def format_course(course):
    return {
        'course_id': course.course_id,
        'training_id': course.training_id,
        'course_name': course.course_name,
        'user_id': course.user_id,
        'role_id': course.role_id,
        'role_name': course.role.role_name,
        'role_type': course.role.role_type,
        'work_item_id': course.work_item_id,
        'work_item_name': course.work_item.work_item_name,
        'images': [base64.b64encode(img.image_data).decode('utf-8') for img in course.work_item.images],
        'key_points': course.work_item.work_item_points,
        'evaluation_criteria': course.work_item.work_item_standards,
        'sop_sip': course.work_item.work_item_sop,
        'training_type_name': course.training.training_type.training_type_name,
        'department_name': course.user.department.department_name,
        'unit_name': course.user.unit.unit_name,
        "image_urls": [f"/uploads/{img.filename}" for img in course.work_item.images]
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

        if course_id:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': f'找不到 ID 為 {course_id} 的課程'}), 404
            return jsonify(format_course(course))

        courses = Course.query.all()
        return jsonify([format_course(course) for course in courses])

    except Exception as e:
        # 錯誤處理
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@server.route('/api/all_values', methods=['GET'])
def get_all_unique_values():
    """
    獲取指定字段的唯一值集合（不進行表關聯）。
    請求參數:
    - fields: 用逗號分隔的字段名稱，如 `training_type_name,work_item_name`

    回應:
    - 返回包含唯一值的 JSON 格式
    """
    try:
        fields = request.args.get('fields')
        if not fields:
            return jsonify({'error': '缺少 fields 參數'}), 400

        field_list = fields.split(',')
        valid_fields = {
            "training_type_name": TrainingType.training_type_name,
            "work_item_name": WorkItem.work_item_name,
            "unit_name": Unit.unit_name,
            "department_name": Department.department_name,
            # "work_item_sop_img": WorkItem.work_item_sop_img,  # 如果不需要圖片的唯一值，則可以移除
        }

        # 確認字段合法性
        invalid_fields = [field for field in field_list if field not in valid_fields]
        if invalid_fields:
            return jsonify({'error': f'非法字段: {", ".join(invalid_fields)}'}), 400

        # 查詢每個字段的唯一值
        unique_values = {}
        for field in field_list:
            column = valid_fields[field]
            query = db.session.query(column).distinct()
            unique_values[field] = [value for value, in query.all()]

        return jsonify(unique_values), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@server.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    刪除指定課程。
    """
    try:
        # 獲取課程資料
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': f'找不到 ID 為 {course_id} 的課程'}), 404

        # 刪除課程及相關圖片
        db.session.delete(course)
        db.session.commit()

        return jsonify({'message': '課程刪除成功！'}), 200

    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@server.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    更新指定課程資料，包括檔案上傳處理。
    """
    try:
        # 獲取課程資料
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'error': f'找不到 ID 為 {course_id} 的課程'}), 404

        # 從請求中提取資料
        course_name = request.form.get('course_name')
        training_type_name = request.form.get('training_type_name')
        work_item_name = request.form.get('work_item_name')
        unit_name = request.form.get('unit_name')
        department_name = request.form.get('department_name')
        evaluation_criteria = request.form.get('evaluation_criteria')
        key_points = request.form.get('key_points')
        sop_sip = request.form.get('sop_sip')

        # 更新課程名稱
        if course_name:
            course.course_name = course_name

        # 更新 training_id
        if training_type_name:
            training_type = TrainingType.query.filter_by(training_type_name=training_type_name).first()
            if training_type:
                course.training_id = training_type.training_type_id

        # 更新 WorkItem 的相關欄位
        if work_item_name:
            work_item = WorkItem.query.filter_by(work_item_name=work_item_name).first()
            if work_item:
                course.work_item_id = work_item.work_item_id
                work_item.work_item_points = key_points
                work_item.work_item_standards = evaluation_criteria
                work_item.work_item_sop = sop_sip

                # 處理多張檔案上傳
                if 'uploadedFiles' in request.files:
                    uploaded_files = request.files.getlist('uploadedFiles')
                    print(uploaded_files)
                    # 刪除舊的圖片
                    WorkItemImage.query.filter_by(work_item_id=work_item.work_item_id).delete()
                    # 新增新的圖片
                    for uploaded_file in uploaded_files:
                        if uploaded_file and allowed_file(uploaded_file.filename):
                            image_data = uploaded_file.read()
                            work_item_image = WorkItemImage(work_item=work_item, image_data=image_data)
                            db.session.add(work_item_image)
                        else:
                            return jsonify({'error': '不允許的檔案類型'}), 400

        # 更新其他外鍵欄位
        if unit_name:
            unit = Unit.query.filter_by(unit_name=unit_name).first()
            if unit:
                course.unit_id = unit.unit_id

        if department_name:
            department = Department.query.filter_by(department_name=department_name).first()
            if department:
                course.department_id = department.department_id

        # 保存修改
        db.session.commit()

        return jsonify({'message': '課程更新成功！'}), 200

    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@server.route('/api/courses', methods=['POST'])
def create_course():
    """
    新增課程資料，包括檔案上傳處理。
    """
    try:
        # 從請求中提取資料
        course_name = request.form.get('course_name')
        training_type_name = request.form.get('training_type_name')
        work_item_name = request.form.get('work_item_name')
        unit_name = request.form.get('unit_name')
        department_name = request.form.get('department_name')
        evaluation_criteria = request.form.get('evaluation_criteria')
        key_points = request.form.get('key_points')
        sop_sip = request.form.get('sop_sip')

        # 驗證必要欄位
        if not course_name or not training_type_name or not work_item_name:
            return jsonify({'error': '缺少必要欄位: course_name, training_type_name, 或 work_item'}), 400

        # 創建新的 Course 物件
        new_course = Course(
            course_name=course_name,
            course_date_start=request.form.get('course_date_start'),
            course_date_end=request.form.get('course_date_end'),
            course_time_start=request.form.get('course_time_start'),
            course_time_end=request.form.get('course_time_end'),
        )

        # 設定 training_id
        if training_type_name:
            training_type = TrainingType.query.filter_by(training_type_name=training_type_name).first()
            if training_type:
                new_course.training_id = training_type.training_type_id

        # 設定 work_item_id 並更新相關欄位
        work_item = WorkItem.query.filter_by(work_item_name=work_item_name).first()
        if work_item:
            new_course.work_item_id = work_item.work_item_id
            work_item.work_item_points = key_points
            work_item.work_item_standards = evaluation_criteria
            work_item.work_item_sop = sop_sip

            # 處理多張檔案上傳
            if 'uploadedFiles' in request.files:
                uploaded_files = request.files.getlist('uploadedFiles')
                for uploaded_file in uploaded_files:
                    if uploaded_file and allowed_file(uploaded_file.filename):
                        image_data = uploaded_file.read()
                        work_item_image = WorkItemImage(work_item=work_item, image_data=image_data)
                        db.session.add(work_item_image)
                    else:
                        return jsonify({'error': '不允許的檔案類型'}), 400

        # 設定其他外鍵欄位
        if unit_name:
            unit = Unit.query.filter_by(unit_name=unit_name).first()
            if unit:
                new_course.unit_id = unit.unit_id

        if department_name:
            department = Department.query.filter_by(department_name=department_name).first()
            if department:
                new_course.department_id = department.department_id

        # 保存新課程資料
        db.session.add(new_course)
        db.session.commit()

        return jsonify({'message': '課程新增成功！'}), 201

    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@server.route('/api/work_item_images', methods=['GET'])
def get_work_item_images_by_work_item_id():
    work_item_id = request.args.get('work_item_id', type=int)
    if not work_item_id:
        return jsonify({'error': '缺少 work_item_id 參數'}), 400

    # 找出對應的全部圖片記錄
    imgs = WorkItemImage.query.filter_by(work_item_id=work_item_id).all()
    print(imgs)
    if not imgs:
        return jsonify({'images': []}), 200

    # 建立圖片URL的列表
    # 假設後端提供每張圖片一個URL，如: /api/work_item_image?id=xxx
    image_urls = [f"{request.host_url}api/work_item_image?id={img.id}" for img in imgs]

    return jsonify({'images': image_urls}), 200

@server.route('/api/work_item_image', methods=['GET'])
def get_work_item_image():
    image_id = request.args.get('id', type=int)
    if not image_id:
        return jsonify({'error': '缺少 id 參數'}), 400

    img = WorkItemImage.query.get(image_id)
    if not img or not img.image_data:
        return jsonify({'error': '圖片未找到'}), 404

    # 假設圖片為 PNG 格式，若有需要可根據實際圖片格式調整 Content-Type
    response = make_response(img.image_data)
    response.headers.set('Content-Type', 'image/png')
    return response

#定義刪除圖片的API路由
@server.route('/api/work_item_image', methods=['DELETE'])
def delete_work_item_image():
    image_id = request.args.get('id', type=int)
    if not image_id:
        return jsonify({'error': '缺少 id 參數'}), 400

    img = WorkItemImage.query.get(image_id)
    if not img:
        return jsonify({'error': '圖片未找到'}), 404

    db.session.delete(img)
    db.session.commit()
    return jsonify({'message': '圖片刪除成功'}), 200

# 
@server.route('/api/menus', methods=['GET'])
def get_menus():
    try:
        # 使用 joinedload 進行關聯預加載，減少查詢次數
        departments = Department.query.options(
            db.joinedload(Department.units)
            .joinedload(Unit.workstations)
            .joinedload(Workstation.workitems)
        ).order_by(Department.department_id.asc()).all()

        def build_dept_dict(dept):
            return {
                "id": dept.department_id,
                "title": dept.department_name,
                "route": f"/departments/{dept.department_id}",
                "children": [build_unit_dict(unit, dept.department_id) for unit in dept.units]
            }

        def build_unit_dict(unit, dept_id):
            return {
                "id": unit.unit_id,
                "title": unit.unit_name,
                "route": f"/departments/{dept_id}/units/{unit.unit_id}",
                "children": [build_ws_dict(ws, dept_id, unit.unit_id) for ws in unit.workstations]
            }

        def build_ws_dict(ws, dept_id, unit_id):
            return {
                "id": ws.work_station_id,
                "title": ws.work_station_name,
                "route": f"/departments/{dept_id}/units/{unit_id}/workstations/{ws.work_station_id}",
                "children": [build_wi_dict(wi, dept_id, unit_id, ws.work_station_id) for wi in ws.workitems]
            }
            
        def build_wi_dict(wi, dept_id, unit_id, ws_id):
            return {
                "id": wi.work_item_id,
                "title": wi.work_item_name,
                "route": f"/departments/{dept_id}/units/{unit_id}/workstations/{ws_id}/workitems/{wi.work_item_id}",
                "children": []
            }

        menu_tree = [build_dept_dict(dept) for dept in departments]

        return jsonify(menu_tree), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "伺服器錯誤"}), 500

@server.route('/api/work_items/<int:work_item_id>', methods=['GET'])
def get_work_item(work_item_id):
    """
    獲取指定工作項目的詳細數據，包括 SOP、教學重點、評量標準以及圖片。
    """
    try:
        # 獲取工作項目數據
        work_item = WorkItem.query.get(work_item_id)
        if not work_item:
            return jsonify({'error': f'找不到 ID 為 {work_item_id} 的工作項目'}), 404

        # 格式化工作項目數據
        work_item_data = {
            'work_item_id': work_item.work_item_id,
            'work_item_name': work_item.work_item_name,
            'sop_sip': work_item.work_item_sop or '',
            'key_points': work_item.work_item_points or '',
            'evaluation_criteria': work_item.work_item_standards or '',
            'images': [base64.b64encode(img.image_data).decode('utf-8') for img in work_item.images]
        }

        return jsonify(work_item_data), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@server.route("/api/quiz", methods=["POST"])
def create_quiz():
    """
    創建 Quiz，如果已存在則返回已存在的 Quiz。
    """
    try:
        work_item_id = request.json.get("work_item_id")
        quiz_type = request.json.get("type", "choice")  # 默認題型為選擇題
        if not work_item_id:
            return jsonify({"error": "缺少 work_item_id"}), 400

        # 檢查是否已有 Quiz
        quiz = Quiz.query.filter_by(work_item_id=work_item_id).first()
        if quiz:
            return jsonify({"message": "Quiz 已存在", "quiz_id": quiz.id}), 200

        # 創建新 Quiz
        quiz = Quiz(
            name=f"Quiz for work_item {work_item_id}",
            work_item_id=work_item_id,
            type=quiz_type,
            options=[] if quiz_type == "choice" else None,
            answer="" if quiz_type == "question" else None,
        )
        db.session.add(quiz)
        db.session.commit()

        return jsonify({"message": "Quiz 創建成功", "quiz_id": quiz.id, "type": quiz.type}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@server.route("/api/quiz/<int:quiz_id>", methods=["PUT"])
def update_quiz(quiz_id):
    """
    更新 Quiz 的數據，支持選擇題和問答題。
    """
    try:
        data = request.json
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"error": "Quiz 不存在"}), 404

        if quiz.type == "choice":
            options = data.get("options", [])
            if not options:
                return jsonify({"error": "缺少選項數據"}), 400
            quiz.options = options
        elif quiz.type == "question":
            answer = data.get("answer", "")
            quiz.answer = answer

        db.session.commit()
        return jsonify({"message": f"Quiz 更新成功 ({quiz.type})"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@server.route('/api/quizzes', methods=['GET', 'POST'])
def manage_quizzes():
    if request.method == 'GET':
        # 現有的獲取 Quizzes 的邏輯
        work_item_id = request.args.get('work_item_id', type=int)
        try:
            if work_item_id:
                quizzes = Quiz.query.filter_by(work_item_id=work_item_id).all()
            else:
                quizzes = Quiz.query.all()

            return jsonify([{
                "id": quiz.id,
                "name": quiz.name,
                "type": quiz.type,
                "options": quiz.options if quiz.type == "choice" else None,
                "answer": quiz.answer if quiz.type == "question" else None,
            } for quiz in quizzes])
        except Exception as e:
            print("Error:", str(e))
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        # 添加 Quiz 的邏輯
        data = request.json
        try:
            work_item_id = data.get('work_item_id')
            name = data.get('name', f"Quiz for work_item {work_item_id}")
            quiz_type = data.get('type', 'choice')
            options = data.get('options', []) if quiz_type == 'choice' else None
            answer = data.get('answer', '') if quiz_type == 'question' else None

            if not work_item_id:
                return jsonify({"error": "缺少 work_item_id"}), 400

            new_quiz = Quiz(
                name=name,
                work_item_id=work_item_id,
                type=quiz_type,
                options=options,
                answer=answer
            )
            print(new_quiz)
            db.session.add(new_quiz)
            db.session.commit()

            return jsonify({"message": "Quiz 創建成功", "quiz_id": new_quiz.id}), 201
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return jsonify({"error": str(e)}), 500




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
    action = data.get('action')  # 'enable' 或 'disable'

    if not user_id or not action:
        return jsonify({'message': '缺少使用者 ID 或操作'}), 400

    user = User.query.get(user_id)
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
    account_name = data.get('account')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not account_name or not current_password or not new_password:
        return jsonify({'message': '缺少帳號、舊密碼或新密碼'}), 400

    account = Account.query.get(account_name)
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
    role_name = request.args.get('role_name')  # 取得 role_name 參數

    if not role_name:
        return jsonify({'message': '缺少角色名稱參數'}), 400

    # 檢查 role_name 是否存在
    role = Role.query.filter_by(role_name=role_name).first()
    if not role:
        return jsonify({'message': '角色名稱不存在'}), 404

    # 查詢所有為 role_name 的 user
    users = User.query.filter(User.role_id == role.role_id).all()

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
