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
                    
                    print(separacao)

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
        
        #
        def expandeLambda(configs):
            visitados = set(configs)
            fila = deque(configs)
            while fila:
                estado, idx, pilha = fila.popleft()
                if not pilha:
                    continue
                topo = pilha[-1]
                print(pilha)

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