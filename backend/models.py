from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    stock: Mapped[int] = mapped_column(default=0)
    min_stock: Mapped[int] = mapped_column(default=5) # Para pedido automático
    
    # JSONB 
    provider_info: Mapped[dict] = mapped_column(JSONB, nullable=True)

class ShiftTask(Base):
    __tablename__ = "shift_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    shift_name: Mapped[str] = mapped_column(String(20)) 
    checklist: Mapped[list] = mapped_column(JSONB)