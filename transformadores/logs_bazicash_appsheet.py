import re

import extratores
from tipos import Registro, Union, Tabela, Linhas


def formatar_cpf(cpf_original: str):
    cpf_desagrupado = re.findall('\d+', str(cpf_original))
    cpf = "".join([str(parte_do_cpf) for parte_do_cpf in cpf_desagrupado])
    return cpf


def refinamento_de_transacao(registro: Registro) -> Union[Tabela, Linhas]:


if __name__ == '__main__':
    cpf_ex = "074.223.914-48"
    cpf = formatar_cpf(cpf_ex)
    print(cpf)