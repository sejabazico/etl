import os

from google.cloud import storage
from pathlib import Path

from tipos import IO

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../arquivos/credenciais/chave_datalake.json'


def subir_para_o_bucket(caminho_do_arquivo: Path, id_projeto: str, nome_do_bucket: str) -> IO:
    cliente_storage = storage.Client(project=id_projeto)
    bucket = cliente_storage.bucket(nome_do_bucket)
    blob = bucket.blob(caminho_do_arquivo)
    blob.upload_from_filename(caminho_do_arquivo)

