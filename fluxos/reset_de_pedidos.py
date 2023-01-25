from engenharia.etl import extratores, transformadores, carregadores

from engenharia.etl.tipos import IO


def reset_de_pedidos() -> IO:
    carregadores.google_planilhas.construtor_de_tabelas(
        transformadores.pedido_json.múltiplos(
            extratores.bling.todos_os_pedidos()),
        planilha="1ZYMvRXGn2-koFUTyJO2fTqp6eYf1dS91NYZhn_Y8ByY",
        intervalo="'Base do Bling'!A:AA")
    carregadores.google_planilhas.ultima_atualizacao()


if __name__ == '__main__':
    reset_de_pedidos()
