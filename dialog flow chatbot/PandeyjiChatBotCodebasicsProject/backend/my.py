
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse


import generic_helper

app = FastAPI()

inprogress_orders = {}


@app.get("/")

async def root():
    return {"message": "Hello World"}

def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })