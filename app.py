from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "Bangame Bot is running 🚀"
    }

@app.post("/webhook")
async def webhook(data: dict):
    print(data)
    return {"ok": True}
# Render Redeploy