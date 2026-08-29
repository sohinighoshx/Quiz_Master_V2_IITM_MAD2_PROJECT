from flask import Blueprint, request, jsonify
from models import db, Subject, Chapter, Quiz, Question, Score, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json
user_bp = Blueprint('user', __name__)

# ---------------------- GET SUBJECTS ----------------------
@user_bp.route('/user/subjects', methods=['GET'])
@jwt_required()
 
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{"id": s.id, "name": s.name, "description": s.description} for s in subjects])

# ---------------------- GET CHAPTERS ----------------------
@user_bp.route('/user/chapters/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([{"id": c.id, "name": c.name, "description": c.description} for c in chapters])

# ---------------------- GET QUIZZES ----------------------
from datetime import datetime, timedelta

@user_bp.route('/user/quizzes/<int:chapter_id>', methods=['GET'])
@jwt_required()
def get_quizzes(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    result = []

    for q in quizzes:
        # Get related chapter and subject
        chapter = Chapter.query.get(q.chapter_id)
        subject = Subject.query.get(chapter.subject_id) if chapter else None

        # Parse date_of_quiz to compute deadline
        try:
            quiz_date = datetime.strptime(q.date_of_quiz, "%Y-%m-%d")
            deadline = quiz_date + timedelta(days=4)
            deadline_str = deadline.strftime("%Y-%m-%d")
        except:
            deadline_str = "N/A"

        result.append({
            "id": q.id,
            "title": q.title,
            "date_of_quiz": q.date_of_quiz,
            "time_duration": q.time_duration,
            "remarks": q.remarks,
            "chapter_name": chapter.name if chapter else "Unknown",
            "subject_name": subject.name if subject else "Unknown",
            "deadline": deadline_str
        })

    return jsonify(result)

# ---------------------- GET QUESTIONS ----------------------
@user_bp.route('/user/quiz/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([
        {
            "id": q.id,
            "question_statement": q.question_statement,
            "options": {
                "option1": q.option1,
                "option2": q.option2,
                "option3": q.option3,
                "option4": q.option4
            }
        } for q in questions
    ])

# ---------------------- SUBMIT QUIZ ----------------------
@user_bp.route('/user/submit_quiz/<int:quiz_id>', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    data = request.json
    print("📥 Got this data from frontend:", data)

    identity = get_jwt_identity()
    print(f"👤 JWT identity from token: {identity}")
    print(f"🔍 Identity type: {type(identity)}")

    # If identity is a JSON string, parse it to a dict
    if isinstance(identity, str):
        try:
            identity = json.loads(identity)
            print("🧠 Parsed identity to dict:", identity)
        except Exception as e:
            print("❌ Failed to parse identity:", e)
            return jsonify({"msg": "Invalid token identity"}), 400

    user_id = identity.get("id") if isinstance(identity, dict) else None

    if not user_id:
        return jsonify({"msg": "User ID not found in token"}), 400

    # Confirm user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    print(f"🧑‍💻 User ID: {user_id}")

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if not questions:
        return jsonify({"msg": "No questions found"}), 404

    score = 0
    for q in questions:
        selected = data.get(str(q.id))
        print(f"📝 QID {q.id} → selected: {selected}, correct: {q.correct_option}")

        if selected == q.correct_option:
            score += 1

    new_score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        total_scored=score
    )
    db.session.add(new_score)
    user.last_seen = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "msg": "✅ Quiz submitted successfully",
        "total_scored": score,
        "total_questions": len(questions)
    })

# ---------------------- VIEW PREVIOUS SCORES ----------------------
@user_bp.route('/user/scores', methods=['GET'])
@jwt_required()
def get_scores():
    identity = get_jwt_identity()
    # FIX: identity is the email string, not a dict
    user = User.query.filter_by(email=identity).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user_id = user.id

    scores = Score.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "quiz_id": s.quiz_id,
            "score": s.total_scored,
            "timestamp": s.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M")
        } for s in scores
    ])
@user_bp.route('/user/all_quizzes', methods=['GET'])
@jwt_required()
def get_all_quizzes():
    quizzes = Quiz.query.all()
    result = []

    for q in quizzes:
        chapter = Chapter.query.get(q.chapter_id)
        subject = Subject.query.get(chapter.subject_id) if chapter else None

        try:
            quiz_date = datetime.strptime(q.date_of_quiz, "%Y-%m-%d")
            deadline = quiz_date + timedelta(days=4)
            deadline_str = deadline.strftime("%Y-%m-%d")
        except:
            deadline_str = "N/A"

        result.append({
            "id": q.id,
            "title": q.title,
            "date_of_quiz": q.date_of_quiz,
            "time_duration": q.time_duration,
            "remarks": q.remarks,
            "chapter_name": chapter.name if chapter else "Unknown",
            "subject_name": subject.name if subject else "Unknown",
            "subject_id": subject.id if subject else None,
            "chapter_id": chapter.id if chapter else None,
            "deadline": deadline_str
        })

    return jsonify(result)
# ---------------------- PROGRESS SUMMARY ----------------------
@user_bp.route('/user/progress_summary', methods=['GET'])
@jwt_required()
def get_progress_summary():
    identity = get_jwt_identity()
    try:
        if isinstance(identity, str):
            identity = json.loads(identity)
        user_id = identity.get("id")
    except:
        return jsonify({"msg": "Invalid token"}), 400

    if not user_id:
        return jsonify({"msg": "User not found"}), 404

    # Get all scores for user
    scores = Score.query.filter_by(user_id=user_id).all()

    summary = []
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id) if quiz else None
        subject = Subject.query.get(chapter.subject_id) if chapter else None

        summary.append({
            "quiz_id": quiz.id if quiz else None,
            "quiz_title": quiz.title if quiz else "Unknown",
            "score": score.total_scored,
            "total": len(quiz.questions) if quiz else 0,
            "timestamp": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M"),
            "subject_name": subject.name if subject else "Unknown",
            "chapter_name": chapter.name if chapter else "Unknown"
        })

    return jsonify(summary)
# ---------------------- PROGRESS STATISTICS ----------------------
@user_bp.route('/user/progress_stats', methods=['GET'])
@jwt_required()
def get_progress_stats():
    identity = get_jwt_identity()

    # Parse identity if it's a JSON string
    if isinstance(identity, str):
        try:
            identity = json.loads(identity)
            print("🧠 Parsed identity to dict:", identity)
        except Exception as e:
            print("❌ Failed to parse identity:", e)
            return jsonify({"msg": "Invalid token identity"}), 400

    user_id = identity.get("id") if isinstance(identity, dict) else None
    if not user_id:
        return jsonify({"msg": "User ID not found in token"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Fetch all scores with related quiz → chapter → subject
    scores = db.session.query(
        Score, Quiz, Chapter, Subject
    ).join(
        Quiz, Score.quiz_id == Quiz.id
    ).join(
        Chapter, Quiz.chapter_id == Chapter.id
    ).join(
        Subject, Chapter.subject_id == Subject.id
    ).filter(
        Score.user_id == user.id
    ).all()

    # Accumulate stats
    subjects = {}
    total_quizzes_attempted = 0
    total_questions_attempted = 0
    total_correct_answers = 0

    for score, quiz, chapter, subject in scores:
        # Handle JSON string questions
        try:
            questions = json.loads(quiz.questions) if isinstance(quiz.questions, str) else quiz.questions
        except Exception as e:
            print(f"⚠️ Failed to parse quiz.questions for quiz {quiz.id}: {e}")
            questions = []

        questions_count = len(questions)
        subject_name = subject.name

        if subject_name not in subjects:
            subjects[subject_name] = {
                'quizzes_attempted': 0,
                'questions_attempted': 0,
                'correct_answers': 0
            }

        subjects[subject_name]['quizzes_attempted'] += 1
        subjects[subject_name]['questions_attempted'] += questions_count
        subjects[subject_name]['correct_answers'] += score.total_scored

        total_quizzes_attempted += 1
        total_questions_attempted += questions_count
        total_correct_answers += score.total_scored

    # Build response
    subject_stats = []
    for subject_name, stats in subjects.items():
        accuracy = (
            stats['correct_answers'] / stats['questions_attempted'] * 100
            if stats['questions_attempted'] > 0 else 0
        )
        subject_stats.append({
            'subject': subject_name,
            'quizzes_attempted': stats['quizzes_attempted'],
            'questions_attempted': stats['questions_attempted'],
            'accuracy': round(accuracy, 2)
        })

    overall_accuracy = (
        total_correct_answers / total_questions_attempted * 100
        if total_questions_attempted > 0 else 0
    )

    return jsonify({
        'total_quizzes_attempted': total_quizzes_attempted,
        'total_questions_attempted': total_questions_attempted,
        'overall_accuracy': round(overall_accuracy, 2),
        'subjects': subject_stats
    })



