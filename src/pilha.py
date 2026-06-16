def criaDicionario(listaTransicoes):

    transicoes = {}
    
    for linha in listaTransicoes:
        linha = linha.replace(" -> ", " ")

        separacao = linha.split(' ')

        for i in range(0, len(separacao)):
            if "\\" in separacao[i]:
                separacao[i] = separacao[i].replace("\\", " ")

        for p in range(3, len(separacao)):
            estadoAtual = separacao[0]
            estadoProx = separacao[1]

            transicaoAtual = separacao[p]

            partes = transicaoAtual.split(",")

            entrada = partes[0]

            infoPilha = partes[1].split("/")
            
            desempilha = infoPilha[0]
            empilha = infoPilha[1]

            transicoes[(estadoAtual, entrada, desempilha)] = (estadoProx, empilha)
        
    return transicoes

def simulacao(estadoI, entrada, transicoes):
    pilha = ["Z"]

    estadoAt = estadoI

    for i in range(0, len(entrada)):
        if(pilha == []):
            return False
        
        print("pilha no incicio", pilha)
        simbolo = entrada[i]
        topo = pilha[-1]

        consulta1 = (estadoAt, simbolo, topo)
        consulta2 = (estadoAt, simbolo, " ")

        if(consulta1 in transicoes):
            novoEstado, empilha = transicoes[consulta1]
            estadoAt = novoEstado
            pilha.pop()

            if(empilha != " "):
                for j in reversed(empilha):
                    pilha.append(j)

        elif(consulta2 in transicoes):
            novoEstado, empilha = transicoes[consulta2]
            estadoAt = novoEstado
            if(empilha != " "):
                for j in reversed(empilha):
                    pilha.append(j)

        print("pilha no final", pilha)

    if len(pilha) == 0 or pilha == ["Z"]:
        return True
    else:
        return False

    

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

listaTransicoes = []

for n in range(4, len(vetLinhas)):
    if vetLinhas[n] != "---":
        listaTransicoes.append(vetLinhas[n])
        ultimaLinha = n
    else: 
        break

ultimaLinha = ultimaLinha + 2
transicoes = criaDicionario(listaTransicoes)

#leitura das entradas de teste
for i in range(ultimaLinha, len(vetLinhas)):
    aceita = False
    entradaAtual = vetLinhas[i]

    #testar para cada estado inicial
    for j in range(0, len(iniciais)):
        estadoInicial = iniciais[j]

        print(entradaAtual)

        if simulacao(estadoInicial, entradaAtual, transicoes) == True:
            aceita = True
            break
    
    if aceita:
        print("OK")

    else:
        print("X")