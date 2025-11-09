from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json, os, random

app = FastAPI(title="SlotBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")

if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.get("/api/balance/{user_id}")
async def get_balance(user_id: int):
    db = load_db()
    balance = db.get(str(user_id), 1000)
    return {"balance": balance}

@app.post("/api/spin")
async def spin(request: Request):
    data = await request.json()
    user_id = str(data.get("user_id"))
    bet = int(data.get("bet", 10))
    db = load_db()
    balance = db.get(user_id, 1000)

    if balance < bet:
        return {"error": "Недостаточно средств"}

    # Симуляция выигрыша (пример вероятностей)
    win = random.choice([0, bet * 2, bet * 5, 0, 0, bet * 3])
    new_balance = balance - bet + win
    db[user_id] = new_balance
    save_db(db)

    return {"bet": bet, "win": win, "balance": new_balance}
