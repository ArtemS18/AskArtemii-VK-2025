from app.views.base import BaseView


class AuthoView(BaseView):
    async def login(self):
        template = await self.template_response("login.html")
        return template

    async def signup(self):
        template = await self.template_response("signup.html")
        return template

