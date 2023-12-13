from pathlib import Path

import pandas as pd
import pygsheets

from tipos import IO

CAMINHO_PARA_CREDENCIAIS = Path(__file__).parent.parent / "carregadores" / "credenciais" / \
                           "google_sheets_credentials.json"


def ler_planilha(service_file_path: Path, spreadsheet_id: str, sheet_name: str) -> IO:
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    wks = sh.worksheet_by_title(sheet_name)
    dados = wks.get_as_df()

    return dados


if __name__ == '__main__':
    ler_planilha(
        service_file_path=CAMINHO_PARA_CREDENCIAIS,
        spreadsheet_id='1dl-S36NOiUvu54D8R0FWtJFZ   BO5dgmNeOfxruCPFiTI',
        sheet_name='relatório de estoque'
    )