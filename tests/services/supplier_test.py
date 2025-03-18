from app.models.supplier import Supplier

# Need the app_context because the tests work with database operations


def test_get_supplier_by_id_with_valid_id(app, mock_db, mock_supplier_service):
    with app.app_context():
        # Arrange
        supplier_id = 2
        expected_category = {
            "SupplierID": 2,
            "CompanyName": "Acme, Inc.",
            "ContactName": "John Doe",
            "ContactTitle": "Sales Representative",
            "Address": "123 Main St.",
            "City": "Anytown",
            "Region": "Anystate",
            "PostalCode": "12345",
            "Country": "USA",
            "Phone": "(123) 456-7890",
            "Fax": "(123) 456-7890",
            "HomePage": "http://www.acme.com/johndoe",
        }

        mock_db.fetchone.return_value = (
            expected_category["SupplierID"],
            expected_category["CompanyName"],
            expected_category["ContactName"],
            expected_category["ContactTitle"],
            expected_category["Address"],
            expected_category["City"],
            expected_category["Region"],
            expected_category["PostalCode"],
            expected_category["Country"],
            expected_category["Phone"],
            expected_category["Fax"],
            expected_category["HomePage"],
        )

        # Act
        result = mock_supplier_service.get_supplier_by_id(supplier_id)

        # Assert
        assert isinstance(result, Supplier)
        assert result.SupplierID == expected_category["SupplierID"]
        assert result.CompanyName == expected_category["CompanyName"]
        assert result.ContactName == expected_category["ContactName"]
        assert result.ContactTitle == expected_category["ContactTitle"]
        assert result.Address == expected_category["Address"]
        assert result.City == expected_category["City"]
        assert result.Region == expected_category["Region"]
        assert result.PostalCode == expected_category["PostalCode"]
        assert result.Country == expected_category["Country"]
        assert result.Phone == expected_category["Phone"]
        assert result.Fax == expected_category["Fax"]
        assert result.HomePage == expected_category["HomePage"]

        # Verify mock interactions
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM Suppliers WHERE SupplierID = ?", (supplier_id,)
        )
        mock_db.fetchone.assert_called_once()


def test_get_supplier_by_id_with_invalid_id(app, mock_db, mock_supplier_service):
    with app.app_context():
        # Arrange
        supplier_id = 0
        mock_db.fetchone.return_value = None

        # Act
        result = mock_supplier_service.get_supplier_by_id(supplier_id)

        # Assert
        assert result is None

        # Verify mock interactions
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM Suppliers WHERE SupplierID = ?", (supplier_id,)
        )
        mock_db.fetchone.assert_called_once()


def test_get_supplier_by_id_with_none(app, mock_db, mock_supplier_service):
    with app.app_context():
        # Arrange
        supplier_id = None

        # Act
        result = mock_supplier_service.get_supplier_by_id(supplier_id)

        # Assert
        assert result is None

        # Verify no database calls were made
        mock_db.execute.assert_not_called()
        mock_db.fetchone.assert_not_called()
