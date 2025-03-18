from flask import Blueprint, render_template, request

from app.models.product import Product
from app.services.category import CategoryService
from app.services.product import ProductService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    """Main landing page with product listing, search, and category browsing."""
    # Get search parameters
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', None)
    
    # Initialize services
    product_service = ProductService()
    category_service = CategoryService()
    
    # Get all categories for the sidebar
    categories = category_service.get_all_categories()
    
    # Get products based on filters
    products: list[Product] = []
    
    if category_id and category_id.isdigit():
        # If category filter is applied
        products = product_service.get_products_by_category(int(category_id))
        selected_category = category_service.get_category_by_id(int(category_id))
        category_name = selected_category.CategoryName if selected_category else "Unknown Category"
    elif search_query:
        # If search is applied
        products = product_service.search_products(search_query)
        category_name = f"Search results for '{search_query}'"
    else:
        # Default: show all products
        products = product_service.get_all_products()
        category_name = "All Products"
    
    return render_template(
        "main/index.html", 
        products=products, 
        categories=categories,
        search_query=search_query,
        category_id=category_id,
        category_name=category_name
    )
