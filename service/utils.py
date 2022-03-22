from itertools import cycle

LENGTH_CNPJ = 14

def cnpj_is_valid(cnpj: str) -> bool:

    # fonte: https://programandoautomacao.blogspot.com/2020/10/python-uma-funcao-pythonica-para_15.html

    '''
        Verifica se o cnpj recebido é valido, devolvendo uma string que pode ser diretamente
        inserida no banco de dados POSTGRES
    '''

    numeros_cnpj = [int(char) for char in cnpj if char.isdigit()]

    if len(numeros_cnpj) != LENGTH_CNPJ:
        return "false"

    if numeros_cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return "false"

    cnpj_r = numeros_cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return "false"

    return "true"

def cpf_is_valid(numbers):
    # fonte: https://www.vivaolinux.com.br/script/Validador-e-gerador-de-CPF-em-Python#:~:text=Duas%20fun%C3%A7%C3%B5es%20em%20Python%2C%20uma,que%20gera%20um%20CPF%20v%C3%A1lido.&text=from%20random%20import%20randint%20def,d%C3%ADgitos%20if%20len(cpf)%20!%3D

    '''
        Verifica se o cnpj recebido é valido, devolvendo uma string que pode ser diretamente
        inserida no banco de dados POSTGRES
    '''

    #  Obtém os números do CPF e ignora outros caracteres
    numeros_cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(numeros_cpf) != 11:
        return "false"

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if numeros_cpf == numeros_cpf[::-1]:
        return "false"

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((numeros_cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != numeros_cpf[i]:
            return "false"
    return "true"