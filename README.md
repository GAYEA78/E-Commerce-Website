# E-Commerce-Website
You can run the app directly from its deployed website: https://e-commerce.aronagaye.me/
## Overview of Project


### Testing Approach


1. **Unit Tests**: For individual components and services
   - Product service tests verify product retrieval, filtering, and inventory management
   - Cart service tests ensure proper cart functionality and session management
   - Authentication tests verify user registration, login processes, and session handling
   - Category and supplier tests validate data retrieval and filtering

2. **Integration Tests**: For end-to-end functionality
   - Complete user flow from browsing to checkout
   - Cart-to-order conversion during checkout
   - Session persistence across multiple requests

3. **Test Coverage**: Tests cover approximately 85% of the codebase, focusing on:
   - Critical user flows (authentication, product browsing, cart management, checkout)
   - Database operations (CRUD operations, inventory updates)
   - Error handling (form validation, inventory checks)

4. **Testing Tools**:
   - Pytest framework for test organization and execution
   - Mock objects for isolating components during testing
   - Fixtures for setting up test environments

### Notable Implementation Details

1. **Architecture**:
   - Clear segregation of concerns among `services`, `models` and `routes`
   - `routes` are purely responsible for rendering the HTML templates, offloading all business logic to the corresponding service in `services`
   - All data structures are centrally managed in the `models` module

2. **Enhanced Authentication System**:
   - Secure password hashing using Flask's built-in security features
   - Session management with proper timeout handling
   - Protection against common security vulnerabilities

3. **Inventory Management**:
   - Real-time inventory updates upon order placement
   - Inventory validation during checkout to prevent ordering out-of-stock items
   - Clear error messaging for insufficient inventory

4. **User Experience Enhancements**:
   - Responsive design for mobile and desktop
   - Intuitive shopping cart management
   - Clear order confirmation process with shipping details

5. **Database Modifications**:
   - Added Authentication table with CustomerID, Password, and SessionID columns
   - Created WEB employee for online orders
   - Implemented Shopping_Cart table with timestamp for cleanup
   - Enhanced Customers table with regional classification
   - Added BLOB image data to Categories table

## Quick Start (Follow from CMD command prompt terminal)
If you want to run it direrctly online: https://e-commerce.aronagaye.me/ otherwise follow instructions below

```bash
Clone the repo
git clone git@github.com:GAYEA78/E-Commerce-Website.git
cd E-Commerce-Website
```

### Install Poetry

Please follow the official [installation guide](https://python-poetry.org/docs/#installation) to install Poetry.

### Install dependencies

It is recommended to use Python virtual environment, so you don't pollute your system Python environment.

```bash
# Install dependencies
poetry install
```

### Mac/Linux

```bash
# Activate Python virtual environment
eval "$(poetry env activate)"
```

### Windows

```bash
# Activate Python Virtual Environment
.venv\Scripts\Activate.bat
```

### Set up environment variables

```bash
# Create .env file (by copying from .env.example)
on Mac: cp .env.example .env
on Windows: copy .env.example .env

```
```Install the flask_bcrypt module
pip install flask-bcrypt
```
```

## Commands

```bash
# Quick Start at root directory
flask run
Customer ID to register: ALFKI

# Run tests
pytest

# Run tests with coverage report
pytest --cov=app

# To verify that the app is running, go to the /status endpoint
```

## Development

### Add dependencies

If you want to add a new dependency, please use `poetry add` command.

For example, to add `python-dotenv` dependency, run:

```bash
poetry add python-dotenv
```

## Style Enforcement

```bash
make lint # Run in the root of the directory
```

## Folder Structure

```bash
├── app/
│   ├── models/ # Data models used across the application
│   ├── routes/ # Routes handle the HTTP requests and render the appropriate templates (no business logic)
│   ├── services/ # Services handle the business logic of the application
│   ├── static/ # Static files like CSS
│   ├── templates/ # Jinja templates
│   ├── utils/ # Utility functions that are used across the entire application
│   ├── northwind.db # Built database file
│   └── run.py # Main executuable file
└── tests/ # Tests for each file are labelled with the file name
    ├── routes/ # Tests for route handlers
    ├── services/ # Tests for service layer
    ├── integration_test.py # End-to-end tests
    └── conftest.py # Test fixtures and configuration
```

## Database Modifications

### Authentication Table
- Added a new table `Authentication` to store user credentials
- Columns include `CustomerID` (foreign key to Customers), `Password` (hashed), and `SessionID`
- Implemented with proper indexing for performance optimization

### Shopping Cart Table
- Created `Shopping_Cart` table to track items in user carts
- Includes timestamp for cleanup of abandoned carts
- Links to both authenticated and unauthenticated users via session IDs

### WEB Employee
- Added a special employee record with ID "WEB" to represent the online ordering system
- Used for all orders placed through the web interface

### Regional Classification for Customers  
- The `Customers` table was updated to assign a `Region` value based on the customer's `Country`  
- Example assignments include:  
  - UK & Ireland → *British Isles*  
  - USA & Canada → *North America*  
  - Mexico → *Central America*  
  - Brazil, Argentina, Venezuela → *South America*  
  - Poland → *Eastern Europe*  
  - Sweden & Denmark → *Northern Europe*  
  - Spain, Italy, Portugal → *Southern Europe*  

### Enhancements to Existing Tables  
- The `Categories` table now includes images stored as `BLOB` data for product classification
- Additional structural or data integrity improvements across other tables
