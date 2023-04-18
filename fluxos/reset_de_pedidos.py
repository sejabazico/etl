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
IDENTITY_TOKEN = ("eyJhbGciOiJSUzI1NiIsImtpZCI6IjI3NDA1MmEyYjY0NDg3NDU3Nj"
                  "RlNzJjMzU5MDk3MWQ5MGNmYjU4NWEiLCJ0eXAiOiJKV1QifQ.eyJpc"
                  "3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI"
                  "zMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsI"
                  "mF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQ"
                  "uY29tIiwic3ViIjoiMTA3NTc3ODc3NDg0MTMzMTYyMjYwIiwiZW1ha"
                  "WwiOiJkYWRvcy5iYXppY29AZ21haWwuY29tIiwiZW1haWxfdmVyaWZ"
                  "pZWQiOnRydWUsImF0X2hhc2giOiJmUzUxVXRyamtPaWdCY2dlelRvQ"
                  "Ux3IiwiaWF0IjoxNjc1MzY2NzUxLCJleHAiOjE2NzUzNzAzNTF9.tD"
                  "qrfkO_34Ovms8SGKFF7N1WbK4x7wU_pwV_gbHNZ_aHC-PXE6G3jPF1"
                  "PkrNOJ20WPxj6nI-xPQJ1tLuTg3A3RXrvuCRgV-UCpX0zqThEgsGzZ"
                  "QZ43g823wE7hTxMhX28S2Vcni8Tjj2CawHEdoyja8yv64vYIwEfDPb"
                  "it0B2MO23BSM8dyKE0N2POx99lNlvrXTao9Zbe5Ru2hI5oZSqpX3p0"
                  "jrk1Q0jaIAFhcRggimXGXS7ejJbLlSJfnuBzfVpVE57tFM8OGdAOjr"
                  "0PTBvJx2fmkpdjmkiw7GOnxKypVOO8Tj2B49HMlmzGuiklHBV7ppaF"
                  "8ycio6jBM8rPU4Hw")


def gatilho_da_cloud_function(url: str):
    headers = {"Authorization": f"bearer {IDENTITY_TOKEN}",
               "Content-Type": "application/json"}
    data = {"acionador": "qualquer"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request succeeded with status code:", response.status_code)
        print("Response content:", response.content)
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content)


def reset_de_pedidos() -> IO:
    carregadores.google_planilhas.construtor_de_tabelas(
        transformadores.pedido_json.múltiplos(
            extratores.bling.todos_os_pedidos()),
        planilha="1ZYMvRXGn2-koFUTyJO2fTqp6eYf1dS91NYZhn_Y8ByY",
        intervalo="'Base do Bling'!A:AD")

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
