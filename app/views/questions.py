from fastapi import Request
from app.lib import pagination as pgn
from app.models.questions import QuestionORM
from app.views.base import BaseView
from app.core.config import api_path
from app.repository.db import question
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from app.models.answers import AnswerORM

class QuestionView(BaseView):
    def __init__(self, session: AsyncSession, req: Request):
        super().__init__(session, req)
        self.PER_PAGE = 10

    async def _get_question_paginate(self, page: int, tag_id: int | None = None) -> pgn.PaginateData:
        total = await question.get_questions_count(self.session, tag_id=tag_id)
        paginate = pgn.paginate(total, page, self.PER_PAGE)
        return paginate
    
    async def questions_list_view(
        self,
        page: int
    ):
        paginate = await self._get_question_paginate(page)
        questions = await question.get_questions_order_by_datetime(
            self.session, 
            limit=self.PER_PAGE, 
            offset=paginate.offset
        )
        return await self.template_paginate(
            "index.html", {
                "pagination": paginate,
                "questions":questions
                }
        )

    async def question_view(
        self,
        id: int, 
        page: int
    ):
        question_orm: QuestionORM = await question.get_question_by_id(self.session, id)
        pagination_data = pgn.paginate(question_orm.answers_count, page, self.PER_PAGE)
        return await self.template_paginate(
             "question.html", {
                "question":question_orm, 
                "answers": question_orm.answers,
                "pagination": pagination_data
                }
            )

    async def questions_list_hots_view(
        self,
        page: int
    ):
        paginate = await self._get_question_paginate(page)
        questions = await question.get_questions_order_by_hots(
            self.session, 
            limit=self.PER_PAGE, 
            offset=paginate.offset
        )

        return await self.template_paginate(
             "hot_questions.html", {
                "pagination": paginate,
                "questions":questions
                }
        )

    async def questions_list_tags_view(
        self,
        tag_id: int, 
        page: int
    ):
        tag = await question.get_tag_by_id(self.session, tag_id)
        paginate = await self._get_question_paginate(page, tag_id=tag_id)
        questions = await question.get_questions_by_tag(
            self.session, 
            tag_id=tag_id, 
            limit=self.PER_PAGE, 
            offset=paginate.offset
        )
        return await self.template_paginate(
             "tags_questions.html", {
                "pagination": paginate,
                "questions":questions,
                "tag": tag
                }
        )

    async def get_ask_page(self):
        return await self.template_response("ask.html", {})

    async def create_question(
            self, 
            title: str, 
            body: str, 
            user_id: int, 
            tags: str | None = None
        ):
        q = QuestionORM(title=title, text=body, author_id=user_id)
        self.session.add(q)
        await self.session.commit()
        await self.session.refresh(q)

        return RedirectResponse(f"{api_path.question}/{q.id}", status_code=303)

    async def create_answer(
            self, 
            question_id: int, 
            text: str,  
            user_id: int
        ):
        a = AnswerORM(text=text, author_id=user_id, question_id=question_id)
        self.session.add(a)
        await self.session.commit()
        await self.session.refresh(a)
        return RedirectResponse(f"{api_path.question}/{question_id}", status_code=303)