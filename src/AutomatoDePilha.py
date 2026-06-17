class AutomatoDePilha:
    def __init__(self, transicoes, estadosIniciais, alfabeto):
        self.transicoes = transicoes
        self.estadosIniciais = estadosIniciais
        self.alfabeto = alfabeto

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

    def simulacao(self, estadoI, entrada):
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

            if(consulta1 in self.transicoes):
                novoEstado, empilha = self.transicoes[consulta1]
                estadoAt = novoEstado
                pilha.pop()

                if(empilha != " "):
                    for j in reversed(empilha):
                        pilha.append(j)

            elif(consulta2 in self.transicoes):
                novoEstado, empilha = self.transicoes[consulta2]
                estadoAt = novoEstado
                if(empilha != " "):
                    for j in reversed(empilha):
                        pilha.append(j)

            print("pilha no final", pilha)

        if len(pilha) == 0 or pilha == ["Z"]:
            return True
        else:
            return False
        

    def verificaAlfabeto(self, entrada):
        alfabeto = self.alfabeto

        for i in entrada:
            if i not in alfabeto:
                return False
            
        return True