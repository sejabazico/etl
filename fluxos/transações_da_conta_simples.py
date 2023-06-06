import extratores
import transformadores
import carregadores

from tipos import IO


def transações_da_conta_simples() -> IO:
    carregadores.google_planilhas.adicionador_de_linhas(
        transformadores.extrato_planilha.transformar_e_pré_processar(
            extratores.conta_simples.ler_relatórios()),
        planilha="1a-urnrV2DwjRwFWGQcjiF7TqbTlF1cfdRVzKslMIe9w",
        intervalo="'Transações da ContaSimples'!A:O")


if __name__ == '__main__':
    transações_da_conta_simples()
