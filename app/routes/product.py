from typing import Optional

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, session
from werkzeug.wrappers.response import Response
from flask_login import login_required, current_user

from app.models.cart import CartItem
from app.models.category import Category
from app.models.product import Product
from app.models.supplier import Supplier
from app.services.cart import CartService, get_cart, save_item_to_cart
from app.services.category import CategoryService
from app.services.product import ProductService
from app.services.supplier import SupplierService
from app.utils.logger import setup_logger
from app.utils.database import get_db

product_bp = Blueprint("product", __name__)


log = setup_logger(__name__)


@product_bp.route("/<int:product_id>")
def index(product_id: int):
    product: Optional[Product] = ProductService().get_product_by_id(product_id)
    if not product:
        return jsonify({"error": f"Product not found with id {product_id}"}), 404
    category: Optional[Category] = CategoryService().get_category_by_id(product.CategoryID)
    supplier: Optional[Supplier] = SupplierService().get_supplier_by_id(product.SupplierID)
    return render_template(
        "product/index.html", product=product, category=category, supplier=supplier
    )


@product_bp.route("/<int:product_id>", methods=["POST"])
def add_to_cart(product_id) -> Response:
    product: Optional[Product] = ProductService().get_product_by_id(product_id)
    if not product:
        flash(f"Product not found with id {product_id}", "error")
        return redirect(url_for("main.index"))

    quantity = int(request.form.get("quantity", 1))

    # get the current quantity of the product in the cart to avoid adding more than the stock
    cart_service = CartService()
    current_cart_quantity = cart_service.get_item_quantity(product_id)
    total_quantity = current_cart_quantity + quantity

    if total_quantity > product.UnitsInStock:
        flash(
            f"Cannot add {quantity} items. "
            f"Only {product.UnitsInStock - current_cart_quantity} remaining.",
            "error",
        )
        return redirect(url_for("product.index", product_id=product_id))

    cart_item = CartItem(
        ProductID=product_id,
        Quantity=quantity,
        ProductName=product.ProductName,
        TotalPrice=product.UnitPrice * quantity,
    )

    save_item_to_cart(cart_item=cart_item)
    log.info("Added the following item to cart: %s", cart_item)

    flash(f"Added {quantity} {product.ProductName} to cart!", "success")
    return redirect(url_for("product.index", product_id=product_id))


@product_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    if not cart or not cart.items:
        flash("Your cart is empty", "error")
        return redirect(url_for("main.index"))
    
    cart_total = sum(item.TotalPrice for item in cart.items.values())
    
    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("Please log in to complete your purchase", "error")
            return redirect(url_for("auth.login"))
        
        # Process checkout
        return redirect(url_for("product.choose_shipping"))
    
    return render_template("product/checkout.html", cart=cart, cart_total=cart_total)

@product_bp.route("/choose_shipping", methods=["GET", "POST"])
@login_required
def choose_shipping():
    if request.method == "POST":
        # Get form data from checkout page
        address = request.form.get("address")
        payment_method = request.form.get("payment_method")
        
        # Store in session
        session['address'] = address
        session['payment_method'] = payment_method
        
        return render_template("product/choose_shipping.html")
    
    # Check if we have the required data from the checkout page
    if 'address' not in session or 'payment_method' not in session:
        flash("Please complete the checkout form first", "error")
        return redirect(url_for("product.checkout"))
    
    return render_template("product/choose_shipping.html")

@product_bp.route("/confirm_order", methods=["GET", "POST"])
@login_required
def confirm_order():
    if request.method == "POST":
        # Get shipping method from form
        shipping_method = request.form.get("shipping_method")
        session['shipping_method'] = shipping_method
    
    # Check if we have all the required information
    address = session.get('address')
    payment_method = session.get('payment_method')
    shipping_method = session.get('shipping_method')
    
    if not address or not payment_method or not shipping_method:
        flash("Missing order information. Please try again.", "error")
        return redirect(url_for("product.checkout"))
    
    # Format shipping method for display
    formatted_shipping_method = shipping_method
    if shipping_method.lower() == "express":
        formatted_shipping_method = "Express (Overnight)"
    elif shipping_method.lower() == "standard":
        formatted_shipping_method = "Standard Shipping (5-7 business days)"
    elif shipping_method.lower() == "priority":
        formatted_shipping_method = "Priority (2-3 business days)"
    
    # Get cart for order total
    cart_service = CartService()
    cart = get_cart()
    cart_total = sum(item.TotalPrice for item in cart.items.values())
    
    # Generate a simple order ID (in a real app, this would come from the database)
    import random
    order_id = random.randint(10000, 99999)
    
    # Here you would handle the order confirmation logic, such as saving the order to the database
    
    # Update product inventory
    product_service = ProductService()
    inventory_updated = True
    
    # First check if all products have enough inventory
    for item in cart.items.values():
        product = product_service.get_product_by_id(item.ProductID)
        if not product or product.UnitsInStock < item.Quantity:
            flash(f"Sorry, {item.ProductName} is no longer available in the requested quantity.", "error")
            inventory_updated = False
            break
    
    # If all inventory checks pass, update the inventory
    if inventory_updated:
        for item in cart.items.values():
            if not product_service.update_product_inventory(item.ProductID, item.Quantity):
                # If any update fails, show an error
                flash("There was an issue processing your order. Please try again.", "error")
                return redirect(url_for("product.checkout"))
        
        # Clear cart and session data after successful order
        cart_service.clear_cart()
        
        # Clear session data
        session.pop('address', None)
        session.pop('payment_method', None)
        session.pop('shipping_method', None)
        
        # Render the order confirmation template with order details
        return render_template(
            "product/order_confirmation.html",
            order_id=order_id,
            order_total=cart_total,
            shipping_method=formatted_shipping_method
        )
    else:
        # If inventory check failed, redirect back to cart
        return redirect(url_for("product.view_cart"))

@product_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_service = CartService()
    cart_service.remove_from_cart(product_id)
    flash("Item removed from cart successfully!", "success")
    return redirect(url_for("product.checkout"))

@product_bp.route("/cart")
def view_cart():
    cart = get_cart()
    cart_total = sum(item.TotalPrice for item in cart.items.values()) if cart else 0
    return render_template("product/cart.html", cart=cart, cart_total=cart_total)
