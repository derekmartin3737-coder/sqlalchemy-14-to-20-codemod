from pydantic import BaseModel, validate_arguments, validator


class User(BaseModel):
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @validator("name")
    def validate_name(cls, value):
        return value.strip()


@validate_arguments
def make_user(name: str) -> User:
    return User(name=name)
