from AutomatoDePilha import AutomatoDePilha

def main():
    leitura()

def leitura():
    arquivoEntrada = input()

    with open('./testes/' + arquivoEntrada, 'r', encoding='utf-8') as arquivo:

        entrada = arquivo.read()

    vetLinhas = entrada.split('\n')

    estados = vetLinhas[0].split(' ')
    estados.remove("Q:")
            
    #alfabeto de cria
    #alfabeto = {'0', '1'}
    alfabeto = vetLinhas[1].split(' ')
    alfabeto = alfabeto[1]
    
    print(alfabeto)

    iniciais = vetLinhas[3].split(' ')
    iniciais.remove("I:")

    listaTransicoes = []

    for n in range(4, len(vetLinhas)):
        if vetLinhas[n] != "---":
            listaTransicoes.append(vetLinhas[n])
            ultimaLinha = n
        else: 
            break

    ultimaLinha = ultimaLinha + 2

    transicoes = AutomatoDePilha.criaDicionario(listaTransicoes)

    automato = AutomatoDePilha(transicoes, iniciais, alfabeto)

    #leitura das entradas de teste
    for i in range(ultimaLinha, len(vetLinhas)):
        aceita = False
        entradaAtual = vetLinhas[i]
        print(entradaAtual)

        if automato.verificaAlfabeto(entradaAtual) == False:
            print("X")
            continue

        #testar para cada estado inicial
        for j in range(0, len(iniciais)):
            estadoInicial = automato.estadosIniciais[j]

            if automato.simulacao(estadoInicial, entradaAtual) == True:
                aceita = True
                break
        
        if aceita:
            print("OK")

        else:
            print("X")

if __name__ == "__main__":
    main()
