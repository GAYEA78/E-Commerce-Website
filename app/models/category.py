from pydantic import BaseModel


class Category(BaseModel):
    CategoryID: int
    CategoryName: str
    Description: str
    Picture: bytes
