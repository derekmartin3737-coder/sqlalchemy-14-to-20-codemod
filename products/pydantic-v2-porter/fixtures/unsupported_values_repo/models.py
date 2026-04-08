from pydantic import BaseModel, validator


class User(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, value, values):
        return value
