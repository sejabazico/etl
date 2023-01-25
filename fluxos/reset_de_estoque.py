import extratores
import transformadores
import carregadores

from tipos import IO


CHAVE_DA_TABELA = '1IKZapbvzGuEYKyBmCck5CvqzIyDBwg_krLwlW0lkiak'
NOME_DA_TABELA = 'Relatório de Estoque'


def reset_de_estoque() -> IO:
    carregadores.google_planilhas.write_to_gsheet(
        transformadores.estoque_json.listar_produtos(
            extratores.bling.todos_os_produtos()),
        service_file_path=carregadores.google_planilhas.CAMINHO_PARA_CREDENCIAIS,
        spreadsheet_id=CHAVE_DA_TABELA,
        sheet_name=NOME_DA_TABELA)


if __name__ == '__main__':
    reset_de_estoque()
