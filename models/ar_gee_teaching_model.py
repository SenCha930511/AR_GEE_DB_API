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

    def __repr__(self):
        return f"<Answer(answer_id={self.answer_id}, student_id={self.student_id}, is_correct={self.is_correct}, response_time={self.response_time}, test_date={self.test_date}, incorrect_attempts={self.incorrect_attempts})>"

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
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
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
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)