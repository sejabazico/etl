from pathlib import Path

import requests

import extratores
import transformadores
import carregadores
from tipos import IO


ID_PROJETO = 'datalake-375813'
NOME_BUCKET_LAYER_RAW = 'bzco_layer_raw'
NOME_BUCKET_LAYER_2 = 'bzco_layer_2'
CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"
IDENTITY_TOKEN = ("eyJhbGciOiJSUzI1NiIsImtpZCI6IjI3NDA1MmEyYjY0NDg3NDU3NjRlNzJjMzU5MDk3"
                  "MWQ5MGNmYjU4NWEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY"
                  "29tIiwiYXpwIjoiNjE4MTA0NzA4MDU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zM" 
                  "m42ZGdxLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNjE4MTA0NzA4M"
                  "DU0LTlyOXMxYzRhbGczNmVybGl1Y2hvOXQ1Mm4zMm42ZGdxLmFwcHMuZ29vZ2xldXNlc"
                  "mNvbnRlbnQuY29tIiwic3ViIjoiMTA3NTc3ODc3NDg0MTMzMTYyMjYwIiwiZW1haWwiO"
                  "iJkYWRvcy5iYXppY29AZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X"
                  "2hhc2giOiJ4aXZjVFVzTHQtUzVZdFZFZ0d3b2JnIiwiaWF0IjoxNjc1MzYxNzU1LCJle"
                  "HAiOjE2NzUzNjUzNTUsImp0aSI6ImI1ODAyZDhhOTlkNWNlZTUzNjliZjdhNzBmMDBmN"
                  "GY3ZGQ1ZDYzMjkifQ.uuUQRiTxLaJYAmf5vbWkDeVC92BlTUlN9BdMsWSGdMYLKXez6p"
                  "P0_PQA0qz7y0LASJjpIL4zeviKSdYsIvvcbLYTujre_eco45CHUXLnJdfokWRm5N-39c"
                  "nWMOJ2jmthDfAOg5y9uDhq9R5IKnJpfxOUsw8G8RZLeOwC3If9yAHTeq0fr5zLBoiXp-"
                  "HwneTemrJoZ_NvJ4okgMyDZBQq9eVcvVyiJaqED9SSfg9h3j4zAawjBLcVGkLB67O6FO"
                  "65eY6ztytsW-lw8BoTy81DvMD9Jmgt0PQgAn9CFjEPnDNDiweeKuderkm9i8_yE2Jf3A"
                  "Dw1mnmwvmx4URrWOk80A")


def gatilho_da_cloud_function():
    url = "https://sobrescrever-tabela-de-pedidos-znz5wp6mbq-uc.a.run.app"
    headers = {"Authorization": f"bearer {IDENTITY_TOKEN}",
               "Content-Type": "application/json"}
    data = {"acionador": "qualquer"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request succeeded with status code: ", response.status_code)
        print("Response content: ", response.content)
    else:
        print("Request failed with status code: ", response.status_code)
        print("Response content: ", response.content)


def reset_de_pedidos() -> IO:
    carregadores.google_planilhas.construtor_de_tabelas(
        transformadores.pedido_json.múltiplos(
            extratores.bling.todos_os_pedidos()),
        planilha="1ZYMvRXGn2-koFUTyJO2fTqp6eYf1dS91NYZhn_Y8ByY",
        intervalo="'Base do Bling'!A:AA")

    carregadores.google_planilhas.ultima_atualizacao()

    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PARA_ARQUIVOS_DE_CACHE / "todos_os_pedidos.json",
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_RAW,
        nome_do_blob="todos_os_pedidos.json")
    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PARA_ARQUIVOS_DE_CACHE / "pedidos.parquet",
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_2,
        nome_do_blob="pedidos.parquet")
    gatilho_da_cloud_function()


if __name__ == '__main__':
    reset_de_pedidos()
