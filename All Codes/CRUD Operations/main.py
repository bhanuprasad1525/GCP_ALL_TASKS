from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db import get_connection
import mysql.connector

app = FastAPI(title="Customer API")

class Customer(BaseModel):
    name: str
    email: str


@app.get("/")
def health():
    return {"status": "API running"}


@app.post("/customers", status_code=201)
def create_customer(customer: Customer):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customer (name, email) VALUES (%s, %s)",
            (customer.name, customer.email)
        )
        conn.commit()
        return {"message": "Customer created"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/customers")
def get_customers():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM customer")
        return cur.fetchall()
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


@app.get("/customers/{id}")
def get_customer(id: int):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM customer WHERE id=%s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Customer not found")

    return row


@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE customer SET name=%s, email=%s WHERE id=%s",
        (customer.name, customer.email, id)
    )
    conn.commit()

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    cur.close()
    conn.close()
    return {"message": "Customer updated"}


@app.delete("/customers/{id}")
def delete_customer(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM customer WHERE id=%s", (id,))
    conn.commit()

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    cur.close()
    conn.close()
    return {"message": "Customer deleted"}
