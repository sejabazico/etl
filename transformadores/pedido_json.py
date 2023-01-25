from functools import reduce
from operator import add

from tipos import List, Union, Pedido, Linhas, Tabela


def único(pedido: Pedido, cabeçalho=True) -> Union[Tabela, Linhas]:
    dados_do_pedido = {"N° do Pedido": pedido["pedido"]["numero"],
            "N° do Pedido na Loja Virtual": nPL if (nPL := pedido["pedido"].get("numeroPedidoLoja", None)) is not None
                                                else pedido["pedido"].get("numeroPedidoLoja", None),
            "Status": pedido["pedido"]["situacao"],
            "Data": pedido["pedido"]["data"],
            "ID contato": pedido["pedido"]["cliente"]["id"],
            "Nome do contato": pedido["pedido"]["cliente"]["nome"],
            "Cpf/Cnpj": pedido["pedido"]["cliente"]["cnpj"],
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
            "Nº da NFe": pedido["pedido"]["parcelas"][0]["parcela"]["forma_pagamento"]["codigoFiscal"]
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


def múltiplos(pedidos: List[Pedido], cabeçalho=True) -> Union[Tabela, Linhas]:
    return reduce(add, [único(pedido, cabeçalho=(i==0 and cabeçalho)) for i, pedido in enumerate(pedidos)])
