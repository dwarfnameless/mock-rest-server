from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.mock_model import MockData, MockModelWithDate
from src.db import DBManager
from src.db.models.mock_data import MockDbData


@DBManager.with_session
async def get_all_mock_data(session: AsyncSession) -> list[MockModelWithDate] | None:
    """
    Получить все mock-данные из базы данных.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        list[MockModelWithDate] | None: Список моделей mock-данных с датой, либо None, если данных нет.
    """
    res = await session.execute(select(MockDbData))
    db_mocks_data = res.scalars().all()

    return [MockModelWithDate.model_validate(mock) for mock in db_mocks_data] if db_mocks_data else None


@DBManager.with_session
async def get_mock_data_by_uuid(session: AsyncSession, uuid: UUID) -> MockModelWithDate | None:
    """
    Получить mock-данные по UUID.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        uuid (UUID): UUID mock-данных.

    Returns:
        MockModelWithDate | None: Модель mock-данных с датой, либо None, если не найдено.
    """
    res = await session.execute(select(MockDbData).where(MockDbData.uuid == uuid))
    db_mock_data = res.scalar_one_or_none()
    return MockModelWithDate.model_validate(db_mock_data) if db_mock_data else None


@DBManager.with_session
async def get_last_mock_data_by_uri_and_method(
    session: AsyncSession, uri: str, method: str
) -> MockModelWithDate | None:
    """
    Получить последние mock-данные по URI и методу.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        uri (str): URI mock-данных.
        method (str): Метод mock-данных.

    Returns:
        MockModelWithDate | None: Модель mock-данных, либо None, если не найдено.
    """
    res = await session.execute(
        select(MockDbData)
        .where(MockDbData.uri == uri)
        .where(MockDbData.method == method)
        .order_by(MockDbData.created_at.desc())
    )
    db_mock_data = res.scalar_one_or_none()
    return MockModelWithDate.model_validate(db_mock_data) if db_mock_data else None


@DBManager.with_session
async def create_mock_data(session: AsyncSession, mock_data: MockData) -> MockModelWithDate:
    """
    Создать новые mock-данные в базе данных.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        mock_data (MockData): Данные для создания mock-объекта.

    Returns:
        MockModelWithDate: Созданная модель mock-данных с датой.
    """
    db_mock = MockDbData(
        uuid=uuid4(),
        uri=mock_data.uri,
        method=mock_data.method,
        status_code=mock_data.status_code,
        headers=mock_data.headers,
        body=mock_data.body,
        delay=mock_data.delay,
    )
    session.add(db_mock)
    await session.flush()
    await session.refresh(db_mock)

    return MockModelWithDate.model_validate(db_mock)


@DBManager.with_session
async def delete_mock_data(session: AsyncSession, uuid: UUID) -> bool:
    """
    Удалить mock-данные по UUID.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.
        uuid (UUID): UUID mock-данных для удаления.

    Returns:
        bool: True, если удаление прошло успешно, иначе False.
    """
    res = await session.execute(select(MockDbData).where(MockDbData.uuid == uuid))
    db_mock_data = res.scalar_one_or_none()
    if db_mock_data:
        await session.delete(db_mock_data)
        await session.commit()
        return True
    return False
