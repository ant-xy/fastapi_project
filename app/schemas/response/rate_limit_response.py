from pydantic import BaseModel

class RateLimited(BaseModel):
    status: int
    message: str

