from flask import Flask
from config import Config
from models import db, User
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask import send_from_directory
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)


@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory('uploads', filename)


@app.route('/')
def home():
    return {"message": "Quiz Master V2 Backend Running 🎯"}

# 🔹 Import and register blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

# 🔹 Auto-create admin user (with error handling)
with app.app_context():
    try:
        # First create all tables
        db.create_all()
        
        # Try to query, but handle missing columns
        admin = User.query.filter_by(email='admin@quiz.com').first()
        if not admin:
            admin_user = User(
                email='admin@quiz.com',
                password=bcrypt.generate_password_hash("admin123").decode('utf-8'),
                full_name="Admin",
                qualification="Admin",
                dob="2000-01-01",
                role="admin"
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created")
    except Exception as e:
        print(f"⚠️ Error during startup: {e}")
        print("This is normal if the database schema has changed.")
        print("Run 'flask db migrate' and 'flask db upgrade' to update the schema.")

# 🔹 Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)