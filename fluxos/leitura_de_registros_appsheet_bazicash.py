from pathlib import Path

import carregadores
import extratores
import transformadores
from tipos import IO


CHAVE_DE_SERVICO_SHEETS = Path(__file__).parent.parent / "carregadores" / "credenciais" / \
                           "google_sheets_credentials.json"
CAMINHO_PARA_LISTA_DE_IDS_DE_ACRESCIMO_ENVIADOS = Path(__file__).parent.parent / "cache" / "ids_de_acrescimo.txt"


ID_PLANILHA_DIM_CLIENTE = '1SRsNyFsvbRgTrlOqGC1Pd9G7G15qXgr0AjWbXGOqYZ8'
NOME_ABA_DIM_CLIENTE = 'dados'
ID_PLANILHA_REGISTROS_TRANSACOES = '1bOpypFRgh4bA5gewLLb7jF8qANNpu5012NMS1GXl4LE'
NOME_ABA_REGISTROS_TRANSACOES = 'teste'
NOME_ABA_ERROS_AO_ENVIAR_PARA_API = 'erros_ao_acrescentar'


def leitura_de_registros_appsheet_bazicash() -> IO:

    transformadores.logs_bazicash_appsheet.lista_de_ids_de_transacoes_positivas_a_enviar(
        dados_clientes=extratores.google_planilhas.ler_planilha(
            service_file_path=CHAVE_DE_SERVICO_SHEETS,
            spreadsheet_id=ID_PLANILHA_DIM_CLIENTE,
            sheet_name=NOME_ABA_DIM_CLIENTE
        ),
        dados_transacoes = extratores.google_planilhas.ler_planilha(
            service_file_path=CHAVE_DE_SERVICO_SHEETS,
            spreadsheet_id=ID_PLANILHA_REGISTROS_TRANSACOES,
            sheet_name=NOME_ABA_REGISTROS_TRANSACOES
        )
    )


if __name__ == '__main__':
    leitura_de_registros_appsheet_bazicash()