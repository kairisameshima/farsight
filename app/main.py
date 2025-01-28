from fastapi import FastAPI
from app.routes import trends

app = FastAPI()
app.include_router(trends.router, prefix="/api", tags=["trends"])


@app.get("/")
def read_root():
    return {"Hello": "World"}