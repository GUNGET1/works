from locale import currency
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/getCurrency/")

def read_item(curr: str = None, amount: float = 0):
    print(curr)
    print(amount)
    return "Hello World!"




#  url = 'http://localhost/getCurrency?curr_usd&amount50'