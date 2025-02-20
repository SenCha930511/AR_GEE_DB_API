from . import db

DB_NAME = "ar_gee_teaching"

class Answers(db.Model):
    """
    Answers 資料模型

    此模型定義了答案資料表的結構，包含以下欄位：
    - answer_id: 唯一識別符 (主鍵)
    - student_id: 學生 ID (Text)
    - question_id: 題目 ID (Text)
    - is_correct: 答題是否正確 (Boolean)
    - response_time: 回答所花費的時間 (Time)
    - test_date: 測試日期 (DateTime)
    - incorrect_attempts: 答錯次數 (Integer)
    """
    __bind_key__ = DB_NAME
    __tablename__ = 'answers'

    answer_id = db.Column(db.String(255), primary_key=True)
    student_id = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    response_time = db.Column(db.Time, nullable=False)
    test_date = db.Column(db.DateTime, nullable=False)
    incorrect_attempts = db.Column(db.Integer, nullable=False)


class Questions(db.Model):
    """
    Questions 資料模型

    此模型定義了問題資料表的結構，包含以下欄位：
    - question_id: 唯一識別符 (主鍵)
    - unit_id: 單元 ID (Text)
    """
    __bind_key__ = DB_NAME
    __tablename__ = 'questions'

    question_id = db.Column(db.String(255), primary_key=True)
    unit_id = db.Column(db.Text, nullable=False)


class Statistics(db.Model):
    """
    Statistics 資料模型

    此模型定義了統計資料表的結構，包含以下欄位：
    - student_id: 學生 ID (主鍵)
    - unit_id: 單元 ID (主鍵)
    - total_correct: 答對題數 (Integer)
    - total_questions: 題目總數 (Integer, 預設值為 3)
    - accuracy_rate: 正確率 (Float)
    """
    __bind_key__ = DB_NAME
    __tablename__ = 'statistics'

    student_id = db.Column(db.Text, primary_key=True)
    unit_id = db.Column(db.Text, primary_key=True)
    total_correct = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False, default=3)
    accuracy_rate = db.Column(db.Float, nullable=False)


class TcStudents(db.Model):
    """
    TcStudents 資料模型

    此模型定義了 TcStudents 資料表的結構，包含以下欄位：
    - student_id: 唯一識別符 (主鍵)
    - name: 學生名稱 (Text)
    - gender: 性別 (Enum: '男性', '女性', '其他', '')
    - birth_date: 出生日期 (Date)
    - age: 年齡 (Integer)
    - disorder_category: 障礙類別 (Text)
    - created_at: 建立時間 (DateTime)
    """
    __bind_key__ = DB_NAME
    __tablename__ = 'students'

    student_id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Enum('男性', '女性', '其他', '', name='gender_enum'), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disorder_category = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class Units(db.Model):
    """
    Units 資料模型

    此模型定義了單元資料表的結構，包含以下欄位：
    - unit_id: 唯一識別符 (主鍵)
    - unit_name: 單元名稱 (Text)
    - video_code: 影片代碼 (Text)
    """
    __bind_key__ = DB_NAME
    __tablename__ = 'units'

    unit_id = db.Column(db.String(255), primary_key=True)
    unit_name = db.Column(db.Text, nullable=False)
    video_code = db.Column(db.Text, nullable=False)


class Users(db.Model):
    """
    Users 資料模型

    此模型定義了用戶資料表的結構，包含以下欄位：
    - user_id: 唯一識別符 (主鍵)
    - student_id: 學生 ID (Text)
    - username: 用戶名稱 (Text)
    - password: 密碼 (Text)
    - role: 角色 (Text)
    - created_at: 建立時間 (DateTime)
    """
    __bind_key__ = DB_NAME
    __tablename__ = 'users'

    user_id = db.Column(db.String(255), primary_key=True)
    student_id = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
