import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    """Function to create a product in stripe"""
    stripe_product = stripe.Product.create(name=product_name)
    return stripe_product["id"]


def create_stripe_price(amount, product_id):
    """Создание цены в страйпе"""
    return stripe.Price.create(
        currency="usd", unit_amount=int(amount * 100), product=product_id
    )


def create_stripe_sessions(price):
    """Создание центы на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
