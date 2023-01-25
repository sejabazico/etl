from engenharia.etl import extratores, transformadores

import pygsheets


caminho_credenciais = 'credenciais/google_sheets_credentials.json'
chave_tabela = '1IKZapbvzGuEYKyBmCck5CvqzIyDBwg_krLwlW0lkiak'
nome_da_tabela = 'Relatório de Estoque'


def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
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
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1
    print("Processo Finalizado!!!")


df = transformadores.estoque_json.listar_produtos(
    extratores.bling.todos_os_produtos()
)


write_to_gsheet(caminho_credenciais, chave_tabela, nome_da_tabela, df)


