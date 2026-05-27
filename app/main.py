from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base, Producto, Categoria, Pedido

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def inicio():
    return {"mensaje": "API de tienda online"}

@app.get("/productos")
def obtener_productos(db: Session = Depends(get_db)):

    productos = db.query(Producto).all()

    return productos

@app.get("/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):

    producto = db.query(Producto).filter(
        Producto.id_producto == id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto

@app.post("/productos")
def crear_producto(
    nombre: str,
    precio: float,
    stock: int,
    id_categoria: int,
    db: Session = Depends(get_db)
    
    ):
    nuevo_producto = Producto(
    nombre=nombre,
    precio=precio,
    stock=stock,
    id_categoria=id_categoria
    )
    db.add(nuevo_producto)

    db.commit()

    db.refresh(nuevo_producto)

    return nuevo_producto

@app.put("/productos/{id}")
def actualizar_producto(
    id: int,
    nombre: str,
    precio: float,
    stock: int,
    db: Session = Depends(get_db)
):

    producto = db.query(Producto).filter(
        Producto.id_producto == id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto.nombre = nombre
    producto.precio = precio
    producto.stock = stock

    db.commit()

    db.refresh(producto)

    return producto

@app.delete("/productos/{id}")
def eliminar_producto(
    id: int,
    db: Session = Depends(get_db)
):

    producto = db.query(Producto).filter(
        Producto.id_producto == id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    db.delete(producto)

    db.commit()

    return {"mensaje": "Producto eliminado correctamente"}

@app.get("/pedidos-detallados")
def pedidos_detallados(db: Session = Depends(get_db)):

    resultado = (
        db.query(
            Pedido.id_pedido,
            Producto.nombre.label("producto"),
            Categoria.nombre.label("categoria"),
            Pedido.cantidad,
            Pedido.total_pago,
            Pedido.fecha_pedido
        )
        .join(
            Producto,
            Pedido.id_producto == Producto.id_producto
        )
        .join(
            Categoria,
            Producto.id_categoria == Categoria.id_categoria
        )
        .all()
    )

    pedidos = []

    for fila in resultado:
        pedidos.append({
            "id_pedido": fila.id_pedido,
            "producto": fila.producto,
            "categoria": fila.categoria,
            "cantidad": fila.cantidad,
            "total_pago": float(fila.total_pago),
            "fecha_pedido": fila.fecha_pedido
        })

    return pedidos

@app.get("/categorias")
def obtener_categorias(db: Session = Depends(get_db)):

    categorias = db.query(Categoria).all()

    return categorias

@app.post("/pedidos")
def crear_pedido(
    id_producto: int,
    cantidad: int,
    db: Session = Depends(get_db)
):

    producto = db.query(Producto).filter(
        Producto.id_producto == id_producto
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    if producto.stock < cantidad:
        raise HTTPException(
            status_code=400,
            detail="Stock insuficiente"
        )

    total = producto.precio * cantidad

    nuevo_pedido = Pedido(
        id_producto=id_producto,
        cantidad=cantidad,
        total_pago=total
    )

    db.add(nuevo_pedido)

    producto.stock -= cantidad

    db.commit()

    db.refresh(nuevo_pedido)

    return nuevo_pedido