import re
from pathlib import Path

import pandas as pd

PASTA_DOS_RELATÓRIOS = (Path(__file__)
                        .parent
                        .parent
                        / "fontes_locais"
                        / "relatórios_da_conta_simples")


def ler_relatórios() -> pd.DataFrame:
    tabelas = []
    for planilha in PASTA_DOS_RELATÓRIOS.iterdir():
        caso = re.findall(r"\[(.+)\]", planilha.name)[0]
        
        dados_da_planilha = pd.read_excel(planilha)
        coluna_1 = dados_da_planilha.iloc[:, 0].tolist()
        linhas_de_cabeçalho = coluna_1.index("Data") + 1

        match caso:
            case "Cartões":
                tabelas.append(pd.read_excel(planilha, header=linhas_de_cabeçalho)
                               .iloc[::-1]
                               .rename(columns={"Nome do estabelecimento": "Histórico",
                                                "Crédito": "Crédito R$",
                                                "Débito": "Débito R$"})
                               .assign(**{"Saldo R$": ""}))
            case "Conta":
                tabelas.append(pd.read_excel(planilha, header=linhas_de_cabeçalho).iloc[::-1])
            case _:
                raise Exception(f"Caso {caso} desconhecido")

    tabela_de_entrada = pd.concat(tabelas)
    tabela_de_entrada["Data"] = pd.to_datetime(tabela_de_entrada["Data"], dayfirst=True)
    return tabela_de_entrada.sort_values(by="Data", ascending=True).reset_index(drop=True)
