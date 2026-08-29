from flask import Flask
from config import Config
from models import db, User
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# 🔹 Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# 🔹 Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)




# 🔹 Home route (test)
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

# 🔹 Auto-create admin user
with app.app_context():
    db.create_all()
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


# 🔹 Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)