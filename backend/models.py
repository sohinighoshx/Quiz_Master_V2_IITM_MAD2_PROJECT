from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    full_name = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    dob = db.Column(db.String(10))
    role = db.Column(db.String(20), default='user')
    
    # ✅ ALL THESE FIELDS MUST EXIST:
    profile_bg = db.Column(db.String(255), nullable=True)
    study_music = db.Column(db.String(255), nullable=True)
    music_upload_date = db.Column(db.DateTime, nullable=True)
    theme_preference = db.Column(db.String(20), default='light', nullable=True)
    music_autoplay = db.Column(db.Boolean, default=True, nullable=True)
    
    scores = db.relationship("Score", backref="user", cascade="all, delete-orphan")

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    # Cascade delete subject → chapters
    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete-orphan")

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    # Cascade delete chapter → quizzes
    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete-orphan")
    notes=db.relationship("Note",backref="chapter",cascade="all, delete-orphan")
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    title = db.Column(db.String(150))  # ✅ Add this
    date_of_quiz = db.Column(db.String(20))
    time_duration = db.Column(db.String(10))
    remarks = db.Column(db.Text)
    questions = db.relationship("Question", backref="quiz", cascade="all, delete-orphan")
    scores = db.relationship("Score", backref="quiz", cascade="all, delete-orphan")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    question_statement = db.Column(db.Text)
    option1 = db.Column(db.String(200))
    option2 = db.Column(db.String(200))
    option3 = db.Column(db.String(200))
    option4 = db.Column(db.String(200))
    correct_option = db.Column(db.String(10))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Integer)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)

    title = db.Column(db.String(200))
    content = db.Column(db.Text)  # can store text OR URL to PDF

    visibility = db.Column(db.String(20), default="public")  # "public" / "private"

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional relationships (handy for joins)
    subject = db.relationship("Subject", backref="notes")
   
