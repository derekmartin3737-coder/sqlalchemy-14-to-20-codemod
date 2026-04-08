from pydantic.v1 import BaseModel, validator


class User(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, value):
        return value
