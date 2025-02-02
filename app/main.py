from fastapi import FastAPI, HTTPException, Depends, status
import requests
from pydantic import BaseModel

from config import *

app = FastAPI()

class Request(BaseModel):
    imei: str
    token: str

def verify_token(authorization: Request):
    token_list = token_list
    if not authorization.token in token_list():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            deatil = 'Invalid token'
        )
    return True

@app.post("/api/check-imei")
async def fetch_data(user_request: Request, verification: bool = Depends(verify_token)):
    url = "https://api.imeicheck.net/v1/checks"
    api_key = api_key

    headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
    }

    body = ({
    "deviceId": f'{user_request.imei}',
    "serviceId": 12
    })

    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
