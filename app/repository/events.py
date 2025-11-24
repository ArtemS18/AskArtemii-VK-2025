from sqlalchemy import Connection, event, update

from app.models.likes import QuestionLikeORM
from app.models.questions import QuestionORM

# @event.listens_for(QuestionLikeORM, 'after_insert')
# async def receive_after_insert(mapper, connection: Connection, target: QuestionLikeORM):
#     if target.question_id:
#         await connection.execute(
#             update(QuestionORM)
#             .where(QuestionORM.id == target.question_id)
#             .values(likes_count=QuestionORM.likes_count + 1)
#         )

# @event.listens_for(QuestionLikeORM, 'after_delete')
# async def receive_after_delete(mapper, connection: Connection, target: QuestionLikeORM):
#     if target.question_id:
#         await connection.execute(
#             update(QuestionORM)
#             .where(QuestionORM.id == target.question_id)
#             .values(likes_count=QuestionORM.likes_count - 1)
#         )