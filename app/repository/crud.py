from app.entities.answers import Answer
from app.entities.questions import Question
from app.entities.tags import Tag
from app.entities.users import User

async def mock_get_users() -> list[User]:
    users = []
    for i in range(5):
        users.append(User(id=i, login=f"user{i}", email=f"user{i}@gmail.com", nickname=f"User{i}", count=i*10+5%(i+1), img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4JCuHyuURcCyeNEc9v4iOma3HVgZgDSMaIQ&s"))
    return users

async def mock_get_tags() -> list[Tag]:
    tags = []
    names = ("python", "nginx", "java", "swift", "fast_api")
    for i in range(10):
        tags.append(Tag(id=i, name=names[i%len(names)], popular=(i*10+1)%10))
    return tags

async def mock_get_answers() -> list[Answer]:
    users = await mock_get_users()
    answers: list[Answer] = []
    for i in range(151):
        answers.append(
            Answer(
                id=i, 
                text=f"Text Question N{i}",
                author=users[i%len(users)], 
                votes=(10%(i+1)), 
                is_correct=False
            )
        )
    return answers

async def mock_get_questions() -> list[Question]:
    questions = []
    tags = await mock_get_tags()
    users = await mock_get_users()
    all_answers = await mock_get_answers()
    for i in range(100):
        answers = all_answers[i % len(all_answers):(i % len(all_answers))+ (i%5)+1].copy()
        answers[0].is_correct = True
        questions.append(
            Question(
                id=i, 
                title=f"Question N{i}", 
                text=f"Text Question N{i}",
                author=users[i%len(users)], 
                likes=(10%(i+1)), 
                tags=tags[i%len(tags): (i%len(tags))+3],
                answers_count=len(answers),
                answers=answers
            )
        )

    return questions
    

async def get_count_questions() -> int:
    questions = await mock_get_questions()
    return len(questions)