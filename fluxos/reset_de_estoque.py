from pathlib import Path

import extratores
import transformadores
import carregadores

from tipos import IO


CHAVE_DA_TABELA = '1IKZapbvzGuEYKyBmCck5CvqzIyDBwg_krLwlW0lkiak'
NOME_DA_TABELA = 'Relatório de Estoque'
ID_PROJETO = 'datalake-375813'
NOME_BUCKET_LAYER_RAW = 'bzco_layer_raw'
NOME_BUCKET_LAYER_2 = 'bzco_layer_2'
CAMINHO_PRODUTOS_JSON = Path(__file__).parent.parent / "cache" / "produtos.json"
CAMINHO_PRODUTOS_PARQUET = Path(__file__).parent.parent / "cache" / "produtos.parquet"


def reset_de_estoque() -> IO:
    carregadores.google_planilhas.write_to_gsheet(
        transformadores.estoque_json.listar_produtos(
            extratores.bling.todos_os_produtos()),
        service_file_path=carregadores.google_planilhas.CAMINHO_PARA_CREDENCIAIS,
        spreadsheet_id=CHAVE_DA_TABELA,
        sheet_name=NOME_DA_TABELA)
    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PRODUTOS_JSON,
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_RAW,
        nome_do_blob="produtos.json")
    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PRODUTOS_PARQUET,
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_2,
        nome_do_blob="produtos.parquet")


if __name__ == '__main__':
    reset_de_estoque()


