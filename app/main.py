from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI()

# Модель для входных данных
class Request(BaseModel):
    imei: str
    token: str

# Эндпоинт, который принимает POST-запрос с двумя строками
@app.post("/api/check-imei")
async def fetch_data(user_request: Request):
    # Здесь можно использовать строки для формирования запроса к стороннему ресурсу
    # Например, передаем их как параметры запроса
    url = "https://api.imeicheck.net/v1/checks"  # Замените на реальный URL стороннего ресурса

    headers = {
    'Authorization': f'Bearer {user_request.token}',
    'Content-Type': 'application/json'
    }

    body = ({
    "deviceId": f'{user_request.imei}',
    "serviceId": 12
    })

    try:
        # Отправляем GET-запрос на сторонний ресурс
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return data

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
