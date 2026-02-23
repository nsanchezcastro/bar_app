import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, select, func, String, Integer
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

# CONFIGURACIÓN DE LA BASE DE DATOS
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@db:5432/bar_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# SQLAlchemy
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    stock: Mapped[int] = mapped_column(default=0)
    min_stock: Mapped[int] = mapped_column(default=5)
    provider_name: Mapped[str] = mapped_column(String(100))

class ShiftTask(Base):
    __tablename__ = "shift_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    shift_name: Mapped[str] = mapped_column(String(50)) 
    checklist: Mapped[list] = mapped_column(JSONB, default=list)

Base.metadata.create_all(bind=engine)

# FASTAPI 
app = FastAPI(title="Gestión de Cocina - El Bar")

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

# FUNCIÓN PARA DATOS INICIALES 
@app.on_event("startup")
def seed_data():
    with SessionLocal() as db:
        count = db.scalar(select(func.count()).select_from(Product))
        if count == 0:
            p1 = Product(name="Cerveza Cruzcampo", stock=3, min_stock=10, provider_name="Distribuidora S.A.")
            p2 = Product(name="Coca-Cola", stock=20, min_stock=10, provider_name="Keiko")
            p3 = Product(name="Aceite de Oliva", stock=2, min_stock=5, provider_name="Aceites del Sur")
            
            t1 = ShiftTask(    #Tarea inicial de ejemplo
                shift_name="Mañana", 
                checklist=[
                    {"item": "Revisar cámaras", "done": True},
                    {"item": "Preparar sofrito croquetas", "done": False}
                    
                ]
            )
            
            db.add_all([p1, p2, p3, t1])
            db.commit()
            print("--- Base de Datos poblada con éxito ---")

# ENDPOINTS

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de la Cocina del Bar"}

# Endpoint para control de Stock y pedidos
@app.get("/orders/check")
def check_low_stock(db: Session = Depends(get_db)):
    stmt = select(Product).where(Product.stock < Product.min_stock)
    low_stock_products = db.scalars(stmt).all()
    
    order_list = []
    for item in low_stock_products:
        order_list.append({
            "producto": item.name,
            "stock_actual": item.stock,
            "minimo_requerido": item.min_stock,
            "cantidad_a_pedir": (item.min_stock * 2) - item.stock, # Pedir para doblar el mínimo
            "proveedor": item.provider_name
        })
    
    return {
        "pedidos_pendientes": len(order_list),
        "lista_de_compra": order_list
    }

# Endpoint para tareas
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    stmt = select(ShiftTask)
    tasks = db.scalars(stmt).all()
    return tasks

# Endpoint para crear productos 
@app.post("/products")
def create_product(
    name: str, 
    stock: int, 
    min_stock: int, 
    provider_name: str, 
    db: Session = Depends(get_db)
):
    nuevo_p = Product(
        name=name, 
        stock=stock, 
        min_stock=min_stock, 
        provider_name=provider_name
    )
    db.add(nuevo_p)
    db.commit()
    db.refresh(nuevo_p)
    return {"message": "Producto añadido con éxito", "id": nuevo_p.id}

@app.put("/products/{product_id}")
def update_product(product_id: int, name: str, stock: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="No encontrado")
    product.name = name
    product.stock = stock
    db.commit()
    return {"message": "Actualizado"}