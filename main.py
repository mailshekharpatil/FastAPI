from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greet():
    return "Hello, World!"

products=[{"id": 1, "name": "Product 1", "description": "Description of Product 1", "price": 10.99, "quantity": 100}]

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}