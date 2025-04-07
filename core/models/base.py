from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True  # Указывает, что этот класс не будет создавать свою таблицу в БД

    # Автоматическое определение имени таблицы на основе имени класса
    @declared_attr.directive
    def __tablename__(self):
        return f"{self.__class__.__name__.lower()}s"  # Например, Product → "products"

    # Универсальное поле ID для всех моделей, использующих этот базовый класс
    id: Mapped[int] = mapped_column(primary_key=True)
