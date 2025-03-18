from typing import Optional

from app.models.supplier import Supplier
from app.utils.database import get_db


class SupplierService:
    def __init__(self):
        self.cursor = get_db().cursor()
        self.columns = list(Supplier.model_fields.keys())

    def get_supplier_by_id(self, supplier_id: Optional[int]) -> Optional[Supplier]:
        if supplier_id is None:
            return None
        self.cursor.execute("SELECT * FROM Suppliers WHERE SupplierID = ?", (supplier_id,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        supplier: Supplier = Supplier.model_validate(dict(zip(self.columns, result)))
        return supplier
