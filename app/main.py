
import os
from typing import Union

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
#from typing import List
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

# templates = Jinja2Templates(directory="templates")


# Modelos

class Order(BaseModel):
    id: int
    user_id: int
    products: str
    total_price: float


# Datos de ejemplo

orders = []
# templates = Jinja2Templates(directory="templates")

def get_next_order_id():
    return max([order.id for order in orders], default=0) + 1

@app.get("/")
async def read_root():
    return {"Hello": "World And Aliens"}

@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "app/static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None,):
    return {"item_id": item_id, "q": q}


# TAREA

@app.get("/orders")
def get_orders():
    return orders

@app.post("/orders")
def create_order(order: Order):
    for o in orders:
        if o.id == order.id:
            raise HTTPException(status_code=400, detail="Esta orden ya existe")
        
    orders.append(order)
    return {"message": "Orden creada"}

@app.put("/orders/{order_id}")
def update_order(order_id: int, order:Order):
    for idx, o in enumerate(orders):
        if o.id == order_id:
            orders[idx] = order
            return order
    return {"message": "Orden actualizada"}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for idx, o in enumerate(orders):
        if o.id == order_id:
            del orders[idx]
            return {"message": "Orden eliminada"}
    return {"error: producto no encontrado"}    