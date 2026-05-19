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
def get_gold_price():
    apikey = os.environ.get("TWELVEDATA_KEY", "97de42f6b07e45f094d2efb021c8428a")
    
    # ดึงราคาปัจจุบัน
    r1 = requests.get(
        f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={apikey}",
        timeout=10
    )
    
    # ดึง quote (high/low/open/close/change)
    r2 = requests.get(
        f"https://api.twelvedata.com/quote?symbol=XAU/USD&apikey={apikey}",
        timeout=10
    )
    
    if r1.status_code != 200 or r2.status_code != 200:
        raise HTTPException(status_code=502, detail="Unable to fetch price")
    
    price_data = r1.json()
    quote_data = r2.json()
    
    price = float(price_data.get("price", 0))
    open_p = float(quote_data.get("open", price))
    high_p = float(quote_data.get("high", price))
    low_p = float(quote_data.get("low", price))
    prev_p = float(quote_data.get("previous_close", price))
    change = price - prev_p
    chp = (change / prev_p * 100) if prev_p else 0

    return {
        "price": price,
        "open_price": open_p,
        "high_price": high_p,
        "low_price": low_p,
        "prev_close_price": prev_p,
        "ch": round(change, 2),
        "chp": round(chp, 4),
        "ask": round(price + 0.3, 2),
        "bid": round(price - 0.3, 2),
        "timestamp": quote_data.get("timestamp", "")
    }
