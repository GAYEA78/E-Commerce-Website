from app.models.product import Product

# Need the app_context because the tests work with database operations


def test_get_all_products(app, mock_db, mock_product_service):
    with app.app_context():
        # Arrange
        expected_products = [
            {
                "ProductID": 1,
                "ProductName": "Product 1",
                "SupplierID": 1,
                "CategoryID": 1,
                "QuantityPerUnit": "24 - 12 oz bottles",
                "UnitPrice": 36.00,
                "UnitsInStock": 10,
                "UnitsOnOrder": 0,
                "ReorderLevel": 5,
                "Discontinued": "1",
            },
            {
                "ProductID": 2,
                "ProductName": "Product 2",
                "SupplierID": 2,
                "CategoryID": 2,
                "QuantityPerUnit": "48 - 6 oz jars",
                "UnitPrice": 14.00,
                "UnitsInStock": 20,
                "UnitsOnOrder": 0,
                "ReorderLevel": 0,
                "Discontinued": "0",
            },
        ]
        mock_rows = [tuple(product.values()) for product in expected_products]
        mock_db.fetchall.return_value = mock_rows

        # Act
        result = mock_product_service.get_all_products()

        # Assert
        assert len(result) == len(expected_products)
        for i, product in enumerate(result):
            assert isinstance(product, Product)
            assert product.ProductID == expected_products[i]["ProductID"]
            assert product.ProductName == expected_products[i]["ProductName"]
            assert product.SupplierID == expected_products[i]["SupplierID"]
            assert product.CategoryID == expected_products[i]["CategoryID"]
            assert product.QuantityPerUnit == expected_products[i]["QuantityPerUnit"]
            assert product.UnitPrice == expected_products[i]["UnitPrice"]
            assert product.UnitsInStock == expected_products[i]["UnitsInStock"]
            assert product.UnitsOnOrder == expected_products[i]["UnitsOnOrder"]
            assert product.ReorderLevel == expected_products[i]["ReorderLevel"]
            assert product.Discontinued == expected_products[i]["Discontinued"]
        mock_db.fetchall.assert_called_once()


def test_get_product_by_id_with_valid_id(app, mock_db, mock_product_service):
    with app.app_context():
        # Arrange
        product_id = 1
        expected_product = {
            "ProductID": 1,
            "ProductName": "Product 1",
            "SupplierID": 1,
            "CategoryID": 1,
            "QuantityPerUnit": "24 - 12 oz bottles",
            "UnitPrice": 36.00,
            "UnitsInStock": 10,
            "UnitsOnOrder": 0,
            "ReorderLevel": 5,
            "Discontinued": "1",
        }

        mock_db.fetchone.return_value = (
            expected_product["ProductID"],
            expected_product["ProductName"],
            expected_product["SupplierID"],
            expected_product["CategoryID"],
            expected_product["QuantityPerUnit"],
            expected_product["UnitPrice"],
            expected_product["UnitsInStock"],
            expected_product["UnitsOnOrder"],
            expected_product["ReorderLevel"],
            expected_product["Discontinued"],
        )

        # Act
        result = mock_product_service.get_product_by_id(product_id)

        # Assert
        assert isinstance(result, Product)
        assert result.ProductID == expected_product["ProductID"]
        assert result.ProductName == expected_product["ProductName"]
        assert result.SupplierID == expected_product["SupplierID"]
        assert result.CategoryID == expected_product["CategoryID"]
        assert result.QuantityPerUnit == expected_product["QuantityPerUnit"]
        assert result.UnitPrice == expected_product["UnitPrice"]
        assert result.UnitsInStock == expected_product["UnitsInStock"]
        assert result.UnitsOnOrder == expected_product["UnitsOnOrder"]
        assert result.ReorderLevel == expected_product["ReorderLevel"]
        assert result.Discontinued == expected_product["Discontinued"]

        # Verify mock interactions
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM Products WHERE ProductID = ?", (product_id,)
        )
        mock_db.fetchone.assert_called_once()


def test_get_product_by_id_with_invalid_id(app, mock_db, mock_product_service):
    with app.app_context():
        # Arrange
        product_id = 0
        mock_db.fetchone.return_value = None

        # Act
        result = mock_product_service.get_product_by_id(product_id)

        # Assert
        assert result is None

        # Verify mock interactions
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM Products WHERE ProductID = ?", (product_id,)
        )
        mock_db.fetchone.assert_called_once()


def test_get_product_by_id_with_none(app, mock_db, mock_product_service):
    with app.app_context():
        # Arrange
        product_id = None
        mock_db.fetchone.return_value = None

        # Act
        result = mock_product_service.get_product_by_id(product_id)

        # Assert
        assert result is None

        # Verify no database calls were made
        mock_db.execute.assert_not_called()
        mock_db.fetchone.assert_not_called()


def test_search_products_with_valid_term(app, mock_db, mock_product_service):
    with app.app_context():
        # Arrange
        search_term = "chai"
        expected_products = [
            {
                "ProductID": 1,
                "ProductName": "Chai",
                "SupplierID": 1,
                "CategoryID": 1,
                "QuantityPerUnit": "10 boxes x 20 bags",
                "UnitPrice": 18.00,
                "UnitsInStock": 39,
                "UnitsOnOrder": 0,
                "ReorderLevel": 10,
                "Discontinued": "0",
            },
        ]
        mock_rows = [tuple(product.values()) for product in expected_products]
        mock_db.fetchall.return_value = mock_rows

        # Act
        result = mock_product_service.search_products(search_term)

        # Assert
        assert len(result) == len(expected_products)
        for i, product in enumerate(result):
            assert isinstance(product, Product)
            assert product.ProductID == expected_products[i]["ProductID"]
            assert product.ProductName == expected_products[i]["ProductName"]

        # Verify mock interactions
        mock_db.execute.assert_called_once()
        search_pattern = f"%{search_term}%"
        assert search_pattern in str(mock_db.execute.call_args)
        mock_db.fetchall.assert_called_once()


def test_search_products_with_empty_term(app, mock_db, mock_product_service):
    with app.app_context():
        # Arrange
        search_term = ""
        expected_products = [
            {
                "ProductID": 1,
                "ProductName": "Product 1",
                "SupplierID": 1,
                "CategoryID": 1,
                "QuantityPerUnit": "24 - 12 oz bottles",
                "UnitPrice": 36.00,
                "UnitsInStock": 10,
                "UnitsOnOrder": 0,
                "ReorderLevel": 5,
                "Discontinued": "1",
            },
            {
                "ProductID": 2,
                "ProductName": "Product 2",
                "SupplierID": 2,
                "CategoryID": 2,
                "QuantityPerUnit": "48 - 6 oz jars",
                "UnitPrice": 14.00,
                "UnitsInStock": 20,
                "UnitsOnOrder": 0,
                "ReorderLevel": 0,
                "Discontinued": "0",
            },
        ]
        mock_rows = [tuple(product.values()) for product in expected_products]
        mock_db.fetchall.return_value = mock_rows

        # Act
        result = mock_product_service.search_products(search_term)

        # Assert
        assert len(result) == len(expected_products)
        
        # Should call get_all_products instead of searching
        mock_db.execute.assert_called_once()
        assert "SELECT * FROM Products" in str(mock_db.execute.call_args)
        mock_db.fetchall.assert_called_once()


def test_get_products_by_category(app, mock_db, mock_product_service):
    with app.app_context():
        # Arrange
        category_id = 1
        expected_products = [
            {
                "ProductID": 1,
                "ProductName": "Chai",
                "SupplierID": 1,
                "CategoryID": 1,
                "QuantityPerUnit": "10 boxes x 20 bags",
                "UnitPrice": 18.00,
                "UnitsInStock": 39,
                "UnitsOnOrder": 0,
                "ReorderLevel": 10,
                "Discontinued": "0",
            },
            {
                "ProductID": 2,
                "ProductName": "Chang",
                "SupplierID": 1,
                "CategoryID": 1,
                "QuantityPerUnit": "24 - 12 oz bottles",
                "UnitPrice": 19.00,
                "UnitsInStock": 17,
                "UnitsOnOrder": 40,
                "ReorderLevel": 25,
                "Discontinued": "0",
            },
        ]
        mock_rows = [tuple(product.values()) for product in expected_products]
        mock_db.fetchall.return_value = mock_rows

        # Act
        result = mock_product_service.get_products_by_category(category_id)

        # Assert
        assert len(result) == len(expected_products)
        for i, product in enumerate(result):
            assert isinstance(product, Product)
            assert product.ProductID == expected_products[i]["ProductID"]
            assert product.ProductName == expected_products[i]["ProductName"]
            assert product.CategoryID == expected_products[i]["CategoryID"]

        # Verify mock interactions
        mock_db.execute.assert_called_once()
        assert str(category_id) in str(mock_db.execute.call_args)
        mock_db.fetchall.assert_called_once()
