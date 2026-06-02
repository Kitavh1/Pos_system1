from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

# FRONTEND PAGE

@app.route("/")
def home ():
    return render_template("index.html") 


# PRODUCTS DATABASE
products = {
    1: {"name": "Coffee", "price": 3.50, "stock": 50},
    2: {"name": "Tea", "price": 2.75, "stock": 40},
    3: {"name": "Sandwich", "price": 5.00, "stock": 20},
}

# CART
cart = {}


# GET PRODUCTS
@app.route("/products", methods=["GET"])
def list_products():
    return jsonify(products)


# VIEW CART
@app.route("/cart", methods=["GET"])
def get_cart():

    total = sum(
        item["quantity"] * item["price"]
        for item in cart.values()
    )

    return jsonify({
        "items": cart,
        "total": round(total, 2)
    })


# ADD TO CART
@app.route("/cart/add", methods=["POST"])
def add_to_cart():

    data = request.get_json()

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if product_id not in products:
        return jsonify({
            "error": "Invalid product"
        }), 400

    product = products[product_id]

    if quantity > product["stock"]:
        return jsonify({
            "error": "Out of stock"
        }), 400

    cart_item = cart.get(product_id, {
        "name": product["name"],
        "price": product["price"],
        "quantity": 0
    })

    cart_item["quantity"] += quantity

    cart[product_id] = cart_item

    product["stock"] -= quantity

    return jsonify({
        "message": "Added to cart"
    })


# CHECKOUT
@app.route("/checkout", methods=["POST"])
def checkout():

    total = sum(
        item["quantity"] * item["price"]
        for item in cart.values()
    )

    receipt = {
        "timestamp": datetime.utcnow().isoformat(),
        "items": cart,
        "total": total
    }

    cart.clear()

    return jsonify(receipt)


# START SERVER
if __name__ == "__main__":
    app.run(debug=True)

else:
    print("POS System backend is ready to serve requests.")
    