class MaquinaDeTuring:

    def __init__(self, transicoes, estadoInicial,
                 estadosFinais, alfabeto):

        self.transicoes = transicoes
        self.estadoInicial = estadoInicial
        self.estadosFinais = estadosFinais
        self.alfabeto = alfabeto
        
    def criaDicionario(self, listaTransicoes):
        transicoes = {}

        for linha in listaTransicoes:
            esquerda, direita = linha.split("|")
            origem, seta, destino = esquerda.strip().split()
            regras = direita.strip().split()

            for regra in regras:
                simboloLido, acao = regra.split("/")
                simboloEscrever = acao[0]
                direcao = acao[1]

                transicoes[(origem, simboloLido)] = (destino, simboloEscrever, direcao)

        return transicoes


    def passo(self, fita, cabecote, estadoAtual):
        simboloAtual = fita[cabecote]

        consulta = (estadoAtual, simboloAtual)

        if consulta not in self.transicoes:
            return fita, cabecote, estadoAtual, False

        novoEstado, simboloEscrever, direcao = self.transicoes[consulta]

        fita[cabecote] = simboloEscrever
        estadoAtual = novoEstado

        if direcao == "D":
            cabecote = cabecote + 1
        if direcao == "E":
            cabecote = cabecote - 1

        return fita, cabecote, estadoAtual, True


    def simulacao(self, entrada):

        fita = list("<" + entrada + "_" * 50)

        cabecote = 1
        estadosAtuais = self.estadoInicial

        limitePassos = 1000
        passos = 0

        while passos < limitePassos:
            passos = passos + 1
        
            if estadosAtuais in self.estadosFinais:
                return True, fita

            fita,cabecote,estadosAtuais, conseguiu = self.passo(
                fita,
                cabecote,
                estadosAtuais
            )

            if conseguiu == False:
                return False, fita
 
        return False, fita
    
    def simulacaoALL(self, entrada):

        fita = list("<" + entrada + ">")

        cabecote = 1
        estadosAtuais = self.estadoInicial

        limitePassos = 1000
        passos = 0

        while passos < limitePassos:
            passos = passos + 1

            if estadosAtuais in self.estadosFinais:
                return True, fita

            fita, cabecote, estadosAtuais, conseguiu = self.passo(
                fita,
                cabecote,
                estadosAtuais
            )

            if conseguiu == False:
                return False, fita

            if cabecote < 0 or cabecote >= len(fita):
                return False, fita

        return False, fita
        
    def formatarFita(self, fita):
        texto = "".join(fita)

        while texto.endswith("_"):
            texto = texto[:-1]

        return texto

    
def leituraALL(vetLinhas):

    estados = vetLinhas[0].split()
    estados.remove("Q:")

    alfabeto = vetLinhas[1].replace("G:", "", 1).strip()

    linhaInicial = vetLinhas[2].split()
    linhaInicial.remove("I:")
    estadoInicial = linhaInicial[0]

    finais = vetLinhas[3].split()
    finais.remove("F:")

    listaTransicoes = []
    ultimaLinha = 4

    for n in range(4, len(vetLinhas)):
        linha = vetLinhas[n].strip()

        if linha == "---":
            ultimaLinha = n + 1
            break

        if linha != "":
            listaTransicoes.append(vetLinhas[n])

    maquina = MaquinaDeTuring(None, estadoInicial, finais, alfabeto)

    transicoes = maquina.criaDicionario(listaTransicoes)
    maquina.transicoes = transicoes

    for i in range(ultimaLinha, len(vetLinhas)):
        entradaAtual = vetLinhas[i].strip()

        aceita, fitaFinal = maquina.simulacaoALL(entradaAtual)

        if aceita:
            print("OK", maquina.formatarFita(fitaFinal))
        else:
            print("X", maquina.formatarFita(fitaFinal))
    
def leituraMT(vetLinhas):

    estados = vetLinhas[0].split()
    estados.remove("Q:")

    alfabeto = vetLinhas[1].replace("G:", "", 1).strip()

    linhaInicial = vetLinhas[2].split()
    linhaInicial.remove("I:")
    estadoInicial = linhaInicial[0]

    finais = vetLinhas[3].split()
    finais.remove("F:")

    listaTransicoes = []
    ultimaLinha = 4

    for n in range(4, len(vetLinhas)):
        linha = vetLinhas[n].strip()

        if linha == "---":
            ultimaLinha = n + 1
            break

        if linha != "":
            listaTransicoes.append(vetLinhas[n])

    maquina = MaquinaDeTuring(None, estadoInicial, finais, alfabeto)

    transicoes = maquina.criaDicionario(listaTransicoes)
    maquina.transicoes = transicoes

    for i in range(ultimaLinha, len(vetLinhas)):
        entradaAtual = vetLinhas[i].strip()

        aceita, fitaFinal = maquina.simulacao(entradaAtual)

        if aceita:
            print("OK", maquina.formatarFita(fitaFinal))
        else:
            print("X", maquina.formatarFita(fitaFinal))