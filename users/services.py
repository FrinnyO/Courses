import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    product = stripe.Product.create(name=name)
    return product.get("name")


def create_stripe_price(amount, prod_name):
    price = stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product_data={"name": prod_name},
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def check_session_status(session_id):
    return stripe.checkout.Session.retrieve(
        session_id,
    )
