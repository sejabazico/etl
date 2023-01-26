import os

from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../arquivos/credenciais/chave_datalake.json'


def subir_para_o_bucket(caminho_do_arquivo, id_projeto, nome_do_bucket):
    cliente_storage = storage.Client(project=id_projeto)
    bucket = cliente_storage.bucket(nome_do_bucket)
    blob = bucket.blob(caminho_do_arquivo)
    blob.upload_from_filename(caminho_do_arquivo)

