# routes/admin.py
from flask import Blueprint, request, jsonify
from models import db, Subject, Chapter, Quiz, Question, User,Score
from flask_jwt_extended import jwt_required
from utils.helpers import admin_only
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Subject
from models import Note
from datetime import datetime

admin_bp = Blueprint('admin', __name__)
# ✅ CREATE SUBJECT
@admin_bp.route('/admin/subject', methods=['POST'])
@jwt_required()
def create_subject():
    print("we are in create_subject")
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        data = request.get_json(force=True)
        print("🔥 Data received from frontend:", data)
    except Exception as e:
        print("❌ JSON parsing failed:", e)
        return jsonify({"msg": "Invalid JSON format"}), 400

    name = data.get("name", "").strip()
    description = data.get("description", "").strip()

    if not name or not description:
        return jsonify({"msg": "Name and description required"}), 400

    try:
        if Subject.query.filter_by(name=name).first():
            return jsonify({"msg": "Subject with this name already exists"}), 400

        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()

        return jsonify({
            "msg": "Subject created successfully!",
            "subject_id": subject.id
        }), 201
    except Exception as e:
        db.session.rollback()
        print("💥 Database error:", e)
        return jsonify({"msg": "Failed to create subject"}), 500


# ✅ LIST SUBJECTS
@admin_bp.route('/admin/subject', methods=['GET'])
@jwt_required()
def list_subjects():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        keyword = request.args.get('q', '').strip().lower()
        if keyword:
            subjects = Subject.query.filter(Subject.name.ilike(f"%{keyword}%")).all()
        else:
            subjects = Subject.query.all()
        return jsonify([
            {"id": s.id, "name": s.name, "description": s.description}
            for s in subjects
        ])
    except Exception as e:
        print("💥 Error fetching subjects:", e)
        return jsonify({"msg": "Failed to fetch subjects"}), 500


# ✅ CREATE CHAPTER
@admin_bp.route('/admin/chapter', methods=['POST'])
@jwt_required()
def create_chapter():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        data = request.get_json(force=True)
        chapter = Chapter(
            subject_id=data['subject_id'],
            name=data['name'].strip(),
            description=data['description'].strip()
        )
        db.session.add(chapter)
        db.session.commit()
        return jsonify({"msg": "Chapter created!"}), 201
    except Exception as e:
        db.session.rollback()
        print("💥 Error creating chapter:", e)
        return jsonify({"msg": "Failed to create chapter"}), 500


# 🔍 SEARCH CHAPTERS
@admin_bp.route('/admin/search/chapters', methods=['GET'])
@jwt_required()
def search_chapters():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    keyword = request.args.get('q', '').strip().lower()
    matches = Chapter.query.filter(Chapter.name.ilike(f"%{keyword}%")).all()
    return jsonify([
    {
        "id": c.id,
        "name": c.name,
        "description": c.description,  # ✅ This was missing
        "subject_id": c.subject_id
    }
    for c in matches
    ])


# ✅ CREATE QUIZ
@admin_bp.route('/admin/quiz', methods=['POST'])
@jwt_required()
def create_quiz():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        data = request.get_json(force=True)
        quiz = Quiz(
            chapter_id=data['chapter_id'],
            date_of_quiz=data['date_of_quiz'],
            title=data['title'],
            time_duration=data['time_duration'],
            remarks=data.get('remarks', '')

        )
        db.session.add(quiz)
        db.session.commit()
        return jsonify({"msg": "Quiz created!"}), 201
    except Exception as e:
        db.session.rollback()
        print("💥 Error creating quiz:", e)
        return jsonify({"msg": "Failed to create quiz"}), 500


# ✅ CREATE QUESTION
@admin_bp.route('/admin/question', methods=['POST'])
@jwt_required()
def create_question():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        data = request.get_json(force=True)
        q = Question(
            quiz_id=data['quiz_id'],
            question_statement=data['question_statement'].strip(),
            option1=data['option1'].strip(),
            option2=data['option2'].strip(),
            option3=data['option3'].strip(),
            option4=data['option4'].strip(),
            correct_option=data['correct_option'].strip()
        )
        db.session.add(q)
        db.session.commit()
        return jsonify({"msg": "Question added!"}), 201
    except Exception as e:
        db.session.rollback()
        print("💥 Error creating question:", e)
        return jsonify({"msg": "Failed to create question"}), 500


# 🔍 SEARCH USERS
@admin_bp.route('/admin/search/users', methods=['GET'])
@jwt_required()
def search_users():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    keyword = request.args.get('q', '').strip().lower()
    matches = User.query.filter(User.email.ilike(f"%{keyword}%")).all()
    return jsonify([
        {"id": u.id, "email": u.email, "name": u.full_name, "role": u.role}
        for u in matches
    ])

# ✅ UPDATE SUBJECT
@admin_bp.route('/admin/subject/<int:subject_id>', methods=['PUT'])
@jwt_required()
def update_subject(subject_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        data = request.get_json(force=True)
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()

        if not name or not description:
            return jsonify({"msg": "Name and description required"}), 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"msg": "Subject not found"}), 404

        # Optional: Check for duplicate name
        existing = Subject.query.filter(Subject.name == name, Subject.id != subject_id).first()
        if existing:
            return jsonify({"msg": "Another subject with this name already exists"}), 400

        subject.name = name
        subject.description = description
        db.session.commit()

        return jsonify({"msg": "Subject updated successfully!"})
    except Exception as e:
        db.session.rollback()
        print("💥 Error updating subject:", e)
        return jsonify({"msg": "Failed to update subject"}), 500
# ❌ DELETE SUBJECT
@admin_bp.route('/admin/subject/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"msg": "Subject not found"}), 404

        db.session.delete(subject)
        db.session.commit()

        return jsonify({"msg": "Subject deleted successfully!"})
    except Exception as e:
        db.session.rollback()
        print("💥 Error deleting subject:", e)
        return jsonify({"msg": "Failed to delete subject"}), 500

# ✅ UPDATE CHAPTER
@admin_bp.route('/admin/chapter/<int:chapter_id>', methods=['PUT'])
@jwt_required()
def update_chapter(chapter_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        data = request.get_json(force=True)
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()

        if not name or not description:
            return jsonify({"msg": "Name and description required"}), 400

        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return jsonify({"msg": "Chapter not found"}), 404

        chapter.name = name
        chapter.description = description
        db.session.commit()

        return jsonify({"msg": "Chapter updated successfully!"})
    except Exception as e:
        db.session.rollback()
        print("💥 Error updating chapter:", e)
        return jsonify({"msg": "Failed to update chapter"}), 500

# ❌ DELETE CHAPTER
@admin_bp.route('/admin/chapter/<int:chapter_id>', methods=['DELETE'])
@jwt_required()
def delete_chapter(chapter_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return jsonify({"msg": "Chapter not found"}), 404

        db.session.delete(chapter)
        db.session.commit()

        return jsonify({"msg": "Chapter deleted successfully!"})
    except Exception as e:
        db.session.rollback()
        print("💥 Error deleting chapter:", e)
        return jsonify({"msg": "Failed to delete chapter"}), 500
# ✅ Get All Chapters for a Subject
@admin_bp.route('/admin/subject/<int:subject_id>/chapters', methods=['GET'])
@jwt_required()
def get_subject_chapters(subject_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"msg": "Subject not found"}), 404

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "quiz_count": Quiz.query.filter_by(chapter_id=c.id).count(),
            "note_count": Note.query.filter_by(
                subject_id=subject_id,
                chapter_id=c.id
            ).count()
        } for c in chapters
    ])

@admin_bp.route('/admin/chapter/<int:chapter_id>/quizzes', methods=['GET'])
@jwt_required()
def get_quizzes_by_chapter(chapter_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return jsonify([
        {
            "id": q.id,
            "date_of_quiz": q.date_of_quiz,
            "time_duration": q.time_duration,
            "remarks": q.remarks
        } for q in quizzes
    ])
@admin_bp.route('/admin/quiz/<int:quiz_id>', methods=['PUT'])
@jwt_required()
def update_quiz(quiz_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    data = request.get_json(force=True)
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"msg": "Quiz not found"}), 404
    quiz.title=data.get("title",quiz.title)
    quiz.date_of_quiz = data.get("date_of_quiz", quiz.date_of_quiz)
    quiz.time_duration = data.get("time_duration", quiz.time_duration)
    quiz.remarks = data.get("remarks", quiz.remarks)

    db.session.commit()
    return jsonify({"msg": "Quiz updated!"})
@admin_bp.route('/admin/quiz/<int:quiz_id>', methods=['DELETE'])
@jwt_required()
def delete_quiz(quiz_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"msg": "Quiz not found"}), 404

    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"msg": "Quiz deleted successfully!"})
@admin_bp.route('/admin/quiz/<int:quiz_id>/questions', methods=['GET'])
@jwt_required()
def get_questions_by_quiz(quiz_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([
        {
            "id": q.id,
            "question_statement": q.question_statement,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
            "correct_option": q.correct_option
        } for q in questions
    ])
@admin_bp.route('/admin/question/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"msg": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"msg": "Question deleted successfully!"})
@admin_bp.route('/admin/question/<int:question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"msg": "Question not found"}), 404

    data = request.get_json()

    question.question_statement = data.get('question_statement', question.question_statement)
    question.option1 = data.get('option1', question.option1)
    question.option2 = data.get('option2', question.option2)
    question.option3 = data.get('option3', question.option3)
    question.option4 = data.get('option4', question.option4)
    question.correct_option = data.get('correct_option', question.correct_option)

    db.session.commit()
    return jsonify({"msg": "Question updated successfully!"})

@admin_bp.route("/admin/quizzes", methods=["GET"])
@jwt_required()
def get_all_quizzes():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    quizzes = Quiz.query.all()
    result = []

    for q in quizzes:
        chapter = Chapter.query.get(q.chapter_id)
        subject = Subject.query.get(chapter.subject_id) if chapter else None

        result.append({
            "id": q.id,
            "title": getattr(q, "title", ""),  # Only if added
            "chapter_id": q.chapter_id,
            "date_of_quiz": q.date_of_quiz,
            "time_duration": q.time_duration,
            "remarks": q.remarks,
            "chapter_name": chapter.name if chapter else "Unknown",
            "subject_name": subject.name if subject else "Unknown",
            "question_count": len(q.questions)  # ✅ Fix here
        })

    return jsonify(result), 200
@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    # Only fetch users with role 'user'
    users = User.query.filter_by(role='user').all()
    result = []

    for user in users:
        attempt_count = Score.query.filter_by(user_id=user.id).count()
        result.append({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "qualification": user.qualification,
            "dob": user.dob,
            "quizzes_attempted": attempt_count
        })

    return jsonify(result)
@admin_bp.route('/admin/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role != 'user':
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"})
@admin_bp.route('/admin/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role != 'user':
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    user.full_name = data.get("full_name", user.full_name)
    user.email = data.get("email", user.email)
    user.qualification = data.get("qualification", user.qualification)
    user.dob = data.get("dob", user.dob)

    db.session.commit()
    return jsonify({"msg": "User updated successfully"})
@admin_bp.route('/admin/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_single_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role != 'user':
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "qualification": user.qualification,
        "dob": user.dob
    })

@admin_bp.route('/admin/summary', methods=['GET'])
@jwt_required()
def get_admin_summary():
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    try:
        subjects = Subject.query.all()
        subject_stats = []

        for subject in subjects:
            chapters_count = Chapter.query.filter_by(subject_id=subject.id).count()
            quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject.id).all()
            quizzes_count = len(quizzes)

            scores = db.session.query(Score).join(Quiz).join(Chapter).filter(Chapter.subject_id == subject.id).all()
            attempts_count = len(scores)

            top_score = max([s.total_scored for s in scores]) if scores else 0
            total_questions = sum(len(q.questions) for q in quizzes)

            if attempts_count > 0 and total_questions > 0:
                total_score_sum = sum(s.total_scored for s in scores)
                average_accuracy = round((total_score_sum / (attempts_count * total_questions)) * 100, 2)
            else:
                average_accuracy = 0

            subject_stats.append({
                "subject": subject.name,
                "chapters": chapters_count,
                "quizzes": quizzes_count,
                "attempts": attempts_count,
                "top_score": top_score,
                "average_accuracy": average_accuracy,
                "notes": Note.query.join(Chapter)
                .filter(Chapter.subject_id == subject.id)
                .count()
            })

        # Top 10 scores across all subjects
        all_scores = Score.query.order_by(Score.total_scored.desc()).limit(10).all()
        top_scores = [s.total_scored for s in all_scores]

        # User attempts per subject
        user_attempts = []
        for subject in subjects:
            count = db.session.query(Score).join(Quiz).join(Chapter).filter(Chapter.subject_id == subject.id).count()
            user_attempts.append({
                "subject": subject.name,
                "attempts": count
            })

        return jsonify({
            "detailed_stats": subject_stats,
            "top_scores": top_scores,
            "user_attempts": user_attempts
        })

    except Exception as e:
        print("Error generating admin summary:", e)
        return jsonify({"msg": "Failed to generate summary"}), 500

@admin_bp.route(
    '/admin/subject/<int:subject_id>/chapter/<int:chapter_id>/notes',
    methods=['POST']
)
@jwt_required()
def create_note(subject_id, chapter_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    data = request.get_json()

    # validate chapter belongs to subject
    chapter = Chapter.query.filter_by(id=chapter_id, subject_id=subject_id).first()
    if not chapter:
        return jsonify({"msg": "Invalid subject/chapter combination"}), 400

    note = Note(
        subject_id=subject_id,
        chapter_id=chapter_id,
        title=data.get('title', '').strip(),
        content=data.get('content', '').strip(),
        visibility=data.get('visibility', 'public'),
        created_at=datetime.utcnow()
    )

    db.session.add(note)
    db.session.commit()

    return jsonify({
        "msg": "Note created successfully",
        "note_id": note.id,
        "created_at": note.created_at.isoformat()
    }), 201


@admin_bp.route(
    '/admin/subject/<int:subject_id>/chapter/<int:chapter_id>/notes',
    methods=['GET']
)
@jwt_required()
def list_notes(subject_id, chapter_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    notes = Note.query.filter_by(
        subject_id=subject_id,
        chapter_id=chapter_id
    ).all()

    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "subject_id": n.subject_id,
            "chapter_id": n.chapter_id,
            "visibility": n.visibility,
            "created_at": n.created_at.isoformat()
        } for n in notes
    ])


@admin_bp.route('/admin/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    note = Note.query.get(note_id)
    if not note:
        return jsonify({"msg": "Note not found"}), 404

    data = request.get_json()

    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)
    note.visibility = data.get("visibility", note.visibility)

    db.session.commit()
    return jsonify({"msg": "Note updated"})
@admin_bp.route('/admin/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    note = Note.query.get(note_id)
    if not note:
        return jsonify({"msg": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"msg": "Note deleted"})

@admin_bp.route('/admin/subject/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_subject(subject_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    subject = Subject.query.get(subject_id)

    if not subject:
        return jsonify({"msg": "Subject not found"}), 404

    return jsonify({
        "id": subject.id,
        "name": subject.name,
        "description": subject.description
    })
@admin_bp.route('/admin/subject/<int:subject_id>/chapters/<int:chapter_id>', methods=['GET'])
@jwt_required()
def get_chapter(subject_id, chapter_id):
    if not admin_only():
        return jsonify({"msg": "Admin access only"}), 403

    chapter = Chapter.query.filter_by(
        id=chapter_id,
        subject_id=subject_id
    ).first()

    if not chapter:
        return jsonify({"msg": "Invalid subject/chapter combination"}), 404

    return jsonify({
        "id": chapter.id,
        "name": chapter.name,
        "description": chapter.description
    })


