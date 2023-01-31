from itertools import count
from pathlib import Path

import requests
import json

from tipos import List, Pedido, Produto


APIKEY = "a3e36e25a52e280465de4b060619486ff2cd0292395bfdac81482c015293b25b250c3104"
CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"


def todos_os_pedidos(apikey: str = APIKEY, salvar_json=True) -> List[Pedido]:
    pedidos = []
    for i in count(1, step=1):
        resposta = requests.get(f"https://bling.com.br/Api/v2/pedidos/page={i}/json/",
                                params={"apikey": apikey}).json()
        if "erros" in resposta["retorno"].keys():
            código_do_erro = resposta["retorno"]["erros"][0]["erro"]["cod"]
            if código_do_erro == 14:
                break
        else:
            pedidos += resposta["retorno"]["pedidos"]

    if salvar_json:
        with open(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "todos_os_pedidos.json", "w") as arquivo:
            json.dump(pedidos, arquivo)
        print('Arquivo todos_os_pedidos.json salvo.')

    return pedidos


def todos_os_produtos(apikey: str = APIKEY, salvar_json=True) -> List[Produto]:
    produtos = []
    for i in count(1, step=1):
        resposta = requests.get(f"https://bling.com.br/Api/v2/produtos/page={i}/json/",
                                params={'apikey': apikey, 'estoque': 'S'}).json()
        if 'erros' in resposta['retorno'].keys():
            codigo_do_erro = resposta['retorno']['erros'][0]['erro']['cod']
            if codigo_do_erro == 14:
                break
        else:
            produtos += resposta['retorno']['produtos']

    if salvar_json:
        with open(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "produtos.json", "w") as arquivo:
            json.dump(produtos, arquivo)
        print('Arquivo produtos.json salvo.')

    return produtos


if __name__ == '__main__':
    resultado = todos_os_pedidos()
    print(resultado[25])