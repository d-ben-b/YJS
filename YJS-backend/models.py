from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BLOB
import hashlib

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True,default=0)
    user_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    account_enabled = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.role_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.department_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey(
        'unit.unit_id'), nullable=False)
    department = db.relationship('Department', backref=db.backref(
        'user', lazy='joined'))   # 指向 Department class
    unit = db.relationship('Unit', backref=db.backref(
        'user', lazy='joined'))   # 指向 Unit class

    def __repr__(self):
        return f'<User {self.user_name}>'


class Account(db.Model):
    __tablename__ = 'account'

    account = db.Column(db.String(30), primary_key=True)
    hashed_password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)

    def __init__(self, account, hashed_password, user_id, email):
        self.account = account
        self.hashed_password = hashed_password
        self.user_id = user_id
        self.email = email

    def __repr__(self):
        return f'<Account {self.account}>'

    def set_password(self, password):
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hashed_password == hashlib.sha256(password.encode()).hexdigest()


class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<Department {self.department_name}>'


class Unit(db.Model):
    __tablename__ = 'unit'
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(30), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.department_id'), nullable=False)

    def __repr__(self):
        return f'<Unit {self.unit_name}>'

# 定義 Role 表


class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), nullable=False)
    role_type = db.Column(db.String(30), nullable=False)

    users = db.relationship('User', backref='role')
    courses = db.relationship('Course', backref='role', lazy=True)

    def __repr__(self):
        return f'<Role {self.role_name}>'

# 定義 Training 表


class Training(db.Model):
    __tablename__ = 'training'

    training_id = db.Column(db.Integer, primary_key=True)
    training_type_id = db.Column(db.Integer, db.ForeignKey(
        'training_type.training_type_id'), nullable=False)
    department_id = db.Column(db.Integer, nullable=False)
    unit_id = db.Column(db.Integer, nullable=False)
    work_station_id = db.Column(db.Integer, nullable=False)
    work_item_id = db.Column(db.Integer, db.ForeignKey(
        'work_item.work_item_id'), nullable=False)

    courses = db.relationship('Course', backref='training', lazy=True)
    training_type = db.relationship(
        'TrainingType', backref='trainings', lazy=True)
    work_item = db.relationship('WorkItem', backref='trainings', lazy=True)
    

# 定義 WorkItem 表


class WorkItem(db.Model):
    __tablename__ = 'work_item'
    work_item_id = db.Column(db.Integer, primary_key=True)
    work_item_name = db.Column(db.String(30), nullable=False)
    work_station_id = db.Column(db.Integer, nullable=False)
    work_item_sop = db.Column(db.String(30), nullable=True, comment="SOP/SIP")
    work_item_sop_img = db.Column(BLOB, nullable=True, comment="SOP/SIP圖片")
    work_item_points = db.Column(db.String(300), nullable=True, comment="教學重點")
    work_item_standards = db.Column(
        db.String(300), nullable=True, comment="評量項目與標準")

    # 新增與 WorkItemImage 的關聯
    images = db.relationship(
        'WorkItemImage', back_populates='work_item', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<WorkItem {self.work_item_name}>'


class WorkItemImage(db.Model):
    __tablename__ = 'work_item_image'
    id = db.Column(db.Integer, primary_key=True)
    work_item_id = db.Column(db.Integer, db.ForeignKey(
        'work_item.work_item_id'), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)
    filename = db.Column(db.String(255), nullable=True, default='Image')

    # 回到 WorkItem 表的關聯
    work_item = db.relationship('WorkItem', back_populates='images')

    def __repr__(self):
        return f'<WorkItemImage {self.id}>'



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
    training_id = db.Column(db.Integer, db.ForeignKey(
        'training.training_id'), nullable=False)
    course_name = db.Column(db.String(30), nullable=False)
    course_date_start = db.Column(db.Date, nullable=True)
    course_date_end = db.Column(db.Date, nullable=True)
    course_time_start = db.Column(db.Time, nullable=True)
    course_time_end = db.Column(db.Time, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=True, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.role_id'), nullable=True, default=0)
    work_item_id = db.Column(db.Integer, db.ForeignKey(
        'work_item.work_item_id'), nullable=False)

    # 新增 relationship
    user = db.relationship('User', backref='courses', lazy=True)
    work_item = db.relationship('WorkItem', backref='courses', lazy=True)
