import pandas as pd

from tipos import Linhas


def transformar_campos(tabela_de_entrada: pd.DataFrame) -> pd.DataFrame:
    dataframe_de_saída = []
    for i, linha in tabela_de_entrada.iterrows():
        if pd.isnull(linha["Situação"]):
            dataframe_de_saída.append(
                {"Processada?": "Não",
                 "Registro no histórico da ContaSimples": linha["Histórico"],
                 "Data da Transação": (data_da_transação := linha["Data"].date()).strftime("%d/%m/%Y"),
                 "Mês de Competência": (data_da_transação).strftime("01/%m/%Y"),
                 "Valor": (str(linha["Crédito R$"]).replace(".", ",")
                           if not pd.isnull(linha["Crédito R$"])
                           else "-" + str(linha["Débito R$"]).replace(".", ",")),
                 "Saldo após transação": linha["Saldo R$"],
                 "Unidade de Entrega": linha["Nome do Cartão"],
                 "Centro de Custo": "",
                 "Categoria": "",
                 "Sub-categoria": "",
                 "Descrição": "",
                 "Entra no CAC?": "",
                 "Composição no Lucro Líquido": "",
                 "Composição no EBITDA": "",
                 "Composição no OPEX ou LB": ""}
            )
    return pd.DataFrame(dataframe_de_saída)


def pré_processar(dataframe_transformado: pd.DataFrame) -> pd.DataFrame:
    dataframe_de_saída = []
    for i, linha in dataframe_transformado.iterrows():
        histórico = linha["Registro no histórico da ContaSimples"]
        if "Rentabilidade 100% CDI" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "FP&A"
            linha["Centro de Custo"] = "Receita"
            linha["Categoria"] = "Rendimentos"
            linha["Sub-categoria"] = "Rendimentos da ContaSimples"
            linha["Descrição"] = f"Rentabilidade do dia {linha['Data da Transação']}"
        elif "655 Recebiveis-Cta Pre-paga" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Houzes"
            linha["Centro de Custo"] = "Receita"
            linha["Categoria"] = "Máquina Stone"
            linha["Sub-categoria"] = "Vendas no cartão"
            linha["Descrição"] = f"Venda do dia {linha['Data da Transação']}"
        elif "GOOGLE ADS" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Agência Bázico"
            linha["Centro de Custo"] = "Marketing"
            linha["Categoria"] = "Anúncios e campanhas"
            linha["Sub-categoria"] = "Anúncios Online"
            linha["Descrição"] = f"Google Ads"
            linha["Entra no CAC?"] = "Sim"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Variáveis (DV)"
        elif "Recarga TED/DOC de PAGAR.ME PAGAMENTOS S.A." in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Ecommerce"
            linha["Centro de Custo"] = "Receita"
            linha["Categoria"] = "Pagarme"
            linha["Sub-categoria"] = "Vendas no cartão"
            linha["Descrição"] = f"Venda do dia {linha['Data da Transação']}"
        elif "HOSTGATOR" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Ecommerce"
            linha["Centro de Custo"] = "Estrutura virtual"
            linha["Categoria"] = "Manutenção do Site"
            linha["Sub-categoria"] = "Hospedagem"
            linha["Descrição"] = f"Mensalidade Hostgator"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "MANYCHAT.COM" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Agência Bázico"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Geração de Leads"
            linha["Sub-categoria"] = "Ferramentas de automação"
            linha["Descrição"] = f"Mensalidade Manychat"
            linha["Entra no CAC?"] = "Sim"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "Recebimento via PIX de" in histórico:
            linha["Processada?"] = "Sim"
            linha["Centro de Custo"] = "Receita"
            linha["Categoria"] = "Recebimento via Pix"
            linha["Sub-categoria"] = "Vendas via Pix"
            linha["Descrição"] = f"Venda para cliente {histórico[23:]}"
        elif "AGAMENON ALMEIDA FILHO" in histórico:
            linha["Processada?"] = "Não"
            linha["Unidade de Entrega"] = "Agência Bázico"
            linha["Centro de Custo"] = "Terceiros"
            linha["Categoria"] = "Marketing de influência"
            linha["Sub-categoria"] = "Influenciadores"
            linha["Descrição"] = f"Agamenon"
            linha["Entra no CAC?"] = "Sim"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Variáveis (DV)"
        elif "DESO/SE" in histórico:
            linha["Processada?"] = "Não"
            linha["Centro de Custo"] = "Estrutura física"
            linha["Categoria"] = "Contas"
            linha["Sub-categoria"] = "Conta de água"
            linha["Descrição"] = f"Conta da DESO"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "LOJA INTEGRADA" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Ecommerce"
            linha["Centro de Custo"] = "Estrutura Virtual"
            linha["Categoria"] = "Manutenção do Site"
            linha["Sub-categoria"] = "Plataforma de Ecommerce"
            linha["Descrição"] = f"Loja Integrada"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "CLARO" in histórico:
            linha["Processada?"] = "Não"
            linha["Centro de Custo"] = "Estrutura física"
            linha["Categoria"] = "Contas"
            linha["Sub-categoria"] = "Conta de internet"
            linha["Descrição"] = f"Conta da Claro"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "ALEXANDRE SANTOS" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Bázico Logística"
            linha["Centro de Custo"] = "Logística"
            linha["Categoria"] = "Custos de entrega"
            linha["Sub-categoria"] = "Expedição"
            linha["Descrição"] = f"Motoboy em Aracaju"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Variáveis (DV)"
        elif "FACEBOOK" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Agência Bázico"
            linha["Centro de Custo"] = "Marketing"
            linha["Categoria"] = "Anúncios e campanhas"
            linha["Sub-categoria"] = "Anúncios Online"
            linha["Descrição"] = f"Meta Ads"
            linha["Entra no CAC?"] = "Sim"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Variáveis (DV)"
        elif "ANTONIO VICTOR CARVALHO OLIVEIRA GOMES" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1000:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Agência Bázico"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "BRUNA RAFAELA MATOS DA SILVA" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1000:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Gente & Gestão"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "KARLA LETÍCIA OLIVEIRA ANDRADE" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 500:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Agência Bázico"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Bolsa estágio"
                linha["Descrição"] = f"Bolsa estágio de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "ROBERT AMAZONAS DE SOUZA FILHO" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1200:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Bázico Logística"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "JULIO VINICIUS SOUSA OLIVEIRA" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1500:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Data Experts"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "SARAH DE FREITAS MONTEIRO GRABHER" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1000:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Relacionamento com o Cliente"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "VICTOR ADIR AMORIM MACHADO" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1200:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Houzes"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "CLEVERTON OLIVEIRA SOBRINHO" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1500:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Relacionamento com o Cliente"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "ALEX MARLEY BRANDÃO SALES" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 1500:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Houzes"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Salário"
                linha["Descrição"] = f"Salário de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "GURU-APRENDIZ" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Relacionamento com o Cliente"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Clube de Assinatura"
            linha["Sub-categoria"] = "Gestão de recorrência"
            linha["Descrição"] = f"Guru Aprendiz"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "MLABS" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Agência Bázico"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Ferramenta de Dados"
            linha["Sub-categoria"] = "Redes sociais"
            linha["Descrição"] = f"MLabs"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "RAFAELA DA SILVA SANTOS" in histórico:
            linha["Processada?"] = "Não"
            linha["Centro de Custo"] = "Estrutura física"
            linha["Categoria"] = "Contas"
            linha["Sub-categoria"] = "Limpeza"
            linha["Descrição"] = f"Faxina feita por {histórico[17:]}"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "KISKADI MARKETING DIGITAL" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Relacionamento com o Cliente"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Gestão de Relacionamento com o Cliente"
            linha["Sub-categoria"] = "Ferramenta de CRM"
            linha["Descrição"] = f"Kiskadi"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "ALEXANDRE TEIXEIRA  CORRETOR DE IMOVEIS" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Gente & Gestão"
            linha["Centro de Custo"] = "Estrutura física"
            linha["Categoria"] = "Contas"
            linha["Sub-categoria"] = "Aluguel"
            linha["Descrição"] = f"Aluguel do QG Urquiza Leal"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "IUGU INSTITUICAO DE PAGAMENTO S.A" in histórico and linha["Valor"] == "-600":
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Diretoria"
            linha["Centro de Custo"] = "Terceiros"
            linha["Categoria"] = "Assessoria Jurídica"
            linha["Sub-categoria"] = "Plataforma de assessoria"
            linha["Descrição"] = f"Bonuz"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "MATHEUS ARICAWA SILVA MELO" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 2000:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Diretoria"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Pró-labore"
                linha["Descrição"] = f"Pró-labore de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "RAFAEL ISSA MARTINS" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 2000:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Diretoria"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Pró-labore"
                linha["Descrição"] = f"Pró-labore de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "GUSTAVO ALEXANDRE SOUZA MELLO" in histórico:
            if -float(linha["Valor"].replace(",", ".")) >= 2000:
                linha["Processada?"] = "Não"
                linha["Unidade de Entrega"] = "Diretoria"
                linha["Centro de Custo"] = "Pessoas"
                linha["Categoria"] = "Folha de pagamento"
                linha["Sub-categoria"] = "Pró-labore"
                linha["Descrição"] = f"Pró-labore de {histórico[17:]}"
                linha["Entra no CAC?"] = "Não"
                linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
                linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
                linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "ORGANISYS SOFTWARE LTDA" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Bázico Logística"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Gestão de Estoque"
            linha["Sub-categoria"] = "Sistema de Gestão de Recursos Empresariais (ERP)"
            linha["Descrição"] = f"Bling"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "IUGU*ASSINATURARE" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Relacionamento com o Cliente"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Gestão de Relacionamento com o Cliente"
            linha["Sub-categoria"] = "Ferramenta de Gestão de Giftback"
            linha["Descrição"] = f"Fidelizar"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "NOTION LABS" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Gente & Gestão"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Virtual Office"
            linha["Sub-categoria"] = "Gestão do Conhecimento"
            linha["Descrição"] = f"Notion"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "EMPREENDER - SAO PAULO/BR" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Relacionamento com o Cliente"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Gestçao do Relacionamento com o Cliente"
            linha["Sub-categoria"] = "Automação de mensagens"
            linha["Descrição"] = f"SAK"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "MINISTERIO DA ECONOMIA" in histórico:
            mês_ano = linha["Mês de Competência"]
            mês = mês_ano[3:5]
            ano = mês_ano[6:]

            linha["Processada?"] = "Sim"
            linha["Mês de Competência"] = f"{(mês_ano[:3] + str(int(mês) - 1) + mês_ano[5:] if mês != '01' else '01/12/' + str(int(ano) - 1))}"
            linha["Unidade de Entrega"] = "Diretoria"
            linha["Centro de Custo"] = "Impostos"
            linha["Categoria"] = "Impostos sobre Faturamento (I)"
            linha["Sub-categoria"] = "Simples Nacional"
            linha["Descrição"] = f"Pagamento de DAS"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Lucro Bruto (LB)"
            linha["Composição no OPEX ou LB"] = "Faturamento Líquido (FL)"
        elif "BENCHMARKEMAILCOM" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Agência Bázico"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Anúncios e campanhas"
            linha["Sub-categoria"] = "Email marketing"
            linha["Descrição"] = f"Benchmarking email"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "PG *ENVIOU" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Relacionamento com o Cliente"
            linha["Centro de Custo"] = "Ferramentas"
            linha["Categoria"] = "Gestão de Relacionamento com o Cliente"
            linha["Sub-categoria"] = "Recuperação de carrinhos abandonados"
            linha["Descrição"] = f"Enviou"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "RAFAELA DE CASSIA LEITE SANTOS" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "Houzes"
            linha["Centro de Custo"] = "Estrutura física"
            linha["Categoria"] = "Contas"
            linha["Sub-categoria"] = "Aluguel"
            linha["Descrição"] = f"Aluguel da Houze Aracaju"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "ENERGISA SERGIPE" in histórico:
            linha["Processada?"] = "Não"
            linha["Centro de Custo"] = "Estrutura física"
            linha["Categoria"] = "Contas"
            linha["Sub-categoria"] = "Conta de energia"
            linha["Descrição"] = f"Conta da Energisa"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"
        elif "FEITOS ASSESSORIA CONTABIL FISCAL" in histórico:
            linha["Processada?"] = "Sim"
            linha["Unidade de Entrega"] = "FP&A"
            linha["Centro de Custo"] = "Terceiros"
            linha["Categoria"] = "Conformidade Fiscal e Contábil"
            linha["Sub-categoria"] = "Assessoria Contábil"
            linha["Descrição"] = f"Feitos Assessoria Contábil"
            linha["Entra no CAC?"] = "Não"
            linha["Composição no Lucro Líquido"] = "Resultado Operacional (EBITDA)"
            linha["Composição no EBITDA"] = "Despesas Operacionais (OPEX)"
            linha["Composição no OPEX ou LB"] = "Despesas Fixas (DF)"

        dataframe_de_saída.append(linha.to_dict())

    return pd.DataFrame(dataframe_de_saída)

def transformar_dataframe_em_linhas(dataframe: pd.DataFrame) -> Linhas:
    return [[None
             if pd.isnull(valor)
             else (str(valor).replace(".", ",")
                   if not isinstance(valor, str)
                   else valor) for valor in linha]
            for linha in dataframe.values.tolist()]


def transformar_e_pré_processar(tabela_de_entrada: pd.DataFrame) -> Linhas:
    return transformar_dataframe_em_linhas(pré_processar(transformar_campos(tabela_de_entrada)))