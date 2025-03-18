from app.models.cart import Cart, CartItem
from app.services.cart import get_cart, save_item_to_cart

# Need client fixture because we are working with session data, which requires a request context.


def test_get_cart_creates_new_cart(client):
    with client:
        client.get("/")  # Creates session context
        cart = get_cart()
        assert isinstance(cart, Cart)
        assert len(cart.items) == 0


def test_get_cart_returns_existing_cart(client):
    with client:
        client.get("/")
        cart_item = CartItem(ProductID=1, ProductName="Chai", Quantity=2, TotalPrice=36.0)
        save_item_to_cart(cart_item)

        cart = get_cart()
        assert isinstance(cart, Cart)
        assert len(cart.items) == 1
        assert cart.items[1].ProductID == 1
        assert cart.items[1].Quantity == 2


def test_save_item_to_cart(client):
    with client:
        client.get("/")
        cart_item = CartItem(ProductID=1, ProductName="Chai", Quantity=2, TotalPrice=36.0)
        save_item_to_cart(cart_item)

        cart = get_cart()
        assert len(cart.items) == 1
        assert cart.items[1].ProductID == 1
        assert cart.items[1].Quantity == 2


def test_save_item_updates_existing_cart(client):
    with client:
        client.get("/")
        # Add first item
        save_item_to_cart(CartItem(ProductID=1, ProductName="Chai", Quantity=2, TotalPrice=36.0))
        # Add second item
        save_item_to_cart(CartItem(ProductID=2, ProductName="Chang", Quantity=3, TotalPrice=57.0))

        cart = get_cart()
        assert len(cart.items) == 2
        assert cart.items[1].Quantity == 2
        assert cart.items[2].Quantity == 3
