from pydantic import BaseModel
from pydantic import validator as field_check


class User(BaseModel):
    slug: str

    @field_check("slug")
    def normalize_slug(cls, value):
        return value
