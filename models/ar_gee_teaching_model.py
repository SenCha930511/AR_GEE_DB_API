from . import db

DB_NAME = "ar_gee_teaching"

class Answers(db.Model):
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
    __bind_key__ = DB_NAME
    __tablename__ = 'questions'

    question_id = db.Column(db.String(255), primary_key=True)
    unit_id = db.Column(db.Text, nullable=False)

  
class Statistics(db.Model):
    __bind_key__ = DB_NAME
    __tablename__ = 'statistics'

    student_id = db.Column(db.Text, primary_key=True)
    unit_id = db.Column(db.Text, primary_key=True)
    total_correct = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False, default=3)
    accuracy_rate = db.Column(db.Float, nullable=False)

  
class TcStudents(db.Model):
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
    __bind_key__ = DB_NAME
    __tablename__ = 'units'

    unit_id = db.Column(db.String(255), primary_key=True)
    unit_name = db.Column(db.Text, nullable=False)
    video_code = db.Column(db.Text, nullable=False)


class Users(db.Model):
    __bind_key__ = DB_NAME
    __tablename__ = 'users'

    user_id = db.Column(db.String(255), primary_key=True)
    student_id = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)