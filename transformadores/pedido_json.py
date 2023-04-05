import os
from functools import reduce
from operator import add
from pathlib import Path

from tipos import List, Union, Pedido, Linhas, Tabela

import fastparquet as fp
import pandas as pd


CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"


def único(pedido: Pedido, cabeçalho=True) -> Union[Tabela, Linhas]:
    dados_do_pedido = {"Número do Pedido": pedido["pedido"]["numero"],
            "Número do Pedido na Loja Virtual": nPL if (nPL := pedido["pedido"].get("numeroPedidoLoja", None)) is not None
                                                else pedido["pedido"].get("numeroPedidoLoja", None),
            "Status": pedido["pedido"]["situacao"],
            "Data": pedido["pedido"]["data"],
            "ID contato": pedido["pedido"]["cliente"]["id"],
            "Nome do contato": pedido["pedido"]["cliente"]["nome"],
            "Cpf ou Cnpj": pedido["pedido"]["cliente"]["cnpj"],
            "Endereço": pedido["pedido"]["cliente"]["endereco"],
            "Bairro": pedido["pedido"]["cliente"]["bairro"],
            "Município": pedido["pedido"]["cliente"]["cidade"],
            "Estado": pedido["pedido"]["cliente"]["uf"],
            "CEP": pedido["pedido"]["cliente"]["cep"],
            "E-mail": pedido["pedido"]["cliente"]["email"],
            "Telefone": celular if ((celular := pedido["pedido"]["cliente"]["celular"]) != ""
                                    and celular is not None)
                                else pedido["pedido"]["cliente"]["fone"],
            "Desconto do pedido": pedido["pedido"]["desconto"].replace(",", "."),
            "Frete": pedido["pedido"]["valorfrete"],
            "Observações": pedido["pedido"]["observacoes"],
            "Vendedor": pedido["pedido"]["vendedor"],
            "Número da NFe": pedido["pedido"]["parcelas"][0]["parcela"]["forma_pagamento"]["codigoFiscal"]
                         if "parcelas" in pedido["pedido"].keys() else None,
            "Forma de pagamento": pedido["pedido"]["parcelas"][0]["parcela"]["forma_pagamento"]["descricao"]
                                  if "parcelas" in pedido["pedido"].keys() else None,
            "Preço Total do pedido": pedido["pedido"]["totalvenda"],
            "Preço Total dos produtos": pedido["pedido"]["totalprodutos"]}

    itens =  [{"ID do Produto": item["item"]["codigo"],
               "Descrição do Produto": item["item"]["descricao"],
               "Preço Unitário": item["item"]["valorunidade"],
               "Custo Unitário": item["item"]["precocusto"],
               "Quantidade": item["item"]["quantidade"]}
              | dados_do_pedido
              for item in pedido["pedido"]["itens"]]

    if cabeçalho:
        return [list(itens[0].keys())] + [list(item.values()) for item in itens]
    else:
        return [list(item.values()) for item in itens]


def múltiplos(pedidos: List[Pedido], cabeçalho=True, salvar_parquet=True) -> Union[Tabela, Linhas]:
    dados = reduce(add, [único(pedido, cabeçalho=(i == 0 and cabeçalho)) for i, pedido in enumerate(pedidos)
                         if "itens" in pedido["pedido"].keys()])

    if salvar_parquet and cabeçalho:
        if not CAMINHO_PARA_ARQUIVOS_DE_CACHE.exists():
            os.mkdir(CAMINHO_PARA_ARQUIVOS_DE_CACHE)

        tabela = pd.DataFrame(dados[1:], columns=dados[0])

        tabela['Preço Unitário'] = pd.to_numeric(tabela['Preço Unitário'], errors='coerce')
        tabela['Custo Unitário'] = pd.to_numeric(tabela['Custo Unitário'], errors='coerce')
        tabela['Quantidade'] = pd.to_numeric(tabela['Quantidade'], errors='coerce', downcast='integer')
        tabela['Número do Pedido'] = pd.to_numeric(tabela['Número do Pedido'], errors='coerce')
        tabela['Número do Pedido na Loja Virtual'] = pd.to_numeric(tabela['Número do Pedido na Loja Virtual'], errors='coerce')
        tabela['ID contato'] = pd.to_numeric(tabela['ID contato'], errors='coerce', downcast='integer')
        tabela['Desconto do pedido'] = pd.to_numeric(tabela['Desconto do pedido'], errors='coerce', downcast='float')
        tabela['Frete'] = pd.to_numeric(tabela['Frete'], errors='coerce')
        tabela['Preço Total do pedido'] = pd.to_numeric(tabela['Preço Total do pedido'], errors='coerce')
        tabela['Preço Total dos produtos'] = pd.to_numeric(tabela['Preço Total dos produtos'], errors='coerce')

        tabela['Data'] = tabela['Data'].apply(lambda data: data.replace("-", ""))

        fp.write(CAMINHO_PARA_ARQUIVOS_DE_CACHE / "pedidos.parquet", data=tabela)

    return dados
