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

    def simulacao(self, estadoI, entrada):
        # configuração: (estado, i da entrada, pilha)
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
    
def automato_de_pilha(linhas):          
    estados_ap = []
    alfabeto_entrada = []
    alfabeto_pilha = []
    iniciais = []
    finais = []
    listaTransicoes = []
    palavras_teste = []

    i = 0
    # 1. Lê os parâmetros do autômato (lida com ordem dinâmica e linhas extras)
    while i < len(linhas):
        linha = linhas[i].strip()
        
        # Pula linhas vazias
        if not linha:
            i += 1
            continue
            
        # Se achou uma transição ou o separador, sai da leitura de parâmetros
        if "->" in linha or linha == "---":
            break
            
        if linha.startswith("Q:"):
            estados_ap = linha.split()[1:]
        elif linha.startswith("S:"):
            # Pega tudo após "S:" e remove espaços para suportar "S: 01" ou "S: 0 1"
            alfabeto_entrada = list(linha[2:].strip().replace(" ", ""))
        elif linha.startswith("G:"):
            alfabeto_pilha = list(linha[2:].strip().replace(" ", ""))
        elif linha.startswith("I:"):
            iniciais = linha.split()[1:]
        elif linha.startswith("F:"):
            finais = linha.split()[1:]
        
        i += 1

    # 2. Lendo transições (agrupando transições que foram quebradas em várias linhas)
    transicao_atual = ""
    while i < len(linhas):
        linha = linhas[i].strip()
        
        if linha == "---":
            if transicao_atual:
                listaTransicoes.append(transicao_atual)
            i += 1
            break
        
        if "->" in linha:
            if transicao_atual:
                listaTransicoes.append(transicao_atual)
            transicao_atual = linha # Começa uma nova transição
        else:
            if linha: # É continuação da transição anterior (ex: "0,Z/ZZ")
                transicao_atual += " " + linha
        i += 1

    # 3. Lendo as palavras de teste
    while i < len(linhas):
        linha = linhas[i].strip()
        palavras_teste.append(linha)
        i += 1

    # 4. Configurando e executando o Autômato de Pilha
    automato = AutomatoDePilha(None, iniciais, alfabeto_entrada)
    transicoes = automato.criaDicionario(listaTransicoes)
    automato.transicoes = transicoes

    # Execução das entradas
    for entradaAtual in palavras_teste:
        
        if automato.verificaAlfabeto(entradaAtual) == False:
            print("X")
            continue

        aceita = False
        
        # Testa todos os estados iniciais
        for estadoInicial in automato.estadosIniciais:
            if automato.simulacao(estadoInicial, entradaAtual) == True:
                aceita = True
                break
        
        if aceita:
            print("OK")
        else:
            print("X")