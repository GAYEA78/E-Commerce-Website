import pytest
from flask import url_for
from unittest.mock import patch, MagicMock

from app.models.product import Product
from app.services.cart import CartService
from app.services.product import ProductService
from app.models.cart import Cart, CartItem


@pytest.fixture
def mock_product():
    return Product(
        ProductID=1,
        ProductName="Chai",
        SupplierID=1,
        CategoryID=1,
        QuantityPerUnit="10 boxes x 20 bags",
        UnitPrice=18.00,
        UnitsInStock=39,
        UnitsOnOrder=0,
        ReorderLevel=10,
        Discontinued="0",
    )


@pytest.fixture
def mock_product_service(mock_product):
    class MockProductService:
        def get_product_by_id(self, product_id):
            if product_id == mock_product.ProductID:
                return mock_product
            return None

    return MockProductService()


class MockCartItem:
    """Mock cart item for testing."""
    def __init__(self, product_id, product_name, unit_price, quantity):
        self.ProductID = product_id
        self.ProductName = product_name
        self.UnitPrice = unit_price
        self.Quantity = quantity
        self.TotalPrice = unit_price * quantity


def mock_cart_service():
    """Create a mock cart service for testing."""
    service = MagicMock()
    
    # Mock cart items
    items = [
        MockCartItem(1, "Test Product", 10.0, 2),
        MockCartItem(2, "Another Product", 15.0, 1)
    ]
    
    # Set up mock methods
    service.get_cart_items.return_value = items
    service.get_cart_total.return_value = 35.0  # (10.0 * 2) + (15.0 * 1)
    service.get_item_quantity.return_value = 2
    
    # Add methods for adding, removing, and clearing items
    def add_to_cart(product_id, quantity):
        for item in items:
            if item.ProductID == product_id:
                item.Quantity += quantity
                item.TotalPrice = item.UnitPrice * item.Quantity
                return
        items.append(MockCartItem(product_id, f"Product {product_id}", 10.0, quantity))
    
    def remove_from_cart(product_id):
        nonlocal items
        items = [item for item in items if item.ProductID != product_id]
        service.get_cart_items.return_value = items
    
    def clear_cart():
        nonlocal items
        items = []
        service.get_cart_items.return_value = items
    
    service.add_to_cart = add_to_cart
    service.remove_from_cart = remove_from_cart
    service.clear_cart = clear_cart
    
    return service


def test_add_to_cart(client):
    """Test adding an item to the cart."""
    # Mock the product service to return a valid product
    with patch('app.routes.product.ProductService') as MockProductService:
        mock_product_service = MagicMock()
        MockProductService.return_value = mock_product_service
        
        # Mock the product to have sufficient inventory
        mock_product = MagicMock()
        mock_product.ProductID = 1
        mock_product.ProductName = "Test Product"
        mock_product.UnitPrice = 10.0
        mock_product.UnitsInStock = 10
        mock_product_service.get_product_by_id.return_value = mock_product
        
        # Mock the cart service
        with patch('app.routes.product.CartService') as MockCartService, \
             patch('app.routes.product.save_item_to_cart') as mock_save_item:
            mock_cart_service = MagicMock()
            MockCartService.return_value = mock_cart_service
            mock_cart_service.get_item_quantity.return_value = 0
            
            # Test adding to cart
            response = client.post('/product/1', data={'quantity': 2})
            
            # Check redirect
            assert response.status_code == 302
            
            # Verify cart service was called - in the actual implementation, save_item_to_cart is called directly
            mock_save_item.assert_called_once()


def test_view_cart(client):
    """Test viewing the cart."""
    # Create a mock cart service
    with patch('app.routes.product.CartService') as MockCartService:
        with patch('app.routes.product.get_cart') as mock_get_cart:
            # Set up mock cart
            mock_cart = MagicMock()
            mock_cart.items = {
                1: MockCartItem(1, "Test Product", 10.0, 2),
                2: MockCartItem(2, "Another Product", 15.0, 1)
            }
            mock_get_cart.return_value = mock_cart
            
            # Test viewing the cart
            response = client.get("/product/cart")
            
            # Check response
            assert response.status_code == 200
            assert b"Test Product" in response.data
            assert b"Another Product" in response.data


def test_remove_from_cart(client):
    """Test removing an item from the cart."""
    # Mock the cart service
    with patch('app.routes.product.CartService') as MockCartService:
        mock_cart_service = MagicMock()
        MockCartService.return_value = mock_cart_service
        
        # Test removing from cart
        response = client.post('/product/cart/remove/1')
        
        # Check redirect
        assert response.status_code == 302
        
        # Verify cart service was called
        mock_cart_service.remove_from_cart.assert_called_once_with(1) 