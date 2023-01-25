import pandas as pd

from engenharia.etl.tipos import Linhas


def transformar_campos(tabela_de_entrada: pd.DataFrame) -> Linhas:
    linhas_da_saída = []
    for i, linha in tabela_de_entrada.iterrows():
        if pd.isnull(linha["Situação"]):
            linhas_da_saída.append(
                {"Data": linha["Data"].date(),
                 "Valor": linha["Crédito R$"] if not pd.isnull(linha["Crédito R$"]) else linha["Débito R$"],
                 "Categoria": linha["Nome do Cartão"],
                 "Descrição": linha["Histórico"],
                 "De": "Pagarme" if linha["CPF/CNPJ Origem/Destino"] == "18.727.053/0001-74"
                                 else "Conta Simples MEI" if pd.isnull(linha["Crédito R$"])
                                                      else "Externo",
                 "Para": "Conta Simples MEI" if not pd.isnull(linha["Crédito R$"]) else "Externo"}
            )
    return [[None if pd.isnull(valor) else str(valor).replace(".", ",") for valor in linha]
                           for linha in pd.DataFrame(linhas_da_saída).values.tolist()]