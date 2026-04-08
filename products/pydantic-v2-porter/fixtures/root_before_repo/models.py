from pydantic import BaseModel, root_validator


class User(BaseModel):
    slug: str

    @root_validator(pre=True)
    def normalize_values(cls, values):
        if "slug" in values:
            values["slug"] = values["slug"].strip()
        return values
