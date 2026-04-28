from fastapi import FastAPI

app = FastAPI(title="Cookmate AI=")

@app.get("/health")
def health():
    return {"status": {"ok"}}