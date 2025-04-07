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


async def delete_record(
        record: T,
        session: AsyncSession,
):
    await session.delete(record)
    await session.commit()


# Универсальная зависимость для получения объекта по ID с 404
def get_object_by_id_or_404(
    model: Type[T],
    id_name: str,
    get_func: Callable[[AsyncSession, int], Awaitable[T | None]],
):
    async def dependency(
        object_id: int = Path(..., alias=id_name),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> T:
        obj = await get_func(session, object_id)
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return obj

    return dependency
