import os, psycopg, uvicorn
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

PORT=8411

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DB_URL")

print(DB_URL)
# Create DB connection
conn = psycopg.connect(DB_URL, autocommit=True, row_factory=dict_row)


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/temp")
def temp():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM messages")
        messages = cur.fetchall()
        return messages

rooms = [
    {"number": 100, "type": "single" },
    {"number": 101, "type": "double"},
    {"number": 102, "type": "suite"}]

@app.get("/rooms")
def room(request: Request):
    return rooms

# Get one room
@app.get("/rooms/{id}")
def get_one_room(id: int):
    try:
        return rooms[id]
    except:
        return { "error": "Room not found" }

# Create booking
@app.post("/bookings")
def create_booking(request: Request):
    return { "msg": "booking created!"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )
