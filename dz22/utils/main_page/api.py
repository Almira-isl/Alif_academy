import requests
from configs import base_url


def get_active_items():
    response = requests.get(url=f"{base_url}/web/client/events/active")

    return response


def get_item(item_slug: str):
    response = requests.get(url=f"{base_url}/web/client/moderated-offers/{item_slug}")

    return response


def search_items(item_name: str):
    body = {
        "query": item_name
    }

    response = requests.post(url=f"{base_url}/web/client/search/full-text", json=body)

    return response

def get_cart(cookie=None):
    if cookie is None:
        response = requests.get(f"{base_url}/web/client/cart/view-cart/duplicate")
    else:
        headers = {
            'Cookie': f"cart={cookie};"
        }

        response = requests.get(
            url=f"{base_url}/web/client/cart/view-cart/duplicate",
            headers=headers
        )

    return response


def add_to_cart(cookie: str, offer_id: str, condition_id: int, quantity=1):
    headers = {
        'Cookie': f"cart={cookie};"
    }

    body = {
        "moderated_offer_id": offer_id,
        "condition_id": condition_id,
        "quantity": quantity
    }

    response = requests.post(
        url=f"{base_url}/web/client/cart/moderated-items",
        json=body,
        headers=headers
    )

    return response



# get_item = f"{base_url}/web/client/moderated-offers"

# moderated_offer_url = f"{base_url}/web/client/moderated-offers"




def get_offers_v2(user_id: str, limit:int=15):
    url = f"{base_url}/web/client/recommend/offers/v2"
    offers_body = {
        "user_id": user_id,
        "from_app": "WebAndMobile",
        "from_layer": "offer_page",
        "limit": limit
    }
    response = requests.post(url, headers={"Accept": "application/json"}, json=offers_body)
   
    return response

def get_offer_reviews(offer_id: int):
    url = f"{base_url}/web/client/moderated-offers/{offer_id}/reviews"
    response = requests.get(url, headers={"Accept": "application/json"})
    return response


def get_delivery_time(offer_id: int):
    url = f"{base_url}/web/client/catalog/moderated-offers/{offer_id}/delivery-time-estimation/duplicate"
    response = requests.get(url, headers={"Accept": "application/json"})
    return response