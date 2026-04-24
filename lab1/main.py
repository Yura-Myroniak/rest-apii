from fastapi import FastAPI
from api.books import router

app = FastAPI()

app.include_router(router)
@app.get("/")
def root():
    return {"message": "API працює"}