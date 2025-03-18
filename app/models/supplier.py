from typing import Optional

from pydantic import BaseModel


class Supplier(BaseModel):
    SupplierID: int
    CompanyName: str
    ContactName: Optional[str]
    ContactTitle: Optional[str]
    Address: Optional[str]
    City: Optional[str]
    Region: Optional[str]
    PostalCode: Optional[str]
    Country: Optional[str]
    Phone: Optional[str]
    Fax: Optional[str]
    HomePage: Optional[str]
