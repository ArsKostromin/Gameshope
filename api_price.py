import requests

api_url = "http://127.0.0.1:8000/store/api/game/"



# Делаем GET-запрос
response = requests.get(api_url, )

# Печатаем статус-код и данные, если запрос успешен
if response.status_code == 200:
    data = response.json()
    for i in data['results']:
        if int(i['price'])>0:
            print(i)
else:
    print(f"Ошибка при запросе: {response.status_code}")
    print(response.text)
