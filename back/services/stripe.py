import os
from urllib.parse import quote

import stripe
import requests

def create_checkout(reference, name, unit_price, quantity, confirmation_secret):
    """
        Create Stripe checkout
        Documentation: https://docs.stripe.com/checkout/quickstart?client=react&lang=python
    """
    
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    origin_host = os.getenv('APP_ORIGIN_HOST')
    return stripe.checkout.Session.create(
        mode='payment',
        success_url=f"{origin_host}/booking/{reference}?checkout_confirmation_secret={confirmation_secret}",
        cancel_url=origin_host,
        line_items=[
            {
                'quantity': quantity,
                'price_data': {
                    'currency': 'EUR',
                    'unit_amount': round(unit_price * 100),
                    'product_data': {
                        'name': name,
                    },
                },
            },
        ],
    )

def get_checkout_lines(checkout_session_id):
    # FIX D3 : l'identifiant est encode avant d'etre place dans le chemin.
    # Il ne peut plus contenir de '../' ni faire sortir de /v1/checkout/sessions/.
    safe_session_id = quote(checkout_session_id, safe="")
    url = f"https://api.stripe.com/v1/checkout/sessions/{safe_session_id}/line_items"

    session = requests.Session()
    session.auth = (os.getenv('STRIPE_API_KEY'), "")
    return session.get(url).json()["data"]
