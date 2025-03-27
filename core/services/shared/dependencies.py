from typing import List, Type, TypeVar

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


async def get_all_records(
        session: AsyncSession,
        model: Type[T],
) -> List[T]:
    stmt = select(model).order_by(model.id)
    result: Result = await session.execute(stmt)
    records = result.scalars().all()
    return list(records)


async def create_record(
        session: AsyncSession,
        model: Type[T],
        data: dict,
) -> T:
    record = model(**data)
    session.add(record)
    await session.commit()
    return record


async def update_record(
        session: AsyncSession,
        record: T,
        update_data: dict,
        partial: bool = False,
) -> T:
    for name, value in update_data.items():
        setattr(record, name, value)
    await session.commit()
    return record
