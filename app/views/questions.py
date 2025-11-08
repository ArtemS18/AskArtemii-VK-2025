from fastapi import Request
from app.lib import pagination as pgn
from app.models.questions import QuestionORM
from app.views.base import BaseView
from app.repository import crud
from sqlalchemy.ext.asyncio import AsyncSession


class QuestionView(BaseView):
    def __init__(self, session: AsyncSession, req: Request):
        super().__init__(session, req)
        self.PER_PAGE = 10

    async def _get_question_paginate(self, page: int, tag_id: int | None = None) -> pgn.PaginateData:
        total = await crud.get_questions_count(self.session, tag_id=tag_id)
        paginate = pgn.paginate(total, page, self.PER_PAGE)
        return paginate
    
    async def questions_list_view(
        self,
        page: int
    ):
        paginate = await self._get_question_paginate(page)
        questions = await crud.get_questions_order_by_datetime(
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
        question: QuestionORM = await crud.get_question_by_id(self.session, id)
        pagination_data = pgn.paginate(question.answers_count, page, self.PER_PAGE)
        return await self.template_paginate(
             "question.html", {
                "question":question, 
                "answers": question.answers,
                "pagination": pagination_data
                }
            )

    async def questions_list_hots_view(
        self,
        page: int
    ):
        paginate = await self._get_question_paginate(page)
        questions = await crud.get_questions_order_by_hots(
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
        paginate = await self._get_question_paginate(page, tag_id=tag_id)
        questions = await crud.get_questions_by_tag(
            self.session, 
            tag_id=tag_id, 
            limit=self.PER_PAGE, 
            offset=paginate.offset
        )
        return await self.template_paginate(
             "hot_questions.html", {
                "pagination": paginate,
                "questions":questions
                }
        )

    async def get_ask_page(self):
        return self.template_response("ask.html", {})