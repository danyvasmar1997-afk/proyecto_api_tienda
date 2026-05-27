from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(150))
    
class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), nullable=False)

    precio = Column(DECIMAL(10,2), nullable=False)

    stock = Column(Integer, default=0)

    id_categoria = Column(
        Integer,
        ForeignKey("categorias.id_categoria")
    )

class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, index=True)

    id_producto = Column(
        Integer,
        ForeignKey("productos.id_producto")
    )

    cantidad = Column(Integer, nullable=False)

    fecha_pedido = Column(DateTime)

    total_pago = Column(DECIMAL(10,2), nullable=False)