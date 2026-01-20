from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import get_password_hash

def ensure_admin():
    db = SessionLocal()
    try:
        # Ensure BasicInfo id=1 exists
        profile = db.query(models.BasicInfo).filter(models.BasicInfo.id == 1).first()
        if not profile:
            print("Creating default profile (ID 1)...")
            profile = models.BasicInfo(
                id=1,
                full_name="Vidhi",
                email="vidhi@example.com",
                bio="Default Profile"
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        
        # Ensure AdminUser 'vidhi22' exists
        user = db.query(models.AdminUser).filter(models.AdminUser.username == "vidhi22").first()
        if not user:
            print("Creating admin user 'vidhi22'...")
            hashed_pw = get_password_hash("password123") # Default password
            user = models.AdminUser(
                username="vidhi22",
                hashed_password=hashed_pw,
                profile_id=1
            )
            db.add(user)
            db.commit()
            print("Admin user 'vidhi22' created with profile_id=1")
        else:
            if user.profile_id != 1:
                print("Updating 'vidhi22' to point to profile 1...")
                user.profile_id = 1
                db.commit()
            print("Admin user 'vidhi22' already exists.")
            
    finally:
        db.close()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    ensure_admin()
