from pathlib import Path

import pandas as pd

PASTA_DOS_RELATÓRIOS = Path(__file__).parent / ".." / "fontes_locais" / "relatórios_da_conta_simples"


def ler_relatórios() -> pd.DataFrame:
    tabela_de_entrada = pd.concat(pd.read_excel(planilha, header=7).iloc[::-1]
                                  for planilha in PASTA_DOS_RELATÓRIOS.iterdir())
    tabela_de_entrada["Data"] = pd.to_datetime(tabela_de_entrada["Data"], dayfirst=True)
    return tabela_de_entrada
