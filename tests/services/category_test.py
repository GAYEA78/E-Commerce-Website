from app.models.category import Category

# Need the app_context because the tests work with database operations


def test_get_category_by_id_with_valid_id(app, mock_db, mock_category_service):
    with app.app_context():
        # Arrange
        category_id = 2
        expected_category = {
            "CategoryID": 2,
            "CategoryName": "Electronics",
            "Description": "Category for electronic devices",
            "Picture": b"asdoiasmdoiasmdoiasmd",
        }

        mock_db.fetchone.return_value = (
            expected_category["CategoryID"],
            expected_category["CategoryName"],
            expected_category["Description"],
            expected_category["Picture"],
        )

        # Act
        result = mock_category_service.get_category_by_id(category_id)

        # Assert
        assert isinstance(result, Category)
        assert result.CategoryID == expected_category["CategoryID"]
        assert result.CategoryName == expected_category["CategoryName"]
        assert result.Description == expected_category["Description"]
        assert result.Picture == expected_category["Picture"]

        # Verify mock interactions
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM Categories WHERE CategoryID = ?", (category_id,)
        )
        mock_db.fetchone.assert_called_once()


def test_get_category_by_id_with_invalid_id(app, mock_db, mock_category_service):
    with app.app_context():
        # Arrange
        category_id = 0
        mock_db.fetchone.return_value = None

        # Act
        result = mock_category_service.get_category_by_id(category_id)

        # Assert
        assert result is None

        # Verify mock interactions
        mock_db.execute.assert_called_once_with(
            "SELECT * FROM Categories WHERE CategoryID = ?", (category_id,)
        )
        mock_db.fetchone.assert_called_once()


def test_get_category_by_id_with_none(app, mock_db, mock_category_service):
    with app.app_context():
        # Arrange
        category_id = None

        # Act
        result = mock_category_service.get_category_by_id(category_id)

        # Assert
        assert result is None

        # Verify no database calls were made
        mock_db.execute.assert_not_called()
        mock_db.fetchone.assert_not_called()


def test_get_all_categories(app, mock_db, mock_category_service):
    with app.app_context():
        # Arrange
        expected_categories = [
            {
                "CategoryID": 1,
                "CategoryName": "Beverages",
                "Description": "Soft drinks, coffees, teas, beers, and ales",
                "Picture": b"beverage_image_data",
            },
            {
                "CategoryID": 2,
                "CategoryName": "Condiments",
                "Description": "Sweet and savory sauces, relishes, spreads, and seasonings",
                "Picture": b"condiment_image_data",
            },
        ]
        mock_rows = [tuple(category.values()) for category in expected_categories]
        mock_db.fetchall.return_value = mock_rows

        # Act
        result = mock_category_service.get_all_categories()

        # Assert
        assert len(result) == len(expected_categories)
        for i, category in enumerate(result):
            assert isinstance(category, Category)
            assert category.CategoryID == expected_categories[i]["CategoryID"]
            assert category.CategoryName == expected_categories[i]["CategoryName"]
            assert category.Description == expected_categories[i]["Description"]
            assert category.Picture == expected_categories[i]["Picture"]

        # Verify mock interactions
        mock_db.execute.assert_called_once_with("SELECT * FROM Categories ORDER BY CategoryName")
        mock_db.fetchall.assert_called_once()
