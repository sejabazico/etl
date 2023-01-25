import extratores
import transformadores
import carregadores

from tipos import IO


def reset_de_produtos() -> IO:
    carregadores.google_planilhas.construtor_de_tabelas(
        transformadores.estoque_json.listar_produtos(
            extratores.bling.todos_os_produtos()),
        planilha= '1ZYMvRXGn2-koFUTyJO2fTqp6eYf1dS91NYZhn_Y8ByY',
        intervalo="'Produtos2.0'!A:G")


if __name__ == '__main__':
    reset_de_produtos()