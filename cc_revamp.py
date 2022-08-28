import json
import requests
import xml.etree.ElementTree as ET
from fastapi import FastAPI

valutes_dict = {}
app = FastAPI()

class CB_Valute_Extract():  
    def init(self):
        global valutes_dict
        url = "http://www.cbr.ru/scripts/XML_daily.asp?"
        response = requests.get(url)
        string = response.content
        parsed_response = ET.fromstring(string)

        # Здесь надо перегнать в строку, иначе...
        # Exception has occurred: TypeError
        # a bytes-like object is required, not 'Response'

        # Вообще я не уверен, что есть "парсинг", но...

        for valute in parsed_response.findall('Valute'):

            valutes_dict[valute.find('Name').text] = valute.find('Value').text.replace(",", ".")
    
            print(valute.find('Name').text)
            print(valute.find('Value').text)

    def getSalaryRub(self, amount, valute):
        result = float(valutes_dict[valute]) * amount

        json_result = json.dumps(str(result))
        print(json.loads(json_result))

        return json_result


try:
    example = CB_Valute_Extract()
    example.init()

    @app.get("/getCurrency/")
    def read_item(curr: str = None, amount: float = 0):
        print(curr)
        print(amount)
        return example.getSalaryRub(amount, curr)


except AttributeError:
    print("-1")


