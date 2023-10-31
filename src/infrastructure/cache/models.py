from typing import Optional

from pydantic import BaseModel


class InsertRedisData(BaseModel):
    name: str
    value: str
    expires: Optional[int]
