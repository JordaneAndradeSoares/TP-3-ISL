def criaDicionario(listaTransicoes):

    transicoes = {}
    
    for linha in listaTransicoes:
        linha = linha.replace(" -> ", " ")

        separacao = linha.split(' ')

        for p in range(3, len(separacao)):
            estadoAtual = separacao[0]
            estadoProx = separacao[1]

            transicaoAtual = separacao[p]

            partes = transicaoAtual.split(",")

            print(partes)

            entrada = partes[0]

            infoPilha = partes[1].split("/")
            
            desempilha = infoPilha[0]
            empilha = infoPilha[1]

            #print(estadoAtual, estadoProx, entrada, desempilha, empilha)

            transicoes[(estadoAtual, entrada, desempilha)] = (estadoProx, empilha)

arquivoEntrada = input()

pilha = []
#usar append e 'x = pilha.pop'

with open('./testes/' + arquivoEntrada, 'r', encoding='utf-8') as arquivo:

    entrada = arquivo.read()

vetLinhas = entrada.split('\n')

estados = vetLinhas[0].split(' ')
estados.remove("Q:")
        
#alfabeto de cria

alfabeto = {'0', '1'}

iniciais = vetLinhas[2].split(' ')
iniciais.remove("I:")

finais = vetLinhas[3].split(' ')

listaTransicoes = []

for n in range(4, len(vetLinhas)):
    if vetLinhas[n] != "---":
        listaTransicoes.append(vetLinhas[n])

criaDicionario(listaTransicoes)



