
import pytest
import requests
import json
from utils.main_page.api import get_active_items, get_item, search_items, get_cart, add_to_cart, get_offers_v2, get_offer_reviews, get_delivery_time
import allure
from utils.functions import attach_reqres


@allure.parent_suite("Главная страница")
@allure.suite("Проверка активных событий")
@allure.title("Проверка корректности данных события")
def test_active_events():
    with allure.step('Отправка запроса на получение активных событий'):
        resp = get_active_items()
        attach_reqres(resp)
        assert resp.status_code == 200

    data = resp.json()
    with allure.step('Проверка, что данные приходят'):
        assert data

    offer = data[0]["offers"][0]

    with allure.step('Проверка цены'):
        assert offer["price"] > 0
        if "old_price" in offer and offer["old_price"] is not None:
            assert offer["old_price"] >= offer["price"]

        if offer.get("discount", 0) < 0:
            assert offer["price"] < offer["old_price"]



@allure.parent_suite("Главная страница")
@allure.suite("Проверка карточки товара")
@allure.title("Проверка moderated_offer по slug")
def test_moderated_offer():
    with allure.step('Отправка запроса на получение активных товаров'):
        resp=get_active_items()
        attach_reqres(resp)
        assert resp.status_code == 200
        slug = resp.json()[0]["offers"][0]["slug"]

    resp=get_item(slug)
    assert resp.status_code == 200
    data = resp.json()

    with allure.step('Проверка moderated_offer'):
        assert "moderated_offer" in data
        offer = data["moderated_offer"]

    with allure.step('Проверка названия'):
        assert "name" in offer and offer["name"]

    with allure.step('Проверка цены'):
        assert offer["price"] > 0

    with allure.step('Проверка скидки'):
        assert "discount" in offer
    
    with allure.step('Проверка картинки'):
        assert isinstance(offer["images"], list)
        assert len(offer["images"]) > 0



@allure.parent_suite("Главная страница")
@allure.suite("Проверка расчетов доставки")
@allure.title("Проверка delivery_time_estimation")
def test_delivery_time():
    with allure.step('Отправка запроса'):
        resp = get_active_items()
        attach_reqres(resp)
        assert resp.status_code == 200
   
   
    events = resp.json()
    with allure.step('Проверка, что данные приходят'):
        assert events

    slug = events[0]["offers"][0]["slug"]

    resp = get_item(slug)
    assert resp.status_code == 200
    offer_data = resp.json()
    assert "moderated_offer" in offer_data
    offer_id = offer_data["moderated_offer"]["id"]

    resp = get_delivery_time(offer_id)
    assert resp.status_code == 200

    data = resp.json()
    assert data

    with allure.step('Проверка времени доставки товара'):
        assert data['days_to_deliver'] >= 0
        assert "delivery_time" in data
        assert data['moderated_offer_id'] == offer_id


@allure.parent_suite("Главная страница")
@allure.suite("Проверка отзывов по товару")
@allure.title("Получение offer_reviews")
def test_offer_reviews():

    with allure.step('Отправление запроса на отзывы по товару'):
        resp = get_active_items()
        attach_reqres(resp)
        assert resp.status_code == 200
        slug = resp.json()[0]["offers"][0]["slug"]

    resp = get_item(slug)
    assert resp.status_code == 200
    offer_data = resp.json()

    with allure.step('Проверка moderated_offer'):
        assert "moderated_offer" in offer_data
        offer_id = offer_data["moderated_offer"]["id"]

    resp = get_offer_reviews(offer_id)
    assert resp.status_code == 200
    data = resp.json()

    with allure.step('Проверка, что  отзывы есть и они в списке'):
        assert "offer_reviews" in data
        assert isinstance(data["offer_reviews"], list)

    if "total" in data and data["total"] > 0:
        assert len(data["offer_reviews"]) > 0



@allure.parent_suite("Главная страница")
@allure.suite("Проверка сервиса offers_v2")
@allure.title("Валидация структуры и значений offers_v2")
def test_offers_v2():
    with allure.step('Получение offers_v2'):
        resp = get_offers_v2("1d8ffdfb-a9d1-45f3-82a2-05b0f3448944")
        attach_reqres(resp)
        assert resp.status_code == 200

    data = resp.json()

    with allure.step('Получение offers_v2 в data'):
         assert "offers" in data
         assert isinstance(data["offers"], list)
         assert len(data["offers"]) > 0

    offer = data["offers"][0]

    with allure.step('Проверка названия и цены'):
        assert "name" in offer and offer["name"]
        assert "price" in offer and offer["price"] > 0

    assert "partner" in offer
    partner = offer["partner"]
    assert partner["id"] > 0
    assert isinstance(partner["name"], str) and partner["name"]
    if partner["rating"] is not None:
        assert 0 <= partner["rating"] <= 5

    with allure.step('Проверка условий'):
        assert "conditions" in offer and isinstance(offer["conditions"], list)
        for cond in offer["conditions"]:
            assert cond["duration"] > 0
            assert cond["commission"] >= 0






@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у неавторизованного пользователя')
@allure.title("Получение товаров")
def test_get_active_items():
    global offer_id, slug, condition_id

    with allure.step('Отправка запроса на получение товара'):
        response = get_active_items()
        attach_reqres(response)

    with allure.step('Проверка статуса ответа'):
        assert response.status_code == 200

    response = response.json()

    with allure.step("Проверка, что в ответе есть товары"):
        assert len(response) > 0

    first_item = response[0]["offers"][0]
    offer_id = first_item["moderated_offer_id"]
    slug = first_item["slug"]
    condition_id = first_item["condition"]["id"]


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у неавторизованного пользователя')
@allure.title("Получение session_id из куки")
def test_get_session_id():
    global cookie

    with allure.step('Отправка запроса на получение корзины'):
        response = get_cart()
        attach_reqres(response=response)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200

    with allure.step("Получение session_id из куки"):
        cookie = response.cookies.get_dict()['cart']
        assert isinstance(cookie, str), f'Тип куки на самом деле {type(cookie)}'


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у неавторизованного пользователя')
@allure.title("Добавление товара в корзину")
def test_add_item():

    with allure.step('Добавление в корзину'):
        response = add_to_cart(cookie=cookie, offer_id=offer_id, condition_id=condition_id)
        attach_reqres(response=response)


    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200

    response = response.json()

@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у неавторизованного пользователя')
@allure.title("Проверка корзины после добавления товара ")
def test_get_cart_after_add():

    with allure.step('Проверка корзины'):
        response=get_cart(cookie)
        attach_reqres(response=response)
        assert response.status_code == 200

    with allure.step('В Корзине что-то должно быть'):
        res_json = response.json()
        assert res_json["total_items_count"] > 0, "Корзина должна содержать хотя бы 1 товар"
        assert "moderated_cart_items" in res_json and len(res_json["moderated_cart_items"]) > 0, "Нет товаров в корзине"


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у неавторизованного пользователя')
@allure.title("Добавление одного и того же товара дважды")
def test_add_same_item_twice():
    with allure.step('Добавление товаров в корзину'):
        add_to_cart(cookie, offer_id, condition_id, 1)
        add_to_cart(cookie, offer_id, condition_id, 1)
        

    response = get_cart(cookie)
    res_json = response.json()

    with allure.step('Проверка общего количества товара'):
        assert res_json["total_items_count"] >= 2
        attach_reqres(response=response)
    
    with allure.step('Проверка количества именно нашего товара'):
        assert res_json["moderated_cart_items"][0]["quantity"] >= 2


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у неавторизованного пользователя')
@allure.title("Проверка, что товар совпадает с добавленным")
def test_cart_items_match():
    with allure.step('Проверка корзины'):
        response=get_cart(cookie)
        attach_reqres(response=response)

    with allure.step('Проверка совпадения товара'):
        res_json = response.json()
        assert res_json["moderated_cart_items"][0]["moderated_offer_id"] == offer_id


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у неавторизованного пользователя')
@allure.title("Проверка суммы total")
def test_total_items_count_sync():
    with allure.step('Проверка корзины'):
        response=get_cart(cookie)
        attach_reqres(response=response)
    
    res_json = response.json()

    with allure.step('Проверка суммы'):
        total_items_count = res_json["total_items_count"]
        real_count = sum([item["quantity"] for item in res_json["moderated_cart_items"]])
        assert total_items_count == real_count, "Сумма quantity должна совпадать с total_items_count"
















