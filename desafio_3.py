#criar função para pedir numero inteiro ao usuario o numero deve ser maior que 0 e so aceitar numeros inteiros
def pede_num_inteiro(mensagem):
    while True:
        try:
            num = int(input(mensagem))
            if num <= 0:
                print("O numero deve ser maior que 0")
            else:
                return num
        except ValueError:
            print('Valor inválido. Tente novamente.')
            
# criar função para verificar se o numero e perfeito
def verifica_perfeito(num):
    #Para resolver esse problema, você pode começar criando uma função que receba um número inteiro positivo como entrada e retorne todos os seus divisores. Em seguida, basta iterar pelos divisores e calcular a soma deles. Se a soma for igual ao número original, o número é perfeito.
    #criar lista para armazenar os divisores
    divisores = []
    #iterar pelos numeros de 1 ate o numero
    for i in range(1, num):
        #verificar se o numero e divisivel pelo numero
        if num % i == 0:
            #adicionar o numero a lista de divisores
            divisores.append(i)
    #somar os divisores
    soma = sum(divisores)
    #verificar se a soma dos divisores é igual ao numero
    if soma == num:
        return True
    else:
        return False

def main():
    #pedir que o usuario digite um numero inteiro
    num = pede_num_inteiro("Digite um numero inteiro: ")
    #verificar se o numero e perfeito
    if verifica_perfeito(num):
        print("O numero {} é perfeito".format(num))
    else:
        print("O numero {} não é perfeito".format(num))
        
if __name__ == "__main__":
    main()