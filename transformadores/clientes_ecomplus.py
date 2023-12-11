from functools import reduce
from operator import add
from pathlib import Path

import pandas as pd
import fastparquet as fp

from tipos import Cliente, Union, Linhas, Tabela, List

import extratores


CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"


def único(cliente: Cliente, cabeçalho=True) -> Union[Tabela, Linhas]:
    dados_do_cliente = {"id_ecomplus_do_cliente": cliente["_id"],
                       "cpf": cliente.get("doc_number") or None,
                       "e-mail": cliente["main_email"],
                       "bazicashs_ativos": sum(desconto.get("active_points", 0)
                                               for desconto in cliente.get("loyalty_points_entries", []))}

    if cabeçalho:
        return [list(dados_do_cliente.keys())] + [list(dados_do_cliente.values())]
    else:
        return [list(dados_do_cliente.values())]


def múltiplos(clientes: List[Cliente], cabeçalho=True, salvar_parquet=True) -> Union[Tabela, Linhas]:
    dados_listados = reduce(add, [único(cliente, cabeçalho=(i == 0 and cabeçalho))
                                  for i, cliente in enumerate(clientes)])

    if salvar_parquet and cabeçalho:
        tabela = pd.DataFrame(dados_listados[1:], columns=dados_listados[0])

        fp.write(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "clientes_ecomplus.parquet", data=tabela)

    tabela.to_excel(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "clientes.xlsx", index=False)

    return dados_listados


if __name__ == '__main__':
    múltiplos(extratores.ecomplus.todos_os_clientes())