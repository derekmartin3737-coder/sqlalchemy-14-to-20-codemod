from pydantic import BaseModel


class User(BaseModel):
    slug: str

    class Config:
        fields = {"slug": {"alias": "user_slug"}}
