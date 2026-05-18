import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/gold-price")
def get_gold_price(symbol: str = "XAU", currency: str = "USD"):
    response = requests.get(
        f"https://www.goldapi.io/api/{symbol}/{currency}",
        headers={
            "x-access-token": os.environ["GOLDAPI_KEY"],
            "Content-Type": "application/json",
        },
        timeout=10,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Unable to fetch price")
    data = response.json()
    return {
        "symbol": data.get("metal", symbol),
        "currency": data.get("currency", currency),
        "price": data.get("price"),
        "open_price": data.get("open_price"),
        "high_price": data.get("high_price"),
        "low_price": data.get("low_price"),
        "prev_close_price": data.get("prev_close_price"),
        "ask": data.get("ask"),
        "bid": data.get("bid"),
        "ch": data.get("ch"),
        "chp": data.get("chp"),
        "timestamp": data.get("timestamp"),
    }
