import logging
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.config import settings

logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Create superuser if it doesn't exist
    user = crud.user.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = schemas.UserCreate(
            email="admin@example.com",
            password="password123", # Change this in production
            name="Admin User",
            role="admin",
            is_active=True,
            is_email_verified=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        logger.info("Superuser created")
    else:
        logger.info("Superuser already exists")