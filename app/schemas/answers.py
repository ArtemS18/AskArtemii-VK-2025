from app.models import AnswerORM
from sqlalchemy_to_pydantic import sqlalchemy_to_pydantic

Answer = sqlalchemy_to_pydantic(AnswerORM)
