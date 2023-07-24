from functools import reduce
from operator import add
from pathlib import Path

import pandas as pd
import fastparquet as fp

from tipos import Pedido, Union, Linhas, Tabela, List

import extratores


CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"


def único_ecomplus(pedido: Pedido, cabeçalho=True) -> Union[Tabela, Linhas]:
    dados_do_pedido = {"Numero do Pedido Ecomplus": pedido["number"],
                       "Cpf": pedido["buyers"][0]["doc_number"],
                       "Nome": pedido["buyers"][0]["display_name"],
                       "E-mail": pedido["buyers"][0]["main_email"],
                       "Id do Cliente na Ecomplus": pedido["buyers"][0]["_id"],
                       "Data": pedido["created_at"],
                       "Cupom": pedido.get("extra_discount", {}).get("discount_coupon") or None}

    if cabeçalho:
        return [list(dados_do_pedido.keys())] + [list(dados_do_pedido.values())]
    else:
        return [list(dados_do_pedido.values())]


def múltiplos_ecomplus(pedidos: List[Pedido], cabeçalho=True, salvar_parquet=True) -> Union[Tabela, Linhas]:
    dados_listados = reduce(add, [único_ecomplus(pedido, cabeçalho=(i == 0 and cabeçalho))
                                  for i, pedido in enumerate(pedidos)])

    if salvar_parquet and cabeçalho:
        tabela = pd.DataFrame(dados_listados[1:], columns=dados_listados[0])

        fp.write(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "pedidos_ecomplus.parquet", data=tabela)

    return dados_listados


if __name__ == '__main__':
    print(múltiplos_ecomplus(extratores.ecomplus.todos_os_pedidos()))