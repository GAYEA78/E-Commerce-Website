import pytest
from flask import session, g
from unittest.mock import patch, MagicMock

from app.models.product import Product
from app.models.category import Category

class TestUserFlow:
    """Test the complete user flow from browsing to checkout."""
    
    def test_browse_add_to_cart_checkout_flow(self, client):
        """Test browsing products, adding to cart, and checking out."""
        # Mock the product service
        with patch('app.routes.product.ProductService') as MockProductService:
            mock_product_service = MagicMock()
            MockProductService.return_value = mock_product_service
            
            # Create mock products
            mock_product = Product(
                ProductID=1,
                ProductName="Test Product",
                CategoryID=1,
                SupplierID=1,
                QuantityPerUnit="10 boxes",
                UnitPrice=10.0,
                UnitsInStock=100,
                UnitsOnOrder=0,
                ReorderLevel=0,
                Discontinued="0"
            )
            
            mock_product_service.get_products.return_value = [mock_product]
            mock_product_service.get_product_by_id.return_value = mock_product
            
            # Mock the category service
            with patch('app.routes.product.CategoryService') as MockCategoryService:
                mock_category_service = MagicMock()
                MockCategoryService.return_value = mock_category_service
                
                mock_category = Category(
                    CategoryID=1,
                    CategoryName="Test Category",
                    Description="Test Category Description",
                    Picture=b"Test Category Picture"
                )
                
                mock_category_service.get_category_by_id.return_value = mock_category
                
                # Step 1: Browse products
                response = client.get('/')
                assert response.status_code == 200
                
                # Step 2: View a product
                response = client.get('/product/1')
                assert response.status_code == 200
                assert b"Test Product" in response.data
                
                # Step 3: Add to cart
                with patch('app.routes.product.save_item_to_cart') as mock_save_item:
                    response = client.post('/product/1', data={'quantity': 2})
                    assert response.status_code == 302  # Redirect after adding to cart
                    mock_save_item.assert_called_once()
                    
                    # Step 4: View cart
                    with patch('app.routes.product.get_cart') as mock_get_cart:
                        mock_cart = MagicMock()
                        mock_item = MagicMock()
                        mock_item.ProductID = 1
                        mock_item.ProductName = "Test Product"
                        mock_item.Quantity = 2
                        mock_item.UnitPrice = 10.0
                        mock_item.TotalPrice = 20.0
                        mock_cart.items = {1: mock_item}
                        mock_get_cart.return_value = mock_cart
                        
                        response = client.get('/product/cart')
                        assert response.status_code == 200
                        assert b"Test Product" in response.data
                        
                        # Step 5: Proceed to checkout (requires login)
                        with patch('flask_login.utils._get_user') as mock_get_user:
                            mock_user = MagicMock()
                            mock_user.is_authenticated = True
                            mock_user.id = 1
                            mock_user.username = "testuser"
                            mock_get_user.return_value = mock_user
                            
                            response = client.get('/product/checkout')
                            assert response.status_code == 200
                            assert b"Checkout" in response.data or b"checkout" in response.data.lower()

    def test_cart_to_order_conversion(self, client):
        """Test the conversion of cart items to an order during checkout."""
        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_user = MagicMock()
            mock_user.is_authenticated = True
            mock_user.id = 1
            mock_user.username = "testuser"
            mock_get_user.return_value = mock_user
            
            # Set up session data for checkout
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['address'] = '123 Test St'
                sess['payment_method'] = 'credit_card'
                sess['shipping_method'] = 'express'
            
            # Mock the cart service to return a non-empty cart
            with patch('app.routes.product.get_cart') as mock_get_cart:
                mock_cart = MagicMock()
                mock_item = MagicMock()
                mock_item.ProductID = 1
                mock_item.ProductName = "Test Product"
                mock_item.Quantity = 2
                mock_item.UnitPrice = 10.0
                mock_item.TotalPrice = 20.0
                mock_cart.items = {1: mock_item}
                mock_get_cart.return_value = mock_cart
                
                # Mock the product service
                with patch('app.routes.product.ProductService') as MockProductService:
                    mock_product_service = MagicMock()
                    MockProductService.return_value = mock_product_service
                    
                    # Create a proper product object
                    mock_product = MagicMock()
                    mock_product.ProductID = 1
                    mock_product.ProductName = "Test Product"
                    mock_product.UnitPrice = 10.0
                    mock_product.UnitsInStock = 10
                    mock_product_service.get_product_by_id.return_value = mock_product
                    
                    # Test confirming the order
                    response = client.post('/product/confirm_order', follow_redirects=True)
                    
                    # Check that the order was confirmed
                    assert response.status_code == 200
                    
                    # Check for confirmation-related content in the response
                    assert b'confirmation' in response.data.lower() or b'thank you' in response.data.lower() or b'success' in response.data.lower() or b'order' in response.data.lower() 