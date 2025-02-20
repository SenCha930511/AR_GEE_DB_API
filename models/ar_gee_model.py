from . import db

DB_NAME = "ar_gee"

class PracticeAnswers(db.Model):
    """
    PracticeAnswers 資料模型

    此模型定義了練習答案資料表的結構，包含以下欄位：
    - practice_answer_id: 唯一識別符 (主鍵)
    - student_id: 學生 ID
    - practice_question_id: 練習題目 ID
    - is_correct: 是否答對 (布林值)
    - response_time: 回答所花費的時間 (Time)
    - test_date: 測試日期 (DateTime)
    - incorrect_attempts: 答錯次數 (Integer)
    """
    __bind_key__ = DB_NAME
    __tablename__ = "practice_answers"

    practice_answer_id = db.Column(db.String(255), primary_key=True, nullable=False)
    student_id = db.Column(db.Text, nullable=False)
    practice_question_id = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)  
    response_time = db.Column(db.Time, nullable=False)
    test_date = db.Column(db.DateTime, nullable=False)
    incorrect_attempts = db.Column(db.Integer, nullable=False)


class PracticeQuestions(db.Model):
    """
    PracticeQuestions 資料模型

    此模型定義了練習題目資料表的結構，包含以下欄位：
    - practice_question_id: 唯一識別符 (主鍵)
    - unit_id: 單元 ID
    """
    __bind_key__ = DB_NAME
    __tablename__ = "practice_questions"

    practice_question_id = db.Column(db.String(255), primary_key=True, nullable=False)
    unit_id = db.Column(db.Text, nullable=False)


class PracticeStatistics(db.Model):
    """
    PracticeStatistics 資料模型

    此模型定義了練習統計資料表的結構，包含以下欄位：
    - student_id: 學生 ID (主鍵)
    - unit_id: 單元 ID (主鍵)
    - total_correct: 答對題數 (Integer)
    - total_questions: 題目總數 (Integer, 預設值 3)
    - accuracy_rate: 正確率 (Float)
    """
    __bind_key__ = DB_NAME
    __tablename__ = "practice_statistics"

    student_id = db.Column(db.Text, nullable=False, primary_key=True)
    unit_id = db.Column(db.Text, nullable=False, primary_key=True)
    total_correct = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, default=3, nullable=False)
    accuracy_rate = db.Column(db.Float, nullable=False)


class PracticeUnits(db.Model):
    """
    PracticeUnits 資料模型

    此模型定義了練習單元資料表的結構，包含以下欄位：
    - unit_id: 唯一識別符 (主鍵)
    - unit_name: 單元名稱 (Text)
    - video_code: 影片代碼 (Text)
    """
    __bind_key__ = DB_NAME 
    __tablename__ = "practice_units" 

    unit_id = db.Column(db.String(255), primary_key=True, nullable=False) 
    unit_name = db.Column(db.Text, nullable=False)
    video_code = db.Column(db.Text, nullable=False)


class Students(db.Model):
    """
    Students 資料模型

    此模型定義了學生資料表的結構，包含以下欄位：
    - student_id: 唯一識別符 (主鍵)
    - username: 使用者名稱 (Text)
    - password: 密碼 (Text)
    - age: 年齡 (Integer)
    - disorder_category: 障礙類別 (Text)
    - created_at: 建立時間 (DateTime)
    """
    __bind_key__ = DB_NAME 
    __tablename__ = "students"

    student_id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disorder_category = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
