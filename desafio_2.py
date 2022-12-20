def pede_num_inteiro(mensagem):
    while True:
        try:
            num = int(input(mensagem))
            return num
        except ValueError:
            print('Valor inválido. Tente novamente.')
            
# criar função para verificar se o numero e armstrong
def verifica_armstrong(num):
    #Para resolver esse problema, você pode começar dividindo o número em dígitos individualmente. Em seguida, você pode usar uma estrutura de repetição para iterar pelos dígitos e calcular o cubo de cada um deles. Por fim, basta verificar se a soma dos cubos dos dígitos é igual ao número original.
    #converter o numero em string
    num = str(num)
    #criar variavel para armazenar a soma dos cubos dos digitos
    soma = 0
    #iterar pelos digitos do numero
    for digito in num:
        #converter o digito para inteiro
        digito = int(digito)
        #calcular o cubo do digito
        cubo = digito ** 3
        #somar o cubo do digito
        soma += cubo
    #verificar se a soma dos cubos dos digitos é igual ao numero original
    if soma == int(num):
        return True
    else:
        return False
    
def main():
    #pedir que o usuario digite um numero inteiro
    num = pede_num_inteiro("Digite um numero inteiro: ")
    #verificar se o numero e armstrong
    if verifica_armstrong(num):
        print("O numero {} é armstrong".format(num))
    else:
        print("O numero {} não é armstrong".format(num))