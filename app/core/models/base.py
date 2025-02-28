from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self):
        return f"{self.__class__.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
