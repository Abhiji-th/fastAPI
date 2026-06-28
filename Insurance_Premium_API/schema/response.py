from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Dict

class Response(BaseModel):
    predicted_class: str = Field(...)
    confidence: float = Field(...)
    categories: Dict[str, float] = Field(...)