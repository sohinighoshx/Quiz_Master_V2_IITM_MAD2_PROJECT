from flask import Blueprint, request, jsonify
from models import db, Subject, Chapter, Quiz, Question, Score, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json
from models import Note
import os
from werkzeug.utils import secure_filename

UPLOAD_BG = "uploads/backgrounds"
UPLOAD_MUSIC = "uploads/music"

os.makedirs(UPLOAD_BG, exist_ok=True)
os.makedirs(UPLOAD_MUSIC, exist_ok=True)
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



@user_bp.route('/user/study_space/<int:chapter_id>', methods=['GET'])
@jwt_required()
def get_public_notes(chapter_id):
    notes = Note.query.filter_by(
        chapter_id=chapter_id,
        visibility="public"
    ).all()

    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "subject_id": n.subject_id,
            "chapter_id": n.chapter_id
        } for n in notes
    ])
@user_bp.route('/user/settings', methods=['GET'])
@jwt_required()
def get_user_settings():
    identity = get_jwt_identity()
    if isinstance(identity, str):
        identity = json.loads(identity)

    user = User.query.get(identity.get("id"))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "email": user.email,
        "full_name": user.full_name,
        "qualification": user.qualification,
        "dob": user.dob,
        "profile_bg": user.profile_bg,
        "study_music": user.study_music,
        "music_upload_date": user.music_upload_date.isoformat() if user.music_upload_date else None,
        "theme_preference": user.theme_preference or "light",
        "music_autoplay": user.music_autoplay if user.music_autoplay is not None else True
    })
@user_bp.route('/user/settings/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    identity = get_jwt_identity()
    if isinstance(identity, str):
        identity = json.loads(identity)

    user = User.query.get(identity.get("id"))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()

    user.full_name = data.get("full_name", user.full_name)
    user.qualification = data.get("qualification", user.qualification)
    user.dob = data.get("dob", user.dob)

    db.session.commit()
    return jsonify({"msg": "Profile updated successfully"})
@user_bp.route('/user/settings/background', methods=['POST'])
@jwt_required()
def upload_background():
    identity = get_jwt_identity()
    if isinstance(identity, str):
        identity = json.loads(identity)

    user = User.query.get(identity.get("id"))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if 'file' not in request.files:
        return jsonify({"msg": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    path = os.path.join(UPLOAD_BG, f"user_{user.id}_{filename}")
    file.save(path)

    user.profile_bg = path
    db.session.commit()

    return jsonify({
        "msg": "Background updated",
        "background": path
    })

@user_bp.route('/user/settings/music', methods=['POST'])
@jwt_required()
def upload_music():
    identity = get_jwt_identity()
    if isinstance(identity, str):
        identity = json.loads(identity)

    user = User.query.get(identity.get("id"))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if 'file' not in request.files:
        return jsonify({"msg": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No file selected"}), 400

    # Validate file type
    allowed_extensions = {'mp3', 'wav', 'ogg', 'm4a'}
    filename = secure_filename(file.filename)
    
    if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"msg": "Invalid file type. Allowed: MP3, WAV, OGG, M4A"}), 400

    # Check file size (10MB limit)
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    
    if file_length > 10 * 1024 * 1024:  # 10MB
        return jsonify({"msg": "File too large. Max size: 10MB"}), 400

    # Delete old music file if exists
    if user.study_music and os.path.exists(user.study_music):
        try:
            os.remove(user.study_music)
        except Exception as e:
            print(f"Error deleting old music file: {e}")

    # Save new file
    filename = f"user_{user.id}_{int(datetime.utcnow().timestamp())}_{filename}"
    path = os.path.join(UPLOAD_MUSIC, filename)
    file.save(path)

    # Update user record with BOTH fields
    user.study_music = path
    user.music_upload_date = datetime.utcnow()  # ADD THIS LINE
    
    db.session.commit()

    return jsonify({
        "msg": "Music uploaded successfully",
        "music": path,
        "music_upload_date": user.music_upload_date.isoformat() if user.music_upload_date else datetime.utcnow().isoformat()
    })
@user_bp.route('/user/settings/background', methods=['DELETE'])
@jwt_required()
def delete_background():
    identity = get_jwt_identity()
    if isinstance(identity, str):
        identity = json.loads(identity)

    user = User.query.get(identity.get("id"))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Delete the file if it exists
    if user.profile_bg and os.path.exists(user.profile_bg):
        try:
            os.remove(user.profile_bg)
        except Exception as e:
            print(f"Error deleting background file: {e}")

    user.profile_bg = None
    db.session.commit()

    return jsonify({"msg": "Background removed successfully"})


@user_bp.route('/user/settings/music', methods=['DELETE'])
@jwt_required()
def delete_music():
    identity = get_jwt_identity()
    if isinstance(identity, str):
        identity = json.loads(identity)

    user = User.query.get(identity.get("id"))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Delete the file if it exists
    if user.study_music and os.path.exists(user.study_music):
        try:
            os.remove(user.study_music)
        except Exception as e:
            print(f"Error deleting music file: {e}")

    user.study_music = None
    db.session.commit()

    return jsonify({"msg": "Music removed successfully"})


@user_bp.route('/user/settings/music/autoplay', methods=['PUT'])
@jwt_required()
def update_music_autoplay():
    identity = get_jwt_identity()
    if isinstance(identity, str):
        identity = json.loads(identity)

    user = User.query.get(identity.get("id"))
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    autoplay = data.get('autoplay', True)
    
    # Now this will work since we added the field to the model
    user.music_autoplay = autoplay
    db.session.commit()

    return jsonify({"msg": "Autoplay preference updated", "autoplay": autoplay})
@user_bp.route('/user/read-notes/subjects', methods=['GET'])
@jwt_required()
def read_notes_subjects():
    subjects = Subject.query.all()
    return jsonify([
        {"id": s.id, "name": s.name}
        for s in subjects
    ])
@user_bp.route('/user/read-notes/<int:chapter_id>', methods=['GET'])
@jwt_required()
def read_public_notes(chapter_id):
    notes = Note.query.filter_by(
        chapter_id=chapter_id,
        visibility="public"
    ).order_by(Note.created_at.desc()).all()

    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at.strftime("%Y-%m-%d")
        }
        for n in notes
    ])
@user_bp.route('/user/read-notes/search', methods=['GET'])
@jwt_required()
def search_notes():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    notes = Note.query.filter(
        Note.visibility == "public",
        Note.title.ilike(f"%{q}%") | Note.content.ilike(f"%{q}%")
    ).all()

    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content[:150] + "..."
        }
        for n in notes
    ])
