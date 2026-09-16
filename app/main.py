from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()


def get_product_by_id(connection_string: str, product_id: int):
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM products WHERE Product_id = :id"),
            {"id": product_id},
        )
        return result.fetchall()


@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"message": f"product {product_id} in stock"}
