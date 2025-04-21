from faker import Faker
from pydantic import BaseModel, Field

fake = Faker("ru_RU")


class MockModel(BaseModel):
    guid: str = Field(default=fake.uuid4(), description="Unique identifier for the mock")
    uri: str = Field(default=fake.uri(), description="URI for the mock")
    method: str = Field(default=fake.http_method(), description="HTTP method for the mock")
    status_code: int = Field(
        default=fake.random_int(min=100, max=599), description="HTTP status code for the mock"
    )
    headers: dict[str, str] = Field(default={}, description="Headers for the mock")
    body: dict[str, object] = Field(default={}, description="Body for the mock")
    delay: int = Field(
        default=fake.random_int(min=0, max=5000), description="Delay in milliseconds for the mock"
    )


class MockModelWithData(MockModel):
    created_at: str = Field(
        default=fake.date_time_this_decade().isoformat(), description="Creation date and time"
    )
    updated_at: str = Field(
        default=fake.date_time_this_decade().isoformat(), description="Last update date and time"
    )
