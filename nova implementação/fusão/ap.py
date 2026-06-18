from collections import deque

LAMBDA = "λ"

class AutomatoDePilha:
    def __init__(self, transicoes, estadosIniciais, alfabeto):
        self.transicoes = transicoes
        self.estadosIniciais = estadosIniciais
        self.alfabeto = alfabeto
        self.tLambda = False

    def criaDicionario(self, listaTransicoes):

        transicoes = {}
        
        for linha in listaTransicoes:
            linha = linha.replace(" -> ", " ")

            separacao = linha.split(' ')

            for i in range(0, len(separacao)):
                if "\\" in separacao[i]:
                    separacao[i] = separacao[i].replace("\\", LAMBDA)

            for p in range(3, len(separacao)):
                estadoAtual = separacao[0]
                estadoProx = separacao[1]

                transicaoAtual = separacao[p]

                partes = transicaoAtual.split(",")

                entrada = partes[0]

                if entrada == LAMBDA:
                    self.tLambda = True

                infoPilha = partes[1].split("/")
                
                desempilha = infoPilha[0]
                empilha = infoPilha[1]

                transicoes[(estadoAtual, entrada, desempilha)] = (estadoProx, empilha)
            
        return transicoes

    #função inicial que precisou ser alterada para aceitar transicoes lambda; 
    #favor não apagar para poder documentar
    """
    def simulacao(self, estadoI, entrada):
        pilha = ["Z"]

        estadoAt = estadoI

        for i in range(0, len(entrada)):
            if(pilha == []):
                return False
            
            #print("pilha no incicio", pilha)
            simbolo = entrada[i]

            topo = pilha[-1]

            consulta1 = (estadoAt, simbolo, topo)
            consulta2 = (estadoAt, simbolo, LAMBDA)

            if(consulta1 in self.transicoes):
                novoEstado, empilha = self.transicoes[consulta1]
                estadoAt = novoEstado
                pilha.pop()

                if(empilha != LAMBDA):
                    for j in reversed(empilha):
                        pilha.append(j)

            elif(consulta2 in self.transicoes):
                novoEstado, empilha = self.transicoes[consulta2]
                estadoAt = novoEstado
                if(empilha != LAMBDA):
                    for j in reversed(empilha):
                        pilha.append(j)

            print("pilha no final", pilha)

        if len(pilha) == 0 or pilha == ["Z"]:
            return True
        else:
            return False
    """

    def simulacao(self, estadoI, entrada):
        #cnfiguração: (estado, i da entrada, pilha)
        iniciais = {(estadoI, 0, ("Z",))}
        
        def expandeLambda(configs):
            visitados = set(configs)
            fila = deque(configs)

            while fila:

                estado, idx, pilha = fila.popleft()
                if not pilha:
                    continue
                topo = pilha[-1]

                #transicao vazia
                for consulta in [(estado, LAMBDA, topo), (estado, LAMBDA, LAMBDA)]:

                    if consulta in self.transicoes:
                        novoEstado, empilha = self.transicoes[consulta]
                        novaPilha = list(pilha)

                        if consulta[2] != LAMBDA:
                            novaPilha.pop()
                        if empilha != LAMBDA:
                            for s in reversed(empilha):
                                novaPilha.append(s)

                        nova = (novoEstado, idx, tuple(novaPilha))
                        if nova not in visitados:
                            visitados.add(nova)
                            fila.append(nova)

            return visitados

        configs = expandeLambda(iniciais)

        for i, simbolo in enumerate(entrada):
            proximas = set()

            for estado, idx, pilha in configs:
                if not pilha:
                    continue
                topo = pilha[-1]

                for consulta in [(estado, simbolo, topo), (estado, simbolo, LAMBDA)]:
                    if consulta in self.transicoes:
                        novoEstado, empilha = self.transicoes[consulta]
                        novaPilha = list(pilha)

                        #desempilha se nao for lambda
                        if consulta[2] != LAMBDA:
                            novaPilha.pop()
                        if empilha != LAMBDA:
                            for s in reversed(empilha):
                                novaPilha.append(s)
                        proximas.add((novoEstado, i + 1, tuple(novaPilha)))
            
            configs = expandeLambda(proximas)
            if not configs:
                return False

        #aceita se alguma configuracao tem pilha só com Z
        return any(
            pilha == ("Z",)
            for estado, idx, pilha in configs
        )

    def verificaAlfabeto(self, entrada):
        alfabeto = self.alfabeto

        for i in entrada:
            if i not in alfabeto:
                return False
            
        return True
    
    def leituraPilha(vetLinhas):          
        estados = []
        alfabeto = []
        #alfabetoPilha = []
        iniciais = []
        #finais = []
        listaTransicoes = []
        #palavrasTeste = []

        estados = vetLinhas[0].split(' ')
        estados.remove("Q:")

        alfabeto = vetLinhas[1].split(' ')
        alfabeto = alfabeto[1]
        
        #print(alfabeto)

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

        automato = AutomatoDePilha(None, iniciais, alfabeto)

        transicoes = automato.criaDicionario(listaTransicoes)
        automato.transicoes = transicoes

        #leitura das entradas de teste
        for i in range(ultimaLinha, len(vetLinhas)):
            aceita = False

            entradaAtual = vetLinhas[i]
            #print(entradaAtual)

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