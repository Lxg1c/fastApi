from typing import List

from pydantic import EmailStr
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.schemas import CreateUser, UserSchema
from core.models.user import User


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def create_user(
    session: AsyncSession,
    user: CreateUser,
) -> UserSchema:
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return UserSchema.model_validate(new_user.__dict__, from_attributes=True)


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_username(
    session: AsyncSession, username: str
) -> UserSchema | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return UserSchema.model_validate(user) if user else None


async def get_user_by_email(
    session: AsyncSession,
    email: EmailStr,
) -> UserSchema | None:
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return UserSchema.model_validate(user) if user else None
