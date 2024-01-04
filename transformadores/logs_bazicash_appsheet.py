import os
from pathlib import Path
import re
from datetime import datetime
from json import loads, dumps

import extratores
from carregadores import ecomplus
from tipos import Registro, Union, Tabela, Linhas, Cliente
import pandas as pd


CHAVE_DE_SERVICO_SHEETS = Path(__file__).parent.parent / "carregadores" / "credenciais" / \
                           "google_sheets_credentials.json"
CAMINHO_PARA_LISTA_DE_IDS_DE_ACRESCIMO_ENVIADOS = Path(__file__).parent.parent / "cache" / "ids_de_acrescimo.txt"


ID_PLANILHA_DIM_CLIENTE = '1SRsNyFsvbRgTrlOqGC1Pd9G7G15qXgr0AjWbXGOqYZ8'
NOME_ABA_DIM_CLIENTE = 'dados'
ID_PLANILHA_REGISTROS_TRANSACOES = '1bOpypFRgh4bA5gewLLb7jF8qANNpu5012NMS1GXl4LE'
NOME_ABA_REGISTROS_TRANSACOES = 'teste'



def formatar_cpf(cpf_original: str):
    cpf_desagrupado = re.findall('\d+', str(cpf_original))
    cpf = "".join([str(parte_do_cpf) for parte_do_cpf in cpf_desagrupado])
    max_len_cpf = 11
    max_len_cnpj = 14
    if len(cpf) >= max_len_cnpj:
        return cpf[:max_len_cnpj]
    if len(cpf) == max_len_cpf:
        return cpf
    cpf_arrumado = '0' * (max_len_cpf - len(cpf)) + cpf
    return cpf_arrumado


def refinamento_de_transacao(registro: Registro) -> Union[Tabela, Linhas]:
    dados_da_transacao = pd.Series({
        "id_transacao": registro["id_transacao"],
        "tipo": registro["tipo"],
        "cpf": formatar_cpf(registro["cpf"]),
        "valor": registro["valor"],
        "atendente": registro["atendente"]
    })

    return dados_da_transacao


def refinamento_de_cliente(cliente:Cliente) -> Union[Tabela, Linhas]:
    dados_do_cliente = pd.DataFrame({
        "cpf": [formatar_cpf(cliente["cpf_ou_cnpj"])],
        "id_ecomplus": [cliente.get("id_ecomplus") or None]
    })

    return dados_do_cliente


def agrupamento_de_clientes(clientes:Tabela) -> Tabela:
    clientes_refinados = pd.DataFrame(columns=['cpf', 'id_ecomplus'])
    for i, cliente in clientes.iterrows():
        #print(f'O cliente de índice {i} e nome {cliente["nome"]} foi adicionado')
        #print(refinamento_de_cliente(cliente))
        clientes_refinados = pd.concat([clientes_refinados, refinamento_de_cliente(cliente)], ignore_index=True)

    return clientes_refinados


def cruzamento_de_cpf_e_id(cpf:str, clientes:Tabela) -> str:
    for i, cliente in clientes.iterrows():
        if cliente['cpf'] == cpf:
            return cliente.get('id_ecomplus') or None
    return 'não encontrado'


def acrescentar_id_ecomplus_na_transacao(dados_clientes:Tabela, dados_transacoes:Tabela):
    transacoes = pd.DataFrame(columns=['id_transacao', 'tipo', 'cpf', 'valor', 'atendente', 'id_ecomplus'])

    for i, registro in dados_transacoes.iterrows():
        transacao = refinamento_de_transacao(registro).to_frame().T
        transacoes = pd.concat([transacoes, transacao], ignore_index=True)

        cpf = transacao['cpf'].iloc[0]
        transacoes.at[i, 'id_ecomplus'] = cruzamento_de_cpf_e_id(cpf, agrupamento_de_clientes(dados_clientes))

    return transacoes


def registros_de_acrescimo(transacoes:pd.DataFrame) -> pd.DataFrame:
    transacoes_positivas = transacoes.loc[transacoes['tipo'] == 'Acréscimo'].copy()

    transacoes_positivas.loc[:, 'name'] = 'Bazicash'
    transacoes_positivas.loc[:, 'program_id'] = 'p0_pontos'
    transacoes_positivas.loc[:, 'ratio'] = 0.1
    transacoes_positivas.loc[:, 'earned_points'] = transacoes_positivas['valor']
    transacoes_positivas.loc[:, 'active_points'] = transacoes_positivas['valor']

    transacoes_positivas = transacoes_positivas[[
        'id_transacao',
        'id_ecomplus',
        'name',
        'program_id',
        'earned_points',
        'active_points',
        'ratio']]

    return transacoes_positivas


def lista_de_ids_de_acrescimo_já_enviados(caminho:Path):
    try:
        with open(caminho, 'r') as lista:
            return [id.strip() for id in lista]
    except FileNotFoundError:
        return []


def acrescentar_novos_ids_de_acrescimo_enviados(caminho, lista_atualizada_de_ids):
    if not os.path.exists(caminho):
        # Create the file if it doesn't exist
        with open(caminho, 'w'):
            pass

    with open(caminho, 'a') as file:
        file.write('\n'.join(lista_atualizada_de_ids) + '\n')


def lista_de_ids_de_transacoes_positivas_a_enviar(transacoes_de_acrescimo:pd.DataFrame):
    transacoes_enviadas = []
    current_time = datetime.now()

    ids_transacoes_de_acrescimo = lista_de_ids_de_acrescimo_já_enviados(CAMINHO_PARA_LISTA_DE_IDS_DE_ACRESCIMO_ENVIADOS)

    novas_transacoes_de_acrescimo = transacoes_de_acrescimo[
        ~transacoes_de_acrescimo['id_transacao'].isin(ids_transacoes_de_acrescimo)]

    if novas_transacoes_de_acrescimo.empty:
        print(f'A execução foi encerrada por não ter encontrado novos registros de acréscimos de Bazicashs.')

    if not novas_transacoes_de_acrescimo.empty:
        print(f'Novas transações foram identificadas.')
        print(novas_transacoes_de_acrescimo)

        transacoes_enviadas.extend(novas_transacoes_de_acrescimo['id_transacao'].tolist())

        acrescentar_novos_ids_de_acrescimo_enviados(
            CAMINHO_PARA_LISTA_DE_IDS_DE_ACRESCIMO_ENVIADOS,
            transacoes_enviadas)

        novas_transacoes_de_acrescimo = novas_transacoes_de_acrescimo.drop(
            ['id_transacao'], axis=1
        )

        for i, registro in novas_transacoes_de_acrescimo.iterrows():
            id_ecomplus_do_registro = registro['id_ecomplus']
            registro_formatado = registro.drop(
                ['id_ecomplus'], axis=0
            )
            registro_formatado['valid_thru'] = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
            print(f'O id do registro atual é {id_ecomplus_do_registro}'
                  f', e o registro formatado é: \n{registro_formatado}')

            ecomplus.adicionar_pontos_em_id(id_ecomplus_do_registro, registro_formatado)

    transacoes_de_acrescimo = transacoes_de_acrescimo.drop(['id_transacao'], axis=1)

    return transacoes_de_acrescimo


if __name__ == '__main__':
    dados_clientes = extratores.google_planilhas.ler_planilha(
        service_file_path=CHAVE_DE_SERVICO_SHEETS,
        spreadsheet_id=ID_PLANILHA_DIM_CLIENTE,
        sheet_name=NOME_ABA_DIM_CLIENTE
    )
    dados_transacoes = extratores.google_planilhas.ler_planilha(
        service_file_path=CHAVE_DE_SERVICO_SHEETS,
        spreadsheet_id=ID_PLANILHA_REGISTROS_TRANSACOES,
        sheet_name=NOME_ABA_REGISTROS_TRANSACOES
    )
    '''for i, cliente in dados.iterrows():
        print(f'\nPara o índice {i}:')
        print(refinamento_de_cliente(cliente))
        #print(cliente)'''

    '''res = cruzamento_de_cpf_e_id(formatar_cpf('047.591.935-10'), agrupamento_de_clientes(dados_clientes))
    print(res)'''

    res = registros_de_acrescimo(acrescentar_id_ecomplus_na_transacao(dados_clientes, dados_transacoes))
    lista = lista_de_ids_de_transacoes_positivas_a_enviar(res)
    #print(lista)
    #print(lista.keys())