import json
import os
from urllib.parse import urljoin, quote_plus
from urllib.request import Request, urlopen
from flask import Flask, render_template

class BrasilIO:

    base_url = "https://api.brasil.io/v1/"
    def __init__(self, auth_token):
        self.__auth_token = auth_token

    @property
    def headers(self):
        return {
            'User-Agent': 'python-urllib/brasilio-client-0.1.0'
        }

    @property
    def api_headers(self):
        data = self.headers
        data.update({"Authorization": f"Token {self.__auth_token}"})
        # print("Token: ", data)
        return data

    def request_data(self, path, query_string):
        url = urljoin(self.base_url, path)
        if query_string:
            url += "?" + query_string

        try:
            json_file = open("data.json")
            json_response = json.load(json_file)
        except IOError:
            print("JSON não existe")

            json_file = open("data.json", "w")
            json_file.write("")
            json_file.close()

            request = Request(url, headers=self.api_headers)
            response = urlopen(request)

            json_response = json.load(response)

            json_file = open("data.json", "w")
            json_file.write(json.dumps(json_response))

            print("JSON criado")
        finally:
            json_file.close()

        return json_response

    def get_data(self, dataset_slug, table_name):
        url_path = f"dataset/{dataset_slug}/{table_name}/data/"
        query_string = "mesano_de_referencia=2018-01-01"

        response = self.request_data(url_path, query_string)

        return response

    def filter_and_format(self, data):
        data = data
        total_payment = 0
        count_daily_rate = 0

        for row in data["results"]:
            daily_rate = float(row["diarias"])
            if(daily_rate > 1000):
                count_daily_rate += 1

            total_payment += float(row["rendimento_liquido"])

        payment_info = "Pagamento total foi de: {:.2f}".format(total_payment)
        total_daily_rate = "O total de pessoas que receberam diárias acima de 1000 reais foi: {}".format(count_daily_rate)
        print(payment_info)
        print(total_daily_rate)
        return

# app = Flask(__name__)
#
# @app.route("/")
# def index():
#   return render_template('index.html')

if __name__ == "__main__":
    api_token = os.getenv("API_TOKEN")
    api = BrasilIO(api_token)
    dataset_slug = "salarios-magistrados"
    table_name = "contracheque"
    # api.api_headers()

    data = api.get_data(dataset_slug, table_name)
    api.filter_and_format(data)

    # app.run(payment_info=payment_info, total_daily_rate=total_daily_rate)
