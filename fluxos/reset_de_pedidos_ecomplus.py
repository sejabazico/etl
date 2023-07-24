from pathlib import Path

import carregadores
import extratores
import transformadores
from tipos import IO


ID_PROJETO = 'datalake-375813'
NOME_BUCKET_LAYER_RAW = 'bzco_layer_raw'
NOME_BUCKET_LAYER_2 = 'bzco_layer_2'
CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"


def reset_de_pedidos_ecomplus() -> IO:
    transformadores.pedido_ecomplus_json.múltiplos_ecomplus(
        extratores.ecomplus.todos_os_pedidos())

    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PARA_ARQUIVOS_DE_CACHE / "todos_os_pedidos_ecomplus.json",
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_RAW,
        nome_do_blob="todos_os_pedidos_ecomplus.json")
    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PARA_ARQUIVOS_DE_CACHE / "pedidos_ecomplus.parquet",
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_2,
        nome_do_blob="pedidos_ecomplus.parquet")


if __name__ == '__main__':
    reset_de_pedidos_ecomplus()