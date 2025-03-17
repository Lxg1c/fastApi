from typing import List
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.users.schemas import CreateUser, UserSchema
from core.models.user import User


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)

async def get_user_by_username(session: AsyncSession, username: str,) -> User:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(
    session: AsyncSession,
    user: CreateUser,
) -> User:
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user