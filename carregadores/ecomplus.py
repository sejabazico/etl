import requests

from extratores.ecomplus import get_access_token

token = get_access_token()

'''
id_ecomplus = '657ca72b2cd6b65959def013'

url_cliente = f"https://api.e-com.plus/v1/customers/{id_ecomplus}.json"

response = requests.patch(
    url=url_cliente,
    headers={
        "Content-Type	": "application/json",
        "X-Store-ID": "51292",
        "X-Access-Token": token,
        "X-My-ID": "6435a3834bd2e929c1cb30c8"
    },
    params={
        "fields": id_ecomplus
    }
)
'''


STORE_ID = 51292
MY_ID = '6435a3834bd2e929c1cb30c8'


def adicionar_pontos_em_id(id_ecomplus:str, informacoes):
    url_cliente = f"https://api.e-com.plus/v1/customers/{id_ecomplus}/loyalty_points_entries.json"
    response = requests.post(
        url=url_cliente,
        headers={
            "Content-Type	": "application/json",
            "X-Store-ID": "51292",
            "X-Access-Token": token,
            "X-My-ID": "6435a3834bd2e929c1cb30c8"
        },
        params={
            "name": "Bazicash",
            "program_id": "p0_pontos",
            "earned_points": informacoes['earned_points'],
            "active_points": informacoes['active_points'],
            "ratio": 0.1,
            "valid_thru": informacoes['valid_thru']
        }
    )

    if response.status_code == 200 or response.status_code == 204:
        print(f'Pontos acrescentados ao id: {id_ecomplus} com sucesso.')
    else:
        print(f'Erro ao acrescentar pontos ao id: {id_ecomplus}. Status de erro: {response.status_code}')