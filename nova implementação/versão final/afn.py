class AFN:

    def __init__(self, transicoes, estadosIniciais,
                 estadosFinais, alfabeto):

        self.transicoes = transicoes
        self.estadosIniciais = estadosIniciais
        self.estadosFinais = estadosFinais
        self.alfabeto = alfabeto


    def criaDicionario(self, listaTransicoes):

        transicoes = {}

        for linha in listaTransicoes:

            linha = linha.strip()

            if linha == "":
                continue

            esquerda, direita = linha.split("|")

            origem, seta, destino = esquerda.strip().split()

            simbolos = direita.strip().split()

            for simbolo in simbolos:

                chave = (origem, simbolo)

                if chave not in transicoes:
                    transicoes[chave] = set()

                transicoes[chave].add(destino)

        return transicoes

    def fechoLambda(self, estados):
        pilha = list(estados)
        fecho = set(estados)

        while pilha:
            estado = pilha.pop()
            consulta = (estado, "\\")
            if consulta in self.transicoes:
                for destino in self.transicoes[consulta]:
                    if destino not in fecho:
                        fecho.add(destino)
                        pilha.append(destino)

        return fecho

    def simulacao(self, estadoInicial, entrada):

        estadosAtuais = self.fechoLambda({estadoInicial})

        for simbolo in entrada:

            proximosEstados = set()

            for estado in estadosAtuais:

                consulta = (estado, simbolo)

                if consulta in self.transicoes:

                    proximosEstados.update(
                        self.transicoes[consulta]
                    )

            estadosAtuais = self.fechoLambda(proximosEstados)

            if len(estadosAtuais) == 0:
                return False


        for estado in estadosAtuais:

            if estado in self.estadosFinais:
                return True

        return False


    def verificaAlfabeto(self, entrada):

        for simbolo in entrada:

            if simbolo not in self.alfabeto:
                return False

        return True



def leituraAFN(vetLinhas):

    estados = []
    alfabeto = []
    iniciais = []
    finais = []
    listaTransicoes = []

    estados = vetLinhas[0].split()
    estados.remove("Q:")

    linhaAlfabeto = vetLinhas[1].replace("S:", "", 1).strip()
    if " " in linhaAlfabeto:
        alfabeto = linhaAlfabeto.split()
    else:
        alfabeto = list(linhaAlfabeto)

    iniciais = vetLinhas[2].split()
    iniciais.remove("I:")

    finais = vetLinhas[3].split()
    finais.remove("F:")

    ultimaLinha = 4

    for n in range(4, len(vetLinhas)):

        linha = vetLinhas[n].strip()

        if linha == "":
            ultimaLinha = n + 1
            continue

        if linha != "---":
            listaTransicoes.append(vetLinhas[n])
            ultimaLinha = n + 1
        else:
            ultimaLinha = n + 1
            break



    automato = AFN(
        None,
        iniciais,
        finais,
        alfabeto
    )


    transicoes = automato.criaDicionario(
        listaTransicoes
    )

    automato.transicoes = transicoes


    for i in range(ultimaLinha, len(vetLinhas)):
        
        entradaAtual = vetLinhas[i].strip()
         
        aceita = False


        if automato.verificaAlfabeto(
            entradaAtual
        ) == False:

            print("X")
            continue


        for estadoInicial in automato.estadosIniciais:

            if automato.simulacao(
                estadoInicial,
                entradaAtual
            ):

                aceita = True
                break


        if aceita:
            print("OK")

        else:
            print("X")