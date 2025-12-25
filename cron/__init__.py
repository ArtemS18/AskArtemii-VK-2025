import threading
import time
from sqlalchemy import text
import schedule 
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from .config import settings

engine = create_async_engine(settings.url)

async def calculate_users_popular():
    sub_q = "" \
    "SELECT users.id AS user_id, COUNT(*) AS popular " \
    "FROM users " \
    "JOIN questions ON users.id=questions.author_id " \
    "JOIN question_grade ON questions.id=question_grade.question_id " \
    "WHERE question_grade.created_at > NOW() - INTERVAL '1 week' AND question_grade.is_like = TRUE "\
    "GROUP BY users.id"

    update_q = text(
        "UPDATE users SET popular_count = c.popular " \
        f"FROM  ({sub_q}) AS c WHERE users.id = c.user_id AND users.popular_count != c.popular;"
    )
    async with engine.begin() as conn: 
        await conn.execute(update_q)
        res = await conn.execute(update_q)
        affected = res.rowcount
        print(f"calculate_users_popular executed: row affected {affected}")


async def calculate_tags_popular():
    sub_q = "SELECT qt.tag_id as tag_id, COUNT(DISTINCT q.id) AS cnt "\
            "FROM question_tags qt "\
            "JOIN questions q ON q.id = qt.question_id "\
            "WHERE q.created_at > NOW() - INTERVAL '3 months' "\
            "GROUP BY qt.tag_id "\
            
    upd_q =  text("UPDATE tags AS t "\
            "SET popular_count = s.cnt "\
            f"FROM ({sub_q}) as s "\
            "WHERE t.id = s.tag_id AND t.popular_count != s.cnt; ")
            
    async with engine.begin() as conn: 
        res = await conn.execute(upd_q)
        affected = res.rowcount
        print(f"calculate_tags_popular executed: row affected {affected}")
        
    
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


async def run():
    loop = asyncio.get_running_loop()
    def job():
        fut1 = asyncio.run_coroutine_threadsafe(calculate_users_popular(), loop)
        fut2 = asyncio.run_coroutine_threadsafe(calculate_tags_popular(), loop)
        try:
            fut1.result() 
            fut2.result()
        except Exception as e:
            print("failed:", e)

    schedule.every(settings.interval_work).seconds.do(job)

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    while True:
        await asyncio.sleep(3600)


