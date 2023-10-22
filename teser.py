from sqlalchemy import select
from models import User
from routers import get_db
from sqlalchemy.orm import Session
from database import SessionLocal

with SessionLocal() as session:
    smtp = select(User).where(User.id == 1)
    user = session.execute(smtp).all()
    print(user)
