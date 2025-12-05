from typing import Optional
from sqlalchemy.orm import Session
from app.models.token import Token
from datetime import datetime

class CRUDToken:
    def create(self, db: Session, token: str, user_id: int, type: str, expires: datetime) -> Token:
        db_token = Token(
            token=token,
            user_id=user_id,
            type=type,
            expires=expires,
            blacklisted=False
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return db_token

    def get_by_token(self, db: Session, token: str, type: str) -> Optional[Token]:
        return db.query(Token).filter(
            Token.token == token, 
            Token.type == type, 
            Token.blacklisted == False
        ).first()

    def delete_tokens_by_user(self, db: Session, user_id: int, type: str):
        # Equivalent to deleteMany in Mongoose
        db.query(Token).filter(Token.user_id == user_id, Token.type == type).delete()
        db.commit()

    def blacklist_token(self, db: Session, token_str: str, type: str):
        token_doc = self.get_by_token(db, token_str, type)
        if token_doc:
            token_doc.blacklisted = True
            db.commit()

token = CRUDToken()