from pydantic import BaseModel


class Product(BaseModel):
    ProductID: int
    ProductName: str
    SupplierID: int
    CategoryID: int
    QuantityPerUnit: str
    UnitPrice: float
    UnitsInStock: int
    UnitsOnOrder: int
    ReorderLevel: int
    Discontinued: str


class CartItem(BaseModel):
    ProductID: int
    Quantity: int
    ProductName: str
    TotalPrice: float

    def to_dict(self):
        return {
            "ProductID": self.ProductID,
            "Quantity": self.Quantity,
            "ProductName": self.ProductName,
            "TotalPrice": self.TotalPrice
        }


class Cart(BaseModel):
    items: dict[int, CartItem]

    def to_dict(self):
        return {
            "items": {k: v.to_dict() for k, v in self.items.items()}
        }
