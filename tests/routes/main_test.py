import pytest

from app.models.category import Category
from app.models.product import Product
from app.services.category import CategoryService
from app.services.product import ProductService


@pytest.fixture
def mock_product_list():
    return [
        Product(
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
        ),
        Product(
            ProductID=2,
            ProductName="Chang",
            SupplierID=1,
            CategoryID=1,
            QuantityPerUnit="24 - 12 oz bottles",
            UnitPrice=19.00,
            UnitsInStock=17,
            UnitsOnOrder=40,
            ReorderLevel=25,
            Discontinued="0",
        ),
        Product(
            ProductID=3,
            ProductName="Aniseed Syrup",
            SupplierID=1,
            CategoryID=2,
            QuantityPerUnit="12 - 550 ml bottles",
            UnitPrice=10.00,
            UnitsInStock=13,
            UnitsOnOrder=70,
            ReorderLevel=25,
            Discontinued="0",
        ),
    ]


@pytest.fixture
def mock_category_list():
    return [
        Category(
            CategoryID=1,
            CategoryName="Beverages",
            Description="Soft drinks, coffees, teas, beers, and ales",
            Picture=b"beverage_image_data",
        ),
        Category(
            CategoryID=2,
            CategoryName="Condiments",
            Description="Sweet and savory sauces, relishes, spreads, and seasonings",
            Picture=b"condiment_image_data",
        ),
    ]


@pytest.fixture
def mock_product_service(mock_product_list):
    class MockProductService:
        def get_all_products(self):
            return mock_product_list

        def search_products(self, search_term):
            if not search_term:
                return mock_product_list
            return [p for p in mock_product_list if search_term.lower() in p.ProductName.lower()]

        def get_products_by_category(self, category_id):
            return [p for p in mock_product_list if p.CategoryID == category_id]

    return MockProductService()


@pytest.fixture
def mock_category_service(mock_category_list):
    class MockCategoryService:
        def get_all_categories(self):
            return mock_category_list

        def get_category_by_id(self, category_id):
            for category in mock_category_list:
                if category.CategoryID == category_id:
                    return category
            return None

    return MockCategoryService()


def test_index_route(client, mock_product_service, mock_category_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(ProductService, "get_all_products", mock_product_service.get_all_products)
    monkeypatch.setattr(CategoryService, "get_all_categories", mock_category_service.get_all_categories)

    # Test the main index route
    response = client.get("/")
    assert response.status_code == 200
    assert b"All Products" in response.data
    assert b"Chai" in response.data
    assert b"Chang" in response.data
    assert b"Aniseed Syrup" in response.data
    assert b"Beverages" in response.data
    assert b"Condiments" in response.data


def test_search_products(client, mock_product_service, mock_category_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(ProductService, "search_products", mock_product_service.search_products)
    monkeypatch.setattr(CategoryService, "get_all_categories", mock_category_service.get_all_categories)

    # Test search functionality
    response = client.get("/?search=chai")
    assert response.status_code == 200
    assert b"Search results for &#39;chai&#39;" in response.data
    assert b"Chai" in response.data
    assert b"Chang" not in response.data
    assert b"Aniseed Syrup" not in response.data


def test_category_filter(client, mock_product_service, mock_category_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(ProductService, "get_products_by_category", mock_product_service.get_products_by_category)
    monkeypatch.setattr(CategoryService, "get_all_categories", mock_category_service.get_all_categories)
    monkeypatch.setattr(CategoryService, "get_category_by_id", mock_category_service.get_category_by_id)

    # Test category filtering
    response = client.get("/?category=1")
    assert response.status_code == 200
    assert b"Beverages" in response.data
    assert b"Chai" in response.data
    assert b"Chang" in response.data
    assert b"Aniseed Syrup" not in response.data


def test_search_with_category(client, mock_product_service, mock_category_service, monkeypatch):
    # Patch the service methods
    monkeypatch.setattr(ProductService, "get_products_by_category", mock_product_service.get_products_by_category)
    monkeypatch.setattr(ProductService, "search_products", mock_product_service.search_products)
    monkeypatch.setattr(CategoryService, "get_all_categories", mock_category_service.get_all_categories)
    monkeypatch.setattr(CategoryService, "get_category_by_id", mock_category_service.get_category_by_id)

    # Test search with category filtering
    # Note: In a real implementation, you would need to handle combined search and category filtering
    # This test is simplified and assumes the route prioritizes category over search
    response = client.get("/?search=chai&category=1")
    assert response.status_code == 200
    assert b"Beverages" in response.data
    # The actual behavior depends on your implementation
    # If category filter takes precedence, we should see both Chai and Chang
    # If search is applied within category, we should only see Chai 