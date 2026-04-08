from pydantic import BaseModel, validator


class User(BaseModel):
    tags: list[str]

    @validator("tags", each_item=True)
    def validate_tag(cls, value):
        return value
