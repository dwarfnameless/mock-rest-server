from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models.mock_model import MockData, MockModelWithDate
from src.db import DBManager
from src.db.models.mock_data import MockDbData


@DBManager.with_session
async def get_all_mock_data(session: AsyncSession) -> list[MockModelWithDate] | None:
    res = await session.execute(select(MockDbData))
    db_mocks_data = res.scalars().all()

    return [MockModelWithDate.model_validate(mock) for mock in db_mocks_data] if db_mocks_data else None


@DBManager.with_session
async def get_mock_data_by_uuid(session: AsyncSession, uuid: UUID) -> MockModelWithDate | None:
    res = await session.execute(select(MockDbData).where(MockDbData.uuid == uuid))
    db_mock_data = res.scalar_one_or_none()
    return MockModelWithDate.model_validate(db_mock_data) if db_mock_data else None


@DBManager.with_session
async def create_mock_data(session: AsyncSession, mock_data: MockData) -> MockModelWithDate:
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
    res = await session.execute(select(MockDbData).where(MockDbData.uuid == uuid))
    db_mock_data = res.scalar_one_or_none()
    if db_mock_data:
        await session.delete(db_mock_data)
        await session.commit()
        return True
    return False


# async def update_mock_data(params: str) -> MockModelWithDate: ...
