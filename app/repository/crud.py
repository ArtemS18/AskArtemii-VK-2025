from app.models.answers import Answer
from app.models.questions import Question
from app.models.tags import Tag
from app.models.users import User

async def get_users() -> list[User]:
    users = []
    for i in range(5):
        users.append(User(id=i, login=f"user{i}", email=f"user{i}@gmail.com", nickname=f"User{i}", count=i*10+5%(i+1), img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4JCuHyuURcCyeNEc9v4iOma3HVgZgDSMaIQ&s"))
    return users

async def get_tags() -> list[Tag]:
    tags = [Tag(id=1, name="pyhon", popular=10), Tag(id=2, name="nginx", popular=40)]
    return tags

async def get_answers() -> list[Answer]:
    users = await get_users()
    return [
        Answer(id=0, text="Answer 1", author=users[0], votes=50, is_correct=True),
        Answer(id=0, text="Answer 2", author=users[1], votes=3)
        ]

async def get_questions() -> list[Question]:
    questions = []
    tags = await get_tags()
    users = await get_users()
    answers = await get_answers()
    for i in range(5):
        questions.append(
            Question(
                id=i, 
                title=f"Question N{i}", 
                text=f"Text Question N{i}",
                author=users[i], 
                likes=(10%(i+1)), 
                tags=tags,
                answers_count=len(answers),
                answers=answers
            )
        )
    return questions
    