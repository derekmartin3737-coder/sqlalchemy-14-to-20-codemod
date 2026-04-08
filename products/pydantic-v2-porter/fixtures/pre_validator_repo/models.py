from pydantic import BaseModel, validator


class User(BaseModel):
    slug: str

    @validator("slug", pre=True, allow_reuse=True)
    def normalize_slug(cls, value):
        return value.strip().lower()
