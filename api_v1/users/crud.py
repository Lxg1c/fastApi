from typing import List

from pydantic import EmailStr
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import CreateUser
from core.models.user import User
from core.services.shared.dependencies import get_all_records, create_record


async def get_users(session: AsyncSession) -> List[User]:
    return await get_all_records(session, User)


async def get_user_by_username(session: AsyncSession, username: str, ) -> User:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: EmailStr) -> User:
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


# Получить пользователя по phone
async def get_user_by_phone(session: AsyncSession, phone: str) -> User:
    stmt = select(User).where(User.phone == phone)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


# Создать пользователя
async def create_user(
        session: AsyncSession,
        user: CreateUser,
) -> User:
    return await create_record(session, User, user.model_dump())


# Удалить пользователя
async def delete_user(
        user: User,
        session: AsyncSession,
):
    await delete_record(record=user, session=session)
