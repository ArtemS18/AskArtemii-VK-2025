from logging import getLogger
import logging
from app.core.db import SessionLocal, init_db, drop_db
from app.models import (
    UserORM, UserProfileORM, QuestionORM, AnswerORM,
    QuestionLikeORM, AnswerLikeORM, TagORM, QuestionTagsORM
)
import sys
import random 
from sqlalchemy import insert
from app.web.logger import setup_logger

log = getLogger(__name__)

def generate_users(ratio: int) -> list[tuple]:
    """Генерирует данные для пользователей и их профилей."""
    user_data = []
    profile_data = []
    for i in range(ratio):
        login = f"user_{i}"
        hashed_password = f"hashed_password_{i}"
        popular_count = random.randint(0, 1000)
        
        profile_data.append({
            "img_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4JCuHyuURcCyeNEc9v4iOma3HVgZgDSMaIQ&s",
            "nickname": f"Nickname_{i}"
        })
        
        user_data.append({
            "email": f"user_{i}@example.com",
            "hashed_password": hashed_password,
            "popular_count": popular_count
            # profile_id будет установлен после создания профилей
        })
    return user_data, profile_data

def generate_questions(ratio: int, user_ids: list[int]) -> list[tuple]:
    questions = []
    for i in range(ratio * 10):
        author_id = random.choice(user_ids) # Выбираем случайного пользователя
        questions.append({
            "title": f"Question Title {i}",
            "text": f"Question Text {i}. This is a sample question generated for testing purposes.",
            "likes_count": random.randint(1, 50),
            "author_id": author_id
        })
    return questions

def generate_answers(ratio: int, user_ids: list[int], question_ids: list[int]) -> list[tuple]:
    answers = []
    for i in range(ratio*100):
        author_id = random.choice(user_ids)
        question_id = random.choice(question_ids)
        answers.append({
            "text": f"Answer Text {i}. This is a sample answer to question {question_id}.",
            "likes_count": random.randint(0, 20),
            "is_correct": random.choice([True, False]),
            "author_id": author_id,
            "question_id": question_id
        })
    return answers

def generate_tags(ratio: int) -> list[tuple]:
    """Генерирует данные для тегов."""
    tags = []
    for i in range(ratio):
        tags.append({"name": f"Tag_{i}"})
    return tags

def generate_question_likes(ratio: int, user_ids: list[int], question_ids: list[int]) -> list[tuple]:
    likes = []
    generated_pairs = set()
    for _ in range(ratio * 200):
        user_id = random.choice(user_ids)
        question_id = random.choice(question_ids)
        
        if (user_id, question_id) not in generated_pairs:
            likes.append({
                "user_id": user_id,
                "question_id": question_id
            })
            generated_pairs.add((user_id, question_id))
    return likes

def generate_answer_likes(ratio: int, user_ids: list[int], answer_ids: list[int]) -> list[tuple]:
    likes = []
    generated_pairs = set()
    for _ in range(ratio * 200):
        user_id = random.choice(user_ids)
        answer_id = random.choice(answer_ids)
        
        if (user_id, answer_id) not in generated_pairs:
            likes.append({
                "user_id": user_id,
                "answer_id": answer_id
            })
            generated_pairs.add((user_id, answer_id))
    return likes

def generate_question_tags(ratio: int, question_ids: list[int], tag_ids: list[int]) -> list[tuple]:
    question_tags = []
    generated_pairs = set()
    for _ in range(ratio * 10):
        question_id = random.choice(question_ids)
        tag_id = random.choice(tag_ids)
        
        if (question_id, tag_id) not in generated_pairs:
            question_tags.append({
                "question_id": question_id,
                "tag_id": tag_id
            })
            generated_pairs.add((question_id, tag_id))
    return question_tags

async def fill_db(ratio = 100):
    async with SessionLocal() as session:
        user_data_tuples, profile_data_tuples = generate_users(ratio)
        stmt_users = insert(UserORM).values(user_data_tuples).returning(UserORM.id)
        result_users = await session.execute(stmt_users)
        await session.flush()
        
        created_user_ids = result_users.scalars().all()
        for i, profile_data in enumerate(profile_data_tuples):
            profile_data["user_id"] = created_user_ids[i]

        stmt_profiles = insert(UserProfileORM).values(profile_data_tuples)
        await session.execute(stmt_profiles)
        await session.flush()

        log.info(f"Created {ratio} users and profiles.")

        question_data_tuples = generate_questions(ratio, created_user_ids)
        stmt_questions = insert(QuestionORM).values(question_data_tuples).returning(QuestionORM.id)
        result_questions = await session.execute(stmt_questions)
        await session.flush()
        created_question_ids = result_questions.scalars().all()
        log.info(f"Created {ratio * 10} questions.")
        answer_data_tuples = generate_answers(ratio, created_user_ids, created_question_ids)
        created_answer_ids = []
        for k in range(0, len(answer_data_tuples), 1000):
            len_ = min(len(answer_data_tuples)-1, k+1000)
            stmt_answers = insert(AnswerORM).values(answer_data_tuples[k:len_]).returning(AnswerORM.id)
            result_answers = await session.execute(stmt_answers)
            await session.flush()
            created_answer_ids.extend(result_answers.scalars().all())
        log.info(f"Created {ratio * 100} answers.")
        
        tag_data_tuples = generate_tags(ratio)
        created_tag_ids = []
        for k in range(0, len(tag_data_tuples), 1000):
            len_ = min(len(tag_data_tuples)-1, k+1000)
            stmt_tags = insert(TagORM).values(tag_data_tuples[k:len_]).returning(TagORM.id)
            result_tags = await session.execute(stmt_tags)
            await session.flush()
            created_tag_ids.extend(result_tags.scalars().all())
        log.info(f"Created {ratio} tags.")
        question_tags_data_tuples = generate_question_tags(ratio, created_question_ids, created_tag_ids)
        stmt_question_tags = insert(QuestionTagsORM).values(question_tags_data_tuples)
        await session.execute(stmt_question_tags)
        await session.flush()
        log.info(f"Created {len(question_tags_data_tuples)} question-tag associations.")

        question_likes_data_tuples = generate_question_likes(ratio, created_user_ids, created_question_ids)
        for k in range(0, len(question_likes_data_tuples), 1000):
            len_ = min(len(question_likes_data_tuples)-1, k+1000)
            stmt_question_likes = insert(QuestionLikeORM).values(question_likes_data_tuples[k:len_])
            await session.execute(stmt_question_likes)
            await session.flush()
        log.info(f"Created {len(question_likes_data_tuples)} question likes.")

        answer_likes_data_tuples = generate_answer_likes(ratio, created_user_ids, created_answer_ids)
        for k in range(0, len(answer_likes_data_tuples), 1000):
            len_ = min(len(answer_likes_data_tuples)-1, k+1000)
            stmt_answer_likes = insert(AnswerLikeORM).values(answer_likes_data_tuples[k:len_])
            await session.execute(stmt_answer_likes)
            await session.flush()
        log.info(f"Created {len(answer_likes_data_tuples)} answer likes.")

        await session.commit()
        log.info("Database filled successfully!")

async def main():
    ratio = 10
    if len(sys.argv) > 1:
        try:
            if int(sys.argv[1]):
                ratio = int(sys.argv[1])
        except ValueError:
            return
    await drop_db()
    await init_db()
    setup_logger(logging.INFO)
    await fill_db(ratio)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
