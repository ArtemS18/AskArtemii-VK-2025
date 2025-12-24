from logging import getLogger
from fastapi import Request
from fastapi.responses import RedirectResponse

from app.lib import pagination as pgn, parser
from app.models.questions import QuestionORM
from app.repository import Store
from app.schemas.error import ErrorTemplate
from app.views.base import BaseView
from app.core.config import api_path


log = getLogger(__name__)

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
        page: int,
    ):
        paginate = await self._get_question_paginate(page)
        _user_id = await self._get_user_id() 
        
        questions = await self.store.quesion.get_questions_order_by_datetime(
            limit=self.PER_PAGE, 
            offset=paginate.offset,
            user_id= _user_id
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
        page: int,
        **context
    ):
        _user_id = await self._get_user_id() 
        question_orm: QuestionORM = await self.store.quesion.get_question_by_id(id, user_id= _user_id)
        log.info("%s, %s", question_orm.answers_count, page)
       
        pagination_data = pgn.paginate(question_orm.answers_count, page, self.PER_PAGE)
        log.info("%s", pagination_data)
        return await self.template_paginate(
             "question.html", {
                "question":question_orm, 
                "answers": question_orm.answers[pagination_data.offset:pagination_data.offset+self.PER_PAGE],
                "pagination": pagination_data,
                **context
                }
            )

    async def questions_list_hots_view(
        self,
        page: int
    ):
        paginate = await self._get_question_paginate(page)
        _user_id = await self._get_user_id() 
        questions = await self.store.quesion.get_questions_order_by_hots(
            limit=self.PER_PAGE, 
            offset=paginate.offset,
            user_id= _user_id
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
        _user_id = await self._get_user_id() 
        paginate = await self._get_question_paginate(page, tag_id=tag_id)
        questions = await self.store.quesion.get_questions_by_tag(
            tag_id=tag_id, 
            limit=self.PER_PAGE, 
            offset=paginate.offset,
            user_id= _user_id
        )
        return await self.template_paginate(
             "tags_questions.html", {
                "pagination": paginate,
                "questions":questions,
                "tag": tag
                }
        )

    async def get_ask_page(self, **context):
        return await self.template_response("ask.html", context)

    async def create_question(
        self,
        title: str,
        body: str,
        user_id: int,
        tags: str | None = None,
    ):
        for k, v in {"Заголовок": title, "Текст вопроса": body}.items():
            if v is None or v.strip() == "":
                return await self.get_ask_page(
                    title=title,
                    body=body,
                    error=ErrorTemplate(text=f"Поле '{k}' должно быть заполнено"),
                )

        tag_names = parser.parse_tags(tags)
        tag_orms = await self.store.tag.get_or_create_tags(tag_names)

        q = await self.store.quesion.create_question(body, user_id, title, tags=tag_orms)

        await self.store.tag.bump_popularity([t.id for t in tag_orms])

        return RedirectResponse(f"{api_path.question}/{q.id}", status_code=303)

    async def create_answer(
            self, 
            question_id: int, 
            text: str,  
            user_id: int,
            page: int, 
        ):
        if not text:
            return await self.question_view(question_id, page, error=ErrorTemplate(text="Введите тест ответа"))
        answer = await self.store.quesion.create_answer(text, user_id, question_id)
        await self.store.centrifugo.publish(
            channel=f"question:{question_id}",
            data={
                "type": "answer.created",
                "payload": {
                    "id": answer.id,
                    "text": answer.text,
                    "author": {
                        "id": answer.author.id,
                        "nickname": answer.author.profile.nickname,
                        "img_url": answer.author.profile.img_url,
                    },
                    "created_at": answer.created_at.strftime("%d-%m-%Y %H:%M"),
                    "like_count": answer.like_count or 0,
                    "dislike_count": answer.dislike_count or 0,
                    "is_correct": answer.is_correct,
                },
            },
        )
        return RedirectResponse(f"{api_path.question}/{question_id}?page={page}", status_code=303)