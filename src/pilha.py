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
            return transicoes

def simulacao(estadoI, entrada, finais, transicoes):
    pilha = ["Z"]

    configuracoes = []

    configuracoes.append((estadoI, 0, []))

    while configuracoes:
        estadoAt, pos, pilha = configuracoes.pop()

        if pos == len(entrada) and estadoAt in finais:
            return True


arquivoEntrada = input()

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
        ultimaLinha = n
    else: break

ultimaLinha = ultimaLinha + 1
transicoes = criaDicionario(listaTransicoes)

print(len(vetLinhas), ultimaLinha)

aceita = False

#leitura das entradas de teste
for i in range(ultimaLinha, len(vetLinhas)):
    entradaAtual = vetLinhas[i]

    #testar para cada estado inicial
    for j in range(0, len(iniciais)):
        estadoInicial = iniciais[j]

        print(entradaAtual)
        print(estadoInicial)

        #logica do automato





    if aceita == False:
        print("X")
    else:
        print("OK")
    