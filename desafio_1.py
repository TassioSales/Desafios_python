#função para pedir que o usuário digite algo
def digite_algo():
    algo = input("Digite algo: ")
    #não aceitar valor vazio e nem espaço em branco
    while algo == "" or algo.isspace():
        algo = input("Digite algo: ")
    #nao aceitar que o tamanho seja menor que 2 caracteres
    while len(algo) < 2:
        algo = input("Digite algo: ")
    return algo

#criar função para retorna a palavra invertida
def inverte_palavra(palavra):
    #inverter a palavra
    palavra_invertida = palavra[::-1]
    return palavra_invertida

def main():
    #chamar a função para pedir que o usuário digite algo
    algo = digite_algo()
    #chamar a função para inverter a palavra
    palavra_invertida = inverte_palavra(algo)
    #imprimir a palavra invertida
    print(palavra_invertida)
    
    
if __name__ == "__main__":
    main()