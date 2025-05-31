import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import pytest
from flask import g

from app import create_app
from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.supplier import SupplierService


@pytest.fixture
def app():
    # Create a temporary file to store the test database
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)  # Close the file descriptor as we'll use the path with shutil

    # Create the app first to get the main database path
    app = create_app()
    main_db = os.path.join(app.root_path, "northwind.db")

    # Copy the main database to our test location
    shutil.copy2(main_db, db_path)

    # Update the app config to use the test database
    app.config.update({"TESTING": True, "DATABASE": db_path})

    yield app

    # Clean up the temporary file
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def mock_cursor():
    cursor = Mock()
    return cursor


@pytest.fixture
def mock_db(app, mock_cursor):
    with app.app_context():
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        # Patch the database connection
        with patch("app.utils.database.get_db", return_value=mock_conn):
            g.db = mock_conn
            yield mock_cursor


@pytest.fixture
def mock_category_service(mock_db):
    service = CategoryService()
    # Ensure the cursor is set after initialization
    service.cursor = mock_db
    return service


@pytest.fixture
def mock_product_service(mock_db):
    service = ProductService()
    # Ensure the cursor is set after initialization
    service.cursor = mock_db
    return service


@pytest.fixture
def mock_supplier_service(mock_db):
    service = SupplierService()
    # Ensure the cursor is set after initialization
    service.cursor = mock_db
    return service


# DO NOT CHANGE THIS FIXTURE AS ITS VALUE IS USED IN MANY TESTS
@pytest.fixture
def mock_product():
    return Product(
        ProductID=1,
        ProductName="Test Product",
        CategoryID=1,
        SupplierID=1,
        QuantityPerUnit="10 boxes",
        UnitPrice=10.0,
        UnitsInStock=100,
        UnitsOnOrder=0,
        ReorderLevel=0,
        Discontinued="1",
    )


# DO NOT CHANGE THIS FIXTURE AS ITS VALUE IS USED IN MANY TESTS
@pytest.fixture
def mock_category():
    return Category(
        CategoryID=1,
        CategoryName="Test Category",
        Description="Test Category Description",
        Picture=b"Test Category Picture",
    )


# DO NOT CHANGE THIS FIXTURE AS ITS VALUE IS USED IN MANY TESTS
@pytest.fixture
def mock_supplier():
    return Supplier(
        SupplierID=1,
        CompanyName="Test Company",
        ContactName="Test Contact",
        ContactTitle="Test Contact Title",
        Address="Test Address",
        City="Test City",
        Region="Test Region",
        PostalCode="Test Postal Code",
        Country="Test Country",
        Phone="Test Phone",
        Fax="Test Fax",
        HomePage="Test Home Page",
    )


@pytest.fixture(autouse=True)
def cleanup_db(app):
    """Clean up the database after each test."""
    yield
    with app.app_context():
        if hasattr(g, "db"):
            g.db.execute("DELETE FROM Shopping_Cart")
            g.db.commit()


@pytest.fixture
def mock_user():
    """Create a mock user for testing authentication."""
    return Mock(
        id=1,
        username="testuser",
        customer_id=1,
        hashed_password="hashed_password"
    )

@pytest.fixture
def login_user(client, mock_user):
    """Simulate a logged-in user for tests that require authentication."""
    with patch('app.models.user.User.validate', return_value=mock_user):
        with patch('flask_login.utils._get_user', return_value=mock_user):
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password'
            })
            yield mock_user

@pytest.fixture
def mock_bcrypt():
    """Mock the bcrypt password hashing functionality."""
    with patch('app.models.user.bcrypt') as mock:
        mock.check_password_hash.return_value = True
        mock.generate_password_hash.return_value = "hashed_password"
        yield mock

@pytest.fixture
def mock_cart_item():
    """Create a mock cart item for testing cart functionality."""
    return Mock(
        ProductID=1,
        ProductName="Test Product",
        UnitPrice=10.0,
        Quantity=2,
        TotalPrice=20.0
    )

@pytest.fixture
def mock_cart_service():
    """Create a mock cart service for testing cart functionality."""
    service = Mock()
    service.get_cart_items.return_value = [
        Mock(
            ProductID=1,
            ProductName="Test Product",
            UnitPrice=10.0,
            Quantity=2,
            TotalPrice=20.0
        )
    ]
    service.get_cart_total.return_value = 20.0
    return service

@pytest.fixture
def mock_order_service():
    """Create a mock order service for testing order functionality."""
    service = Mock()
    service.create_order.return_value = 1  # Order ID
    return service
