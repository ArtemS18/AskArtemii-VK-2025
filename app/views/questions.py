from fastapi import Request
from app.lib import pagination as pgn
from app.models.questions import QuestionORM
from app.repository import Store
from app.views.base import BaseView
from app.core.config import api_path
from fastapi.responses import RedirectResponse

class QuestionView(BaseView):
    def __init__(self, request: Request, store: Store):
        super().__init__(request, store)
        self.PER_PAGE = 10

    async def _get_question_paginate(self, page: int, tag_id: int | None = None) -> pgn.PaginateData:
        total = await self.store.quesion.get_questions_count(tag_id=tag_id)
        paginate = pgn.paginate(total, page, self.PER_PAGE)
        return paginate
    
    async def questions_list_view(
        self,
        page: int
    ):
        paginate = await self._get_question_paginate(page)
        questions = await self.store.quesion.get_questions_order_by_datetime(
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
        question_orm: QuestionORM = await self.store.quesion.get_question_by_id(id)
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
        questions = await self.store.quesion.get_questions_order_by_hots(
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
        tag = await self.store.tag.get_tag_by_id(tag_id)
        paginate = await self._get_question_paginate(page, tag_id=tag_id)
        questions = await self.store.quesion.get_questions_by_tag(
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
            tags: str | None = None # TODO: fix
        ):
        q = await self.store.quesion.create_question(body, user_id, title)
        return RedirectResponse(f"{api_path.question}/{q.id}", status_code=303)

    async def create_answer(
            self, 
            question_id: int, 
            text: str,  
            user_id: int
        ):
        await self.store.quesion.create_answer(text, user_id, question_id)
        return RedirectResponse(f"{api_path.question}/{question_id}", status_code=303)