import json
import requests
import xml.etree.ElementTree as ET
from fastapi import FastAPI
import uvicorn

valutes_dict = {}
name_to_CharCode = {}

app = FastAPI()

class CB_Valute_Extract():  
    def init(self):
        global valutes_dict
        global name_to_CharCode

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
            name_to_CharCode[valute.find('CharCode').text] = valute.find('Name').text
    
            print(valute.find('Name').text)
            print(valute.find('Value').text)
            print(valute.find('CharCode').text)

    def getSalaryRub(self, amount, valute):
        result = float(valutes_dict[name_to_CharCode.get(valute)]) * amount

        json_result = json.dumps(str(result))
        print(json.loads(json_result))

        return json_result


try:
    example = CB_Valute_Extract()
    example.init()

    @app.get("/getCurrency/")
    async def read_item(curr: str = 'USD', amount: float = 0):
        print(curr)
        print(amount)
        return example.getSalaryRub(amount, curr)

#    if __name__ == "__main__":
#        uvicorn.run(app, host="0.0.0.0", port=8000)
# Это для дебагера.


except AttributeError:
    print("-1")


