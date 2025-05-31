import pytest

from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.supplier import SupplierService


@pytest.fixture
def mock_product_service(mock_product):
    class MockProductService:
        def get_product_by_id(self, product_id):
            if product_id == 1:
                return mock_product
            return None

    return MockProductService()


@pytest.fixture
def mock_category_service(mock_category):
    class MockCategoryService:
        def get_category_by_id(self, category_id):
            if category_id == 1:
                return mock_category
            return None

    return MockCategoryService()


@pytest.fixture
def mock_supplier_service(mock_supplier):
    class MockSupplierService:
        def get_supplier_by_id(self, supplier_id):
            if supplier_id == 1:
                return mock_supplier
            return None

    return MockSupplierService()


def test_index_route(
    client, mock_product_service, mock_category_service, mock_supplier_service, monkeypatch
):
    monkeypatch.setattr(ProductService, "get_product_by_id", mock_product_service.get_product_by_id)
    monkeypatch.setattr(
        CategoryService, "get_category_by_id", mock_category_service.get_category_by_id
    )
    monkeypatch.setattr(
        SupplierService, "get_supplier_by_id", mock_supplier_service.get_supplier_by_id
    )

    response = client.get("/product/1")
    assert response.status_code == 200
    assert b"Test Product" in response.data


def test_add_to_cart_route(client, mock_product_service, monkeypatch):
    monkeypatch.setattr(ProductService, "get_product_by_id", mock_product_service.get_product_by_id)

    # Test successful addition
    response = client.post("/product/1", data={"quantity": 2}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Added 2 Test Product to cart!" in response.data

    # Test non-existent product
    response = client.post("/product/999", data={"quantity": 1}, follow_redirects=True)
    assert response.status_code == 200  # Because it redirects to main.index
    assert b"Product not found with id 999" in response.data

    # Test exceeding stock quantity
    response = client.post("/product/1", data={"quantity": 101}, follow_redirects=True)
    assert response.status_code == 200  # Because it redirects to product.index
    assert b"Cannot add 101 items" in response.data
