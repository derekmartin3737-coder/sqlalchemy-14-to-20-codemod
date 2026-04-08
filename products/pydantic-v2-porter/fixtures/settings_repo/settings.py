from pydantic.v1 import BaseSettings


class AppSettings(BaseSettings):
    region: str = "us"

    class Config:
        allow_mutation = False
        schema_extra = {"title": "Settings"}
