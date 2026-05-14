import requests

def test_key(key):
    # Тест для Яндекс Геокодера
    yandex_url = "https://geocode-maps.yandex.ru/1.x/"
    yandex_params = {
        'geocode': '37.617633,55.755826',  # Москва
        'format': 'json',
        'apikey': key
    }
    yandex_response = requests.get(yandex_url, params=yandex_params)
    print("Яндекс:", yandex_response.status_code, yandex_response.json())

    # Тест для Google Geocoding API
    google_url = "https://maps.googleapis.com/maps/api/geocode/json"
    google_params = {
        'latlng': '55.7558,37.6173',
        'key': key
    }
    google_response = requests.get(google_url, params=google_params)
    print("Google:", google_response.status_code, google_response.json())

test_key("f3a0fe3a-b07e-4840-a1da-06f18b2ddf13")