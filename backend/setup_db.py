# setup_db.py
from app import app, db, bcrypt
from models import User

with app.app_context():
    # Drop and recreate all tables
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    
    # Create admin user
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
    
    print("✅ Database setup complete!")