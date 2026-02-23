import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, select, func, String, Integer, Column 
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel

# CONFIGURACIÓN
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@db:5432/bar_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# MODELOS SQLALCHEMY
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    proveedor = Column(String) 

class ShiftTask(Base):
    __tablename__ = "shift_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    shift_name: Mapped[str] = mapped_column(String(50)) 
    checklist: Mapped[list] = mapped_column(JSONB, default=list)

Base.metadata.create_all(bind=engine)

# SCHEMAS PYDANTIC 
class ProductCreate(BaseModel):
    nombre: str
    stock_actual: int
    stock_minimo: int
    proveedor: Optional[str] = None

# APP
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def seed_data():
    with SessionLocal() as db:
        count = db.scalar(select(func.count()).select_from(Product))
        if count == 0:
            p1 = Product(nombre="Cerveza Cruzcampo", stock_actual=3, stock_minimo=10, proveedor="Distribuidora S.A.")
            p2 = Product(nombre="Coca-Cola", stock_actual=20, stock_minimo=10, proveedor="Keiko")
            p3 = Product(nombre="Aceite de Oliva", stock_actual=2, stock_minimo=5, proveedor="Aceites del Sur")
            
            t1 = ShiftTask(
                shift_name="Mañana", 
                checklist=[{"item": "Revisar cámaras", "done": True}]
            )
            db.add_all([p1, p2, p3, t1])
            db.commit()

# ENDPOINTS
@app.get("/orders/check")
def check_low_stock(db: Session = Depends(get_db)):
    stmt = select(Product).where(Product.stock_actual < Product.stock_minimo)
    low_stock_products = db.scalars(stmt).all()
    
    order_list = []
    for item in low_stock_products:
        order_list.append({
            "id": item.id,
            "producto": item.nombre,
            "stock_actual": item.stock_actual,
            "minimo_requerido": item.stock_minimo,
            "cantidad_a_pedir": (item.stock_minimo * 2) - item.stock_actual,
            "proveedor": item.proveedor
        })
    return {"lista_de_compra": order_list}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(ShiftTask)).all()

@app.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    nuevo = Product(
        nombre=product.nombre,
        stock_actual=product.stock_actual,
        stock_minimo=product.stock_minimo,
        proveedor=product.proveedor
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

