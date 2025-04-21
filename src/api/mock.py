from fastapi import APIRouter
from fastapi.params import Query

from src.api.models.mock import MockModelWithData

router = APIRouter()


@router.get("/mock", response_model=MockModelWithData | list[MockModelWithData])
async def get_mock(
    guid: str | None = Query(default=None),
) -> MockModelWithData | list[MockModelWithData]:
    if guid is None:
        return [MockModelWithData() for _ in range(5)]

    return MockModelWithData()


# @router.post("/mock", response_model=MockModelWithData)

# @router.put("/mock", response_model=MockModelWithData)

# @router.patch("/mock", response_model=MockModelWithData)

# @router.delete("/mock")
