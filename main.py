from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from database_models import Product as DBProduct, Base
import database_models
from models import Product, ProductCreate

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)
Base.metadata.create_all(bind=engine)

products =[Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
           Product(id=2, name="Smartphone", description="A latest model smartphone", price=499.99, quantity=20)
                   ]

def init_db():
    db =SessionLocal()
    count =db.query(database_models.Product).count()

    if(count == 0):
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    db.commit()
    db.close()

init_db()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet():
    return "Hello, World!"

@app.get("/products", response_model=list[Product])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(DBProduct).all()
    return products

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = DBProduct(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product