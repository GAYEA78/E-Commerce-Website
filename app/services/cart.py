import secrets
from datetime import datetime, timedelta
from typing import Optional

from flask import session

from app.models.cart import Cart, CartItem
from app.utils.database import get_db
from app.utils.logger import setup_logger

log = setup_logger(__name__)


def get_session_id() -> str:
    """Get or create a session ID for the current user."""
    if "session_id" not in session:
        session["session_id"] = secrets.token_hex(16)
    return session["session_id"]


class CartService:
    def __init__(self):
        self.db = get_db()
        self.cursor = self.db.cursor()

    def add_to_cart(self, product_id: int, quantity: int) -> None:
        """Add or update an item in the shopping cart."""
        session_id = get_session_id()

        # Check if item already exists in cart
        self.cursor.execute(
            """
            SELECT Quantity FROM Shopping_Cart 
            WHERE SessionID = ? AND ProductID = ?
            """,
            (session_id, product_id),
        )
        result = self.cursor.fetchone()

        if result:
            # Update existing item
            new_quantity = result[0] + quantity
            self.cursor.execute(
                """
                UPDATE Shopping_Cart 
                SET Quantity = ?, AddedAt = CURRENT_TIMESTAMP
                WHERE SessionID = ? AND ProductID = ?
                """,
                (new_quantity, session_id, product_id),
            )
        else:
            # Add new item
            self.cursor.execute(
                """
                INSERT INTO Shopping_Cart (SessionID, ProductID, Quantity)
                VALUES (?, ?, ?)
                """,
                (session_id, product_id, quantity),
            )

        self.db.commit()

    def get_cart_items(self) -> list[CartItem]:
        """Get all items in the current user's cart."""
        session_id = get_session_id()

        self.cursor.execute(
            """
            SELECT sc.ProductID, sc.Quantity, p.ProductName, p.UnitPrice
            FROM Shopping_Cart sc
            JOIN Products p ON sc.ProductID = p.ProductID
            WHERE sc.SessionID = ?
            """,
            (session_id,),
        )

        items = []
        for row in self.cursor.fetchall():
            product_id, quantity, name, unit_price = row
            items.append(
                CartItem(
                    ProductID=product_id,
                    Quantity=quantity,
                    ProductName=name,
                    TotalPrice=quantity * unit_price,
                )
            )

        return items

    def cleanup_old_carts(self, days: int = 30) -> None:
        """Remove cart items older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)

        self.cursor.execute(
            "DELETE FROM Shopping_Cart WHERE AddedAt < ?", (cutoff_date.isoformat(),)
        )
        self.db.commit()

    def clear_cart(self, session_id: Optional[str] = None) -> None:
        """Clear all items from the cart for a given session."""
        session_id = session_id or get_session_id()

        self.cursor.execute("DELETE FROM Shopping_Cart WHERE SessionID = ?", (session_id,))
        self.db.commit()

    def remove_from_cart(self, product_id: int) -> None:
        """Remove an item from the shopping cart."""
        session_id = get_session_id()

        self.cursor.execute(
            """
            DELETE FROM Shopping_Cart 
            WHERE SessionID = ? AND ProductID = ?
            """,
            (session_id, product_id),
        )
        self.db.commit()

    def get_item_quantity(self, product_id: int) -> int:
        """Get the quantity of a specific item in the cart."""
        session_id = get_session_id()

        self.cursor.execute(
            """
            SELECT Quantity FROM Shopping_Cart 
            WHERE SessionID = ? AND ProductID = ?
            """,
            (session_id, product_id),
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0


# Keep the session-based cart functions for now, but they should be updated to use CartService
def get_cart() -> Cart:
    cart_service = CartService()
    items = cart_service.get_cart_items()
    return Cart(items={item.ProductID: item for item in items})


def save_item_to_cart(cart_item: CartItem) -> None:
    cart_service = CartService()
    cart_service.add_to_cart(cart_item.ProductID, cart_item.Quantity)
