from engenharia.etl import extratores, transformadores




df = transformadores.estoque_json.listar_produtos(
    extratores.bling.todos_os_produtos()
)


write_to_gsheet(caminho_credenciais, chave_tabela, nome_da_tabela, df)


