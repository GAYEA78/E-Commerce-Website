import sqlite3

from app.utils.logger import setup_logger

log = setup_logger(__name__)


def init_db(app):
    """Initialize the database with required tables."""
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)

        # Enable foreign key support
        db.execute("PRAGMA foreign_keys = ON")

        # Create tables
        db.executescript(
            """
            -- Create Users table that references Customers
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL, 
                hashed_password TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(CustomerID)
            );

            -- Insert initial users from Customers if the table is empty
            INSERT OR IGNORE INTO Users (customer_id, username, hashed_password)
            SELECT 
                CustomerID,
                LOWER(ContactName), -- Use contact name as username (converted to lowercase)
                '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFJWQQFXZs.5HZi' -- Default hashed password: 'password'
            FROM Customers
            WHERE NOT EXISTS (SELECT 1 FROM Users WHERE customer_id = CustomerID);

            -- Create Shopping_Cart table
            CREATE TABLE IF NOT EXISTS Shopping_Cart (
                CartID INTEGER PRIMARY KEY AUTOINCREMENT,
                SessionID TEXT NOT NULL,
                ProductID INTEGER NOT NULL,
                Quantity INTEGER NOT NULL,
                AddedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
            );

            -- Add index for faster lookups
            CREATE INDEX IF NOT EXISTS idx_shopping_cart_session 
            ON Shopping_Cart(SessionID);
            
            CREATE INDEX IF NOT EXISTS idx_shopping_cart_added_at 
            ON Shopping_Cart(AddedAt);
            
            -- Add WEB employee if not exists
            INSERT OR IGNORE INTO Employees (
                FirstName, LastName, Title
            ) VALUES (
                'WEB', 'WEB', 'Online Sales System'
            );
        """
        )

        db.commit()

        # Get the WEB employee ID for reference
        cursor = db.cursor()
        cursor.execute(
            "SELECT EmployeeID FROM Employees WHERE FirstName = 'WEB' AND LastName = 'WEB'"
        )
        web_employee_id = cursor.fetchone()[0]

        log.info("Database initialized. WEB employee ID: %s", web_employee_id)

        return web_employee_id
