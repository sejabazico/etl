import extratores
import transformadores
import carregadores

from tipos import IO


def transações_da_conta_simples() -> IO:
    carregadores.google_planilhas.adicionador_de_linhas(
        transformadores.extrato_planilha.transformar_campos(
            extratores.conta_simples.ler_relatórios()),
        planilha="1fEV60EKcDpgODsI77evyERcZIre8zRhC7mFnrQcl1Jo",
        intervalo="Transações!A:F")


if __name__ == '__main__':
    transações_da_conta_simples()