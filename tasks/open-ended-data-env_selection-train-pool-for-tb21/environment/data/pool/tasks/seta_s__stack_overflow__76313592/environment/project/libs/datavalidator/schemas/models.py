from pydantic import BaseModel, validator


class InputSchema(BaseModel):
    id: int
    name: str
    email: str = ""
    score: float = 0.0
    tags: list = []
    metadata: dict = {}

    class Config:
        extra = "allow"

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('name must not be empty')
        return v.strip()

    @validator('email')
    def email_format(cls, v):
        if v and '@' not in v:
            raise ValueError('invalid email format')
        return v


class OutputSchema(BaseModel):
    id: int
    name: str
    email: str = ""
    score: float = 0.0
    tags: list = []
    status: str = "processed"
    valid: bool = True
