import os
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def add_cors(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.options("/{path:path}")
async def options_handler():
    return JSONResponse(content={}, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })

@app.get("/gold-price")
def get_gold_price():
    apikey = os.environ.get("TWELVEDATA_KEY", "97de42f6b07e45f094d2efb021c8428a")
    r1 = requests.get(f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={apikey}", timeout=10)
    r2 = requests.get(f"https://api.twelvedata.com/quote?symbol=XAU/USD&apikey={apikey}", timeout=10)
    if r1.status_code != 200 or r2.status_code != 200:
        raise HTTPException(status_code=502, detail="Unable to fetch price")
    p = r1.json()
    q = r2.json()
    price = float(p.get("price", 0))
    open_p = float(q.get("open", price))
    high_p = float(q.get("high", price))
    low_p = float(q.get("low", price))
    prev_p = float(q.get("previous_close", price))
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
        "timestamp": q.get("timestamp", "")
    }

@app.get("/health")
def health():
    return {"status": "ok"}
