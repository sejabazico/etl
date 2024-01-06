from pathlib import Path

import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from datetime import datetime
import pandas as pd
import pygsheets

from tipos import Tabela, IO, Linhas, Tuple


RecursoDeInteraçãoComAPI = Resource
CódigoDeIdentificaçãoDePlanilha = str


CAMINHO_PARA_CREDENCIAIS = Path(__file__).parent / "credenciais" / "google_sheets_credentials.json"

FUSO_HORÁRIO = pytz.timezone("America/Bahia")


def iniciar_serviço_da_api_do_sheets(caminho_para_credenciais: Path = CAMINHO_PARA_CREDENCIAIS
                                     ) -> RecursoDeInteraçãoComAPI:
    escopos = ['https://www.googleapis.com/auth/spreadsheets']
    credenciais = service_account.Credentials.from_service_account_file(caminho_para_credenciais,
                                                                        scopes=escopos)
    return build('sheets', 'v4', credentials=credenciais).spreadsheets()

def construtor_de_tabelas(tabela: Tabela,
                          planilha: CódigoDeIdentificaçãoDePlanilha,
                          intervalo: str,
                          ) -> IO:
    operação = iniciar_serviço_da_api_do_sheets().values().update(
        spreadsheetId=planilha,
        range=intervalo,
        valueInputOption="USER_ENTERED",
        body={"values": tabela}
    ).execute()

    print(f'{operação.get("updatedCells")} células atualizadas.')
    #f'Última atualização: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')


def ultima_atualizacao():
    def hora_para_planilha(credentials_path,spreadsheet_id,sheet_name,data):
        gc = pygsheets.authorize(service_file=credentials_path)
        sh = gc.open_by_key(spreadsheet_id)
        try:
            sh.add_worksheet(sheet_name)
        except:
            pass
        wks_write = sh.worksheet_by_title(sheet_name)
        wks_write.clear('A1', None, '*')
        wks_write.set_dataframe(data, (1, 1), encoding='utf-8', fit=True)
        wks_write.frozen_rows = 1

    hora = [datetime.now(FUSO_HORÁRIO).strftime("%d/%m/%Y %H:%M:%S")]
    hora_df = pd.DataFrame(data=hora, index=None, columns=None)
    credencials = CAMINHO_PARA_CREDENCIAIS
    spreadsheet_id = "1IKZapbvzGuEYKyBmCck5CvqzIyDBwg_krLwlW0lkiak"
    sheet_name = "Última Atualização"
    hora_para_planilha(credencials, spreadsheet_id, sheet_name, hora_df)
    print(f'Última atualização: {hora[0]}')

def adicionador_de_linhas(linhas: Linhas,
                          planilha: CódigoDeIdentificaçãoDePlanilha,
                          intervalo: str
                          ) -> IO:
    operação = iniciar_serviço_da_api_do_sheets().values().append(
        spreadsheetId=planilha,
        range=intervalo,
        valueInputOption="USER_ENTERED",
        body={"values": linhas}
    ).execute()

    print(f'{operação.get("updates").get("updatedCells")} células atualizadas')

def apagador_de_linhas(planilha: CódigoDeIdentificaçãoDePlanilha,
                       aba: int,
                       índices: Tuple[int, int]
                       ) -> IO:
    requisições = {"requests": [{"deleteDimension": {"range": {"sheetId": aba,
                                                               "dimension": "ROWS",
                                                               "startIndex": índices[0],
                                                               "endIndex": índices[1] + 1}}}]}
    resposta = iniciar_serviço_da_api_do_sheets().batchUpdate(
        spreadsheetId=planilha,
        body=requisições
    ).execute()




chave_tabela = '1IKZapbvzGuEYKyBmCck5CvqzIyDBwg_krLwlW0lkiak'
nome_da_tabela = 'Relatório de Estoque'


def write_to_gsheet(data_df: Tabela, service_file_path: Path, spreadsheet_id: str, sheet_name: str) -> IO:
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)

    existing_data_df = wks_write.get_as_df()

    combined_data = pd.concat([existing_data_df, data_df], ignore_index=True)

    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(combined_data, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1
    print("Processo Finalizado!!!")