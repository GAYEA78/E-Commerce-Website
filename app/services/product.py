from typing import Optional

from app.models.product import Product
from app.utils.database import get_db
from app.utils.logger import setup_logger

log = setup_logger(__name__)


class ProductService:

    def __init__(self):
        self.cursor = get_db().cursor()
        self.columns = list(Product.model_fields.keys())

    def get_all_products(self) -> list[Product]:
        self.cursor.execute("SELECT * FROM Products")
        products: list[Product] = [
            Product.model_validate(dict(zip(self.columns, row))) for row in self.cursor.fetchall()
        ]
        return products

    def get_product_by_id(self, product_id: Optional[int]) -> Optional[Product]:
        if product_id is None:
            return None
        self.cursor.execute("SELECT * FROM Products WHERE ProductID = ?", (product_id,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        product: Product = Product.model_validate(dict(zip(self.columns, result)))
        return product

    def search_products(self, search_term: str) -> list[Product]:
        """Search for products by name or description."""
        if not search_term:
            return self.get_all_products()
            
        # Use LIKE for case-insensitive search with wildcards
        search_pattern = f"%{search_term}%"
        self.cursor.execute(
            """
            SELECT * FROM Products 
            WHERE ProductName LIKE ? OR QuantityPerUnit LIKE ?
            ORDER BY ProductName
            """, 
            (search_pattern, search_pattern)
        )
        
        products: list[Product] = [
            Product.model_validate(dict(zip(self.columns, row))) for row in self.cursor.fetchall()
        ]
        return products
        
    def get_products_by_category(self, category_id: int) -> list[Product]:
        """Get all products in a specific category."""
        self.cursor.execute(
            """
            SELECT * FROM Products 
            WHERE CategoryID = ? 
            ORDER BY ProductName
            """, 
            (category_id,)
        )
        
        products: list[Product] = [
            Product.model_validate(dict(zip(self.columns, row))) for row in self.cursor.fetchall()
        ]
        return products

    def update_product_inventory(self, product_id: int, quantity: int) -> bool:
        """Update product inventory by decreasing the UnitsInStock.
        
        Args:
            product_id: The ID of the product to update
            quantity: The quantity to decrease from inventory
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            # First check if there's enough inventory
            product = self.get_product_by_id(product_id)
            if not product or product.UnitsInStock < quantity:
                log.error(f"Not enough inventory for product {product_id}. Available: {product.UnitsInStock if product else 0}, Requested: {quantity}")
                return False
                
            # Update the inventory
            self.cursor.execute(
                """
                UPDATE Products 
                SET UnitsInStock = UnitsInStock - ? 
                WHERE ProductID = ?
                """, 
                (quantity, product_id)
            )
            get_db().commit()
            log.info(f"Updated inventory for product {product_id}. New stock: {product.UnitsInStock - quantity}")
            return True
        except Exception as e:
            log.error(f"Error updating product inventory: {e}")
            return False
