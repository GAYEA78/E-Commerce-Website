import pytest
from unittest.mock import patch, MagicMock
from flask import session

def test_checkout_get_not_logged_in(client):
    """Test that checkout redirects to login if not logged in."""
    response = client.get('/product/checkout')
    assert response.status_code == 302
    assert '/' in response.location

def test_checkout_post_success(client, app):
    """Test successful checkout form submission."""
    with app.app_context():
        # Set up a logged-in session
        with client.session_transaction() as sess:
            sess['user_id'] = 'TESTID'
        
        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_get_user.return_value = MagicMock(is_authenticated=True)
            
            # Mock the cart service to return a non-empty cart
            with patch('app.routes.product.get_cart') as mock_get_cart:
                mock_cart = MagicMock()
                mock_cart.items = {'1': MagicMock(TotalPrice=10.0)}
                mock_get_cart.return_value = mock_cart
                
                # Submit the checkout form
                response = client.post('/product/checkout', data={
                    'address': '123 Test St',
                    'payment_method': 'credit_card'
                }, follow_redirects=True)
                
                # Check that the user was redirected to the shipping page
                assert response.status_code == 200
                assert b'Shipping' in response.data or b'shipping' in response.data

def test_choose_shipping_get_not_logged_in(client):
    """Test that shipping page redirects to login if not logged in."""
    response = client.get('/product/choose_shipping')
    assert response.status_code == 302
    assert '/login' in response.location

def test_choose_shipping_get_logged_in(client, app):
    """Test that shipping page loads correctly when logged in."""
    with app.app_context():
        # Set up a logged-in session with checkout data
        with client.session_transaction() as sess:
            sess['user_id'] = 'TESTID'
            sess['address'] = '123 Test St'
            sess['payment_method'] = 'credit_card'
        
        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_get_user.return_value = MagicMock(is_authenticated=True)
            
            response = client.get('/product/choose_shipping')
            
            # Check that the shipping page loads
            assert response.status_code == 200
            assert b'Shipping' in response.data or b'shipping' in response.data

def test_choose_shipping_post_success(client, app):
    """Test successful shipping method selection."""
    with app.app_context():
        # Set up a logged-in session with checkout data
        with client.session_transaction() as sess:
            sess['user_id'] = 'TESTID'
            sess['address'] = '123 Test St'
            sess['payment_method'] = 'credit_card'
        
        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_get_user.return_value = MagicMock(is_authenticated=True)
            
            # Submit the shipping form
            response = client.post('/product/choose_shipping', data={
                'shipping_method': 'express'
            }, follow_redirects=True)
            
            # Check that the user was redirected to the order confirmation page
            assert response.status_code == 200
            assert b'Order Confirmation' in response.data or b'Confirm' in response.data or b'confirm' in response.data

def test_confirm_order_get_not_logged_in(client):
    """Test that order confirmation redirects to login if not logged in."""
    response = client.get('/product/confirm_order')
    assert response.status_code == 302
    assert '/login' in response.location

def test_confirm_order_get_missing_info(client, app):
    """Test that order confirmation redirects to checkout if missing information."""
    with app.app_context():
        # Set up a logged-in session with incomplete checkout data
        with client.session_transaction() as sess:
            sess['user_id'] = 'TESTID'
            # Missing address, payment_method, or shipping_method
        
        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_get_user.return_value = MagicMock(is_authenticated=True)
            
            response = client.get('/product/confirm_order')
            
            # Check that the user was redirected to checkout
            assert response.status_code == 302
            assert '/product/checkout' in response.location

def test_confirm_order_get_success(client, app):
    """Test that order confirmation page loads correctly with complete information."""
    with app.app_context():
        # Set up a logged-in session with complete checkout data
        with client.session_transaction() as sess:
            sess['user_id'] = 'TESTID'
            sess['address'] = '123 Test St'
            sess['payment_method'] = 'credit_card'
            sess['shipping_method'] = 'express'

        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_get_user.return_value = MagicMock(is_authenticated=True)

            # Mock the cart service to return a non-empty cart
            with patch('app.routes.product.get_cart') as mock_get_cart:
                mock_cart = MagicMock()
                mock_item = MagicMock()
                mock_item.ProductID = 1
                mock_item.Quantity = 2
                mock_item.TotalPrice = 10.0
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
                    
                    # Test loading the order confirmation page
                    response = client.get('/product/confirm_order')
                    
                    # Check that the page loaded successfully
                    assert response.status_code == 200
                    assert b'confirm' in response.data.lower() or b'order' in response.data.lower()

def test_confirm_order_post_success(client, app):
    """Test successful order confirmation with inventory update."""
    with app.app_context():
        # Set up a logged-in session with complete checkout data
        with client.session_transaction() as sess:
            sess['user_id'] = 'TESTID'
            sess['address'] = '123 Test St'
            sess['payment_method'] = 'credit_card'
            sess['shipping_method'] = 'express'
        
        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_get_user.return_value = MagicMock(is_authenticated=True)
            
            # Mock the cart service to return a non-empty cart
            with patch('app.routes.product.get_cart') as mock_get_cart:
                mock_cart = MagicMock()
                mock_item = MagicMock()
                mock_item.ProductID = 1
                mock_item.Quantity = 2
                mock_item.TotalPrice = 10.0
                mock_cart.items = {1: mock_item}
                mock_get_cart.return_value = mock_cart
                
                # Mock the product service to check and update inventory
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
                    
                    # Mock the inventory update to succeed
                    mock_product_service.update_product_inventory.return_value = True
                    
                    # Test confirming the order
                    response = client.post('/product/confirm_order', follow_redirects=True)
                    
                    # Check that the order was confirmed successfully
                    assert response.status_code == 200
                    
                    # Check for confirmation-related content in the response
                    assert b'confirmation' in response.data.lower() or b'thank you' in response.data.lower() or b'success' in response.data.lower()

def test_confirm_order_post_insufficient_inventory(client, app):
    """Test order confirmation with insufficient inventory."""
    with app.app_context():
        # Set up a logged-in session with complete checkout data
        with client.session_transaction() as sess:
            sess['user_id'] = 'TESTID'
            sess['address'] = '123 Test St'
            sess['payment_method'] = 'credit_card'
            sess['shipping_method'] = 'express'
        
        # Mock the authenticated user
        with patch('flask_login.utils._get_user') as mock_get_user:
            mock_get_user.return_value = MagicMock(is_authenticated=True)
            
            # Mock the cart service to return a non-empty cart
            with patch('app.routes.product.get_cart') as mock_get_cart:
                mock_cart = MagicMock()
                mock_item = MagicMock()
                mock_item.ProductID = 1
                mock_item.ProductName = "Test Product"
                mock_item.Quantity = 20  # More than available
                mock_item.TotalPrice = 10.0
                mock_cart.items = {1: mock_item}
                mock_get_cart.return_value = mock_cart
                
                # Mock the product service to check inventory
                with patch('app.routes.product.ProductService') as MockProductService:
                    mock_product_service = MagicMock()
                    MockProductService.return_value = mock_product_service
                    
                    # Create a proper product object with limited inventory
                    mock_product = MagicMock()
                    mock_product.ProductID = 1
                    mock_product.ProductName = "Test Product"
                    mock_product.UnitPrice = 10.0
                    mock_product.UnitsInStock = 10  # Less than requested quantity
                    mock_product_service.get_product_by_id.return_value = mock_product
                    
                    # Instead of checking flash messages, check that we're redirected back to the cart page
                    # or that the response contains an error message
                    response = client.post('/product/confirm_order', follow_redirects=True)
                    
                    # Check that the response indicates an error
                    assert response.status_code == 200
                    
                    # Either we should be redirected back to the cart page or the response should contain
                    # an error message about inventory
                    assert b'cart' in response.data.lower() or \
                           b'inventory' in response.data.lower() or \
                           b'stock' in response.data.lower() or \
                           b'insufficient' in response.data.lower() 