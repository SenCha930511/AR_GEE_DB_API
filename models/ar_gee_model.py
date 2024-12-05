from . import db

DB_NAME = "ar_gee"

class PracticeAnswers(db.Model):
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
    __bind_key__ = DB_NAME
    __tablename__ = "practice_questions"

    practice_question_id = db.Column(db.String(255), primary_key=True, nullable=False)
    unit_id = db.Column(db.Text, nullable=False)


class PracticeStatistics(db.Model):
    __bind_key__ = DB_NAME
    __tablename__ = "practice_statistics"

    student_id = db.Column(db.Text, nullable=False, primary_key=True)
    unit_id = db.Column(db.Text, nullable=False, primary_key=True)
    total_correct = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, default=3, nullable=False)
    accuracy_rate = db.Column(db.Float, nullable=False)


class PracticeUnits(db.Model):
    __bind_key__ = DB_NAME 
    __tablename__ = "practice_units" 

    unit_id = db.Column(db.String(255), primary_key=True, nullable=False) 
    unit_name = db.Column(db.Text, nullable=False)
    video_code = db.Column(db.Text, nullable=False) 


class Students(db.Model):
    __bind_key__ = DB_NAME 
    __tablename__ = "students"

    student_id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disorder_category = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
