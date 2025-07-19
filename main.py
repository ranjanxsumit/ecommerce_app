import os
from fastapi import FastAPI
from routers import products, orders

app = FastAPI(title="HROne E-Commerce API")

app.include_router(products.router, tags=["Products"])
app.include_router(orders.router, tags=["Orders"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the E-Commerce API"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
