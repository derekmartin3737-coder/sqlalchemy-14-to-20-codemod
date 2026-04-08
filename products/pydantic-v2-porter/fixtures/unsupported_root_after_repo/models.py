from pydantic import BaseModel, root_validator


class User(BaseModel):
    slug: str

    @root_validator
    def normalize_values(cls, values):
        return values
