from sqlalchemy import select, update
from app.lib.log import log_call
from app.models.users import UserORM, UserProfileORM
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserUpdate, UserWrite

@log_call
async def get_user_by_email(session: AsyncSession, email: str) -> UserORM | None:
    query = select(UserORM).where(UserORM.email==email).options(joinedload(UserORM.profile))
    raw = await session.execute(query)
    user = raw.scalar_one_or_none()
    return user


@log_call
async def get_user_by_id(session: AsyncSession, id: int) -> UserORM | None:
    query = select(UserORM).where(UserORM.id==id).options(joinedload(UserORM.profile))
    raw = await session.execute(query)
    user = raw.scalar_one_or_none()
    return user



@log_call
async def create_user(session: AsyncSession, data: UserWrite) -> UserORM:
    user = UserORM(
            email=data.email,
            hashed_password=data.hashed_password
    )
    profile = UserProfileORM(
        nickname=data.nickname,
        img_url=data.img_url
    )
    user.profile = profile
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def update_user(session: AsyncSession, user_id: int, data: UserUpdate) -> UserORM:
    updated = {k: v for k, v in data.model_dump().items() if v is not None}
    updated_user = {k: v for k, v in updated.items() if k in ("email",)}
    updated_profile = {k: v for k, v in updated.items() if k in ("nickname", "img_url")}

    query = select(UserORM).where(UserORM.id == user_id).options(joinedload(UserORM.profile))
    async with session.begin():
        raw = await session.execute(query)
        user = raw.scalar_one_or_none()
        if user is None:
            return None

        for k, v in updated_user.items():
            setattr(user, k, v)

        if updated_profile:
            if user.profile is None:
                profile = UserProfileORM(user_id=user.id, **updated_profile)
                user.profile = profile
                session.add(profile)
            else:
                for k, v in updated_profile.items():
                    setattr(user.profile, k, v)

    await session.refresh(user)
    return user