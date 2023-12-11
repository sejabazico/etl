import datetime
import json
import pickle
from itertools import count
from pathlib import Path

import requests

from tipos import Pedido


ID_LOJA = "51292"
API_KEY = "a454166eade58d1905a90b250de4ec569144de38617fe7ea17c1dd618b64422e549651b669ae976b1c75c8ecf6834760" \
          "d8dbec4ad1027bc26743621a53518152"
MY_ID = "6435a3834bd2e929c1cb30c8"
CACHE_ACCESS_TOKEN_DATA = Path(__file__).parent.parent / "cache" / "access_token_data.b"
CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"


def get_access_token():
    if CACHE_ACCESS_TOKEN_DATA.exists():
        with open(CACHE_ACCESS_TOKEN_DATA, "rb") as cache_access_token_data_file:
            access_token_data = pickle.load(cache_access_token_data_file)
        if (access_token_data["expires"] - datetime.datetime.today()).days == 0:
            return access_token_data["access_token"]

    response = requests.post(url="https://api.e-com.plus/v1/_authenticate.json",
                             headers={"Content-Type": "application/json",
                                      "X-Store-ID": ID_LOJA},
                             json={"$schema": "http://json-schema.org/draft-04/schema#",
                                   "type": "object",
                                   "properties": {"_id": {"type": "string"},
                                                  "api_key": {"type": "string"}},
                                   "required": ["_id", "api_key"],
                                   "_id": MY_ID,
                                   "api_key": API_KEY})
    access_token_data = response.json()
    access_token_data["expires"] = datetime.datetime.strptime(access_token_data["expires"], '%Y-%m-%dT%H:%M:%S.%fZ')

    with open(CACHE_ACCESS_TOKEN_DATA, "wb") as cache_access_token_data_file:
        pickle.dump(access_token_data, cache_access_token_data_file)

    return access_token_data["access_token"]


def todos_os_pedidos(salvar_json=True) -> list[Pedido]:
    access_token = get_access_token()

    dados = []
    for i in count(0, step=1000):
        response = requests.get(url="https://api.e-com.plus/v1/orders.json",
                                 headers={"Content-Type	": "application/json",
                                          "X-Store-ID": ID_LOJA,
                                          "X-Access-Token": access_token,
                                          "X-My-ID": MY_ID},
                                params={"limit": 1000,
                                        "offset": {i},
                                        "fields": ",".join(["_id",
                                                   "source_name",
                                                   "channel_id",
                                                   "number",
                                                   "code",
                                                   "status",
                                                   "financial_status.updated_at",
                                                   "financial_status.current",
                                                   "fulfillment_status.updated_at",
                                                   "fulfillment_status.current",
                                                   "amount",
                                                   "payment_method_label",
                                                   "shipping_method_label",
                                                   "buyers._id",
                                                   "buyers.main_email",
                                                   "buyers.display_name",
                                                   "buyers.doc_number",
                                                   "items.product_id",
                                                   "items.sku",
                                                   "items.name",
                                                   "items.quantity",
                                                   "created_at",
                                                   "updated_at",
                                                   "extra_discount"])}).json()

        if len(response["result"]) == 0:
            break
        else:
            dados += response["result"]

    if salvar_json:
        with open(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "todos_os_pedidos_ecomplus.json", "w") as arquivo:
            json.dump(dados, arquivo)
        print("Arquivo todos_os_pedidos_ecomplus.json salvo!!")

    return dados


def todos_os_clientes(salvar_json=True) -> list[Pedido]:
    access_token = get_access_token()

    clientes = []
    for i in count(0, step=1000):
        response = requests.get(url="https://api.e-com.plus/v1/customers.json",
                                headers={"Content-Type	": "application/json",
                                         "X-Store-ID": ID_LOJA,
                                         "X-Access-Token": access_token,
                                         "X-My-ID": MY_ID},
                                params={"limit": 1000,
                                        "offset": {i},
                                        "fields": ",".join(["_id",
                                                            "name",
                                                            "main_email",
                                                            "doc_number",
                                                            "loyalty_points_entries"])}).json()

        if len(response["result"]) == 0:
            break
        else:
            clientes += response["result"]

    if salvar_json:
        with open(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "todos_os_clientes_ecomplus.json", "w") as arquivo:
            json.dump(clientes, arquivo)
        print("Arquivo todos_os_clientes_ecomplus.json salvo!!")

    return clientes


if __name__ == '__main__':
    todos_os_clientes()
