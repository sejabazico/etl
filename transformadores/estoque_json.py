from datetime import datetime
import pandas as pd

from tipos import Produto, List, Tabela, Linhas

ID_DEPÓSITO_ECOMMERCE = '12267858145'
ID_DEPÓSITO_HOUZE = '14886481310'


def listar_produtos(produtos: List[Produto]) -> Tabela:
    dados_do_produto = [{
        'Código': produto['produto']['codigo'],
        'Descrição': str(produto['produto']['descricao']),
        'Situação': produto['produto']['situacao'],
        'Estoque E-commerce': int([deposito['deposito']['saldo'] for deposito in produto['produto']['depositos']
                    if deposito['deposito']['id'] == ID_DEPÓSITO_ECOMMERCE][0]),
        'Estoque Houze': int([deposito['deposito']['saldo'] for deposito in produto['produto']['depositos']
                               if deposito['deposito']['id'] == ID_DEPÓSITO_HOUZE][0]),
        'Estoque Total': int([deposito['deposito']['saldo'] for deposito in produto['produto']['depositos']
                    if deposito['deposito']['id'] == ID_DEPÓSITO_ECOMMERCE][0]) + int([deposito['deposito']['saldo'] for deposito in produto['produto']['depositos']
                               if deposito['deposito']['id'] == ID_DEPÓSITO_HOUZE][0]),
        'Fornecedor': produto['produto']['nomeFornecedor'],
        'Preço': (produto['produto']['preco']).replace('.',','),
        'NCM': produto['produto']['class_fiscal']
    } for produto in produtos]
    produtos_list = [list(linha.values()) for linha in dados_do_produto]
    produtos_df = pd.DataFrame(produtos_list, columns=dados_do_produto[0].keys())
    produtos_df['SKU'] = produtos_df.apply(
        lambda row: (("Sim" if len(row.Descrição.split('-')) >= 3 else "Não") if row.Código not in (
            '555', '1000') else "Não") if row.Código.isnumeric() is True else "Não", axis=1)
    produtos_df['Modelo'] = produtos_df.apply(lambda row: row.Descrição.split('-')[0].strip(), axis=1)
    produtos_df['Cor'] = produtos_df.apply(
        lambda row: None if len(row.Descrição.split('-')) == 1 else row.Descrição.split('-')[1].strip(), axis=1)
    produtos_df['Tecido'] = produtos_df.apply(
        lambda row: None if len(row.Descrição.split('-')) <= 2 else row.Descrição.split('-')[2].strip(), axis=1)
    produtos_df['Tamanho'] = produtos_df.apply(
        lambda row: None if len(row.Descrição.split('-')) <= 3 else row.Descrição.split('-')[3].strip(), axis=1)
    produtos_df['Grupo'] = produtos_df.apply(
        lambda row: None if len(row.Descrição.split('-')) <= 2 else (
                row.Descrição.split('-')[0].strip() + ' - ' +
                row.Descrição.split('-')[1].strip() + ' - ' +
                row.Descrição.split('-')[2].strip()), axis=1)


    return produtos_df


def listar_produto(produto: Produto) -> Linhas:
    data = datetime.today().strftime('%d/%m/%Y')
    dados_do_produto = {
        'Data': data,
        'Código': produto['retorno']['estoques'][0]['estoque']['codigo'],
        'Descrição': produto['retorno']['estoques'][0]['estoque']['nome'],
        'Estoque': [deposito['deposito']['saldo']
                                for deposito in produto['retorno']['estoques'][0]['estoque']['depositos']
                                if deposito['deposito']['id'] == ID_DEPÓSITO_ECOMMERCE][0]
    }

    return [list(dados_do_produto.values())]


if __name__ == '__main__':
    from engenharia.etl import extratores

    resultado = listar_produtos(extratores.bling.todos_os_produtos())
    print(resultado["SKU"])