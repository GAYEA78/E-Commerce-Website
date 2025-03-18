from pydantic import BaseModel


class CartItem(BaseModel):
    ProductID: int
    Quantity: int
    ProductName: str
    TotalPrice: float


class Cart(BaseModel):
    items: dict[int, CartItem]
