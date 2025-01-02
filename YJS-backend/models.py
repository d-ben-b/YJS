from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BLOB
import hashlib

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, default=0)
    user_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    account_enabled = db.Column(db.Boolean, default=False)
    department_id = db.Column(
        db.Integer, db.ForeignKey("department.department_id"), nullable=False
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.unit_id"), nullable=False)
    department = db.relationship(
        "Department", backref=db.backref("users", lazy="joined")
    )
    unit = db.relationship("Unit", backref=db.backref("users", lazy="joined"))

    def __repr__(self):
        return f"<User {self.user_name}>"


class Account(db.Model):
    __tablename__ = "account"

    account = db.Column(db.String(30), primary_key=True)
    hashed_password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __init__(self, account, hashed_password, user_id, email):
        self.account = account
        self.hashed_password = hashed_password
        self.user_id = user_id
        self.email = email

    def __repr__(self):
        return f"<Account {self.account}>"

    def set_password(self, password):
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hashed_password == hashlib.sha256(password.encode()).hexdigest()


class Department(db.Model):
    __tablename__ = "department"
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(30), nullable=False)

    # 添加 order_by 參數
    units = db.relationship(
        "Unit", backref="department", lazy="joined", order_by="Unit.unit_id.asc()"
    )

    def __repr__(self):
        return f"<Department {self.department_name}>"


class Unit(db.Model):
    __tablename__ = "unit"
    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(30), nullable=False)
    department_id = db.Column(
        db.Integer, db.ForeignKey("department.department_id"), nullable=False
    )

    # 添加 order_by 參數
    workstations = db.relationship(
        "Workstation",
        backref="unit",
        lazy="joined",
        order_by="Workstation.work_station_id.asc()",
    )

    def __repr__(self):
        return f"<Unit {self.unit_name}>"


class Role(db.Model):
    __tablename__ = "role"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), nullable=False)
    role_type = db.Column(db.String(30), nullable=False)

    courses = db.relationship("Course", backref="role", lazy=True)

    def __repr__(self):
        return f"<Role {self.role_name}>"


class Quiz(db.Model):
    __tablename__ = "quizs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    work_item_id = db.Column(db.Integer, nullable=False)
    # 題型: "choice" 或 "question"
    type = db.Column(db.String(50), nullable=False)
    options = db.Column(db.JSON, nullable=True)  # 選項 (選擇題)
    answer = db.Column(db.String(255), nullable=True)  # 答案 (問答題)
    status = db.Column(
        db.String(50), nullable=True, default="不通過"
    )  # 狀態: "通過/採用" "通過/保留" "不通過"
    reason = db.Column(db.String(255), nullable=True)  # 原因

    def __repr__(self):
        return f"<Quiz {self.name}>"


class Training(db.Model):
    __tablename__ = "training"

    training_id = db.Column(db.Integer, primary_key=True)
    training_type_id = db.Column(
        db.Integer, db.ForeignKey("training_type.training_type_id"), nullable=False
    )
    department_id = db.Column(db.Integer, nullable=False)
    unit_id = db.Column(db.Integer, nullable=False)
    work_station_id = db.Column(db.Integer, nullable=False)
    work_item_id = db.Column(
        db.Integer, db.ForeignKey("work_item.work_item_id"), nullable=False
    )

    courses = db.relationship("Course", backref="training", lazy=True)
    training_type = db.relationship("TrainingType", backref="trainings", lazy=True)
    work_item = db.relationship("WorkItem", backref="trainings", lazy=True)


class WorkItem(db.Model):
    __tablename__ = "work_item"
    work_item_id = db.Column(db.Integer, primary_key=True)
    work_item_name = db.Column(db.String(30), nullable=False)
    work_station_id = db.Column(
        db.Integer, db.ForeignKey("workstation.work_station_id"), nullable=False
    )
    work_item_sop = db.Column(db.String(30), nullable=True, comment="SOP/SIP")
    work_item_sop_img = db.Column(BLOB, nullable=True, comment="SOP/SIP圖片")
    work_item_points = db.Column(db.String(300), nullable=True, comment="教學重點")
    work_item_standards = db.Column(
        db.String(300), nullable=True, comment="評量項目與標準"
    )

    images = db.relationship(
        "WorkItemImage", back_populates="work_item", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<WorkItem {self.work_item_name}>"


class WorkItemImage(db.Model):
    __tablename__ = "work_item_image"

    id = db.Column(db.Integer, primary_key=True)
    work_item_id = db.Column(
        db.Integer, db.ForeignKey("work_item.work_item_id"), nullable=False
    )
    image_data = db.Column(db.LargeBinary, nullable=False)
    filename = db.Column(db.String(255), nullable=True, default="Image")

    work_item = db.relationship("WorkItem", back_populates="images")

    def __repr__(self):
        return f"<WorkItemImage {self.id}>"


class Workstation(db.Model):
    __tablename__ = "workstation"

    work_station_id = db.Column(db.Integer, primary_key=True)
    work_station_name = db.Column(db.String(30), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.unit_id"), nullable=False)

    # 添加 order_by 參數
    workitems = db.relationship(
        "WorkItem",
        backref="workstation",
        cascade="all, delete-orphan",
        lazy="joined",
        order_by="WorkItem.work_item_id.asc()",
    )

    def __repr__(self):
        return f"<Workstation {self.work_station_name}>"


class TrainingType(db.Model):
    __tablename__ = "training_type"

    training_type_id = db.Column(db.Integer, primary_key=True)
    training_type_name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<TrainingType {self.training_type_name}>"


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(
        db.Integer, db.ForeignKey("training.training_id"), nullable=False
    )
    course_name = db.Column(db.String(30), nullable=False)
    course_date_start = db.Column(db.Date, nullable=True)
    course_date_end = db.Column(db.Date, nullable=True)
    course_time_start = db.Column(db.Time, nullable=True)
    course_time_end = db.Column(db.Time, nullable=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id"), nullable=True, default=0
    )
    role_id = db.Column(
        db.Integer, db.ForeignKey("role.role_id"), nullable=True, default=0
    )
    work_item_id = db.Column(
        db.Integer, db.ForeignKey("work_item.work_item_id"), nullable=False
    )

    user = db.relationship("User", backref="courses", lazy=True)
    work_item = db.relationship("WorkItem", backref="courses", lazy=True)

    def __repr__(self):
        return f"<Course {self.course_name}>"
