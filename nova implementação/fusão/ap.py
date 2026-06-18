from collections import deque

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

            for i in range(len(separacao)):
                if "\\" in separacao[i]:
                    separacao[i] = separacao[i].replace("\\", "λ")

            # Evita linhas vazias ou mal formatadas
            if len(separacao) < 4:
                continue

            estadoAtual = separacao[0]
            estadoProx = separacao[1]
            # separacao[2] é o caractere "|"

            for p in range(3, len(separacao)):
                transicaoAtual = separacao[p]
                
                if not transicaoAtual: # Ignora espaços em branco excedentes
                    continue

                partes = transicaoAtual.split(",")
                entrada = partes[0]

                if entrada == "λ":
                    self.tLambda = True

                infoPilha = partes[1].split("/")
                desempilha = infoPilha[0]
                empilha = infoPilha[1]

                chave = (estadoAtual, entrada, desempilha)
                
                # Para suportar o não-determinismo, guardamos as transições em uma lista
                if chave not in transicoes:
                    transicoes[chave] = []
                transicoes[chave].append((estadoProx, empilha))
            
        return transicoes

    def simulacao(self, estadoI, entrada):
        # A configuração agora inicia com a pilha completamente vazia tuple()
        iniciais = {(estadoI, 0, tuple())}
        
        def expandeLambda(configs):
            visitados = set(configs)
            fila = deque(configs)
            while fila:
                estado, idx, pilha = fila.popleft()
                
                # Se a pilha está vazia, nosso "topo" imaginário pode ser tratado como "λ"
                topo = pilha[-1] if pilha else "λ"

                # Se a pilha for vazia, só testamos desempilhar "λ"
                consultas = [(estado, "λ", topo), (estado, "λ", "λ")]
                if not pilha:
                    consultas = [(estado, "λ", "λ")]

                for consulta in consultas:
                    if consulta in self.transicoes:
                        # Agora iteramos por todas as transições possíveis a partir daquela chave
                        for novoEstado, empilha in self.transicoes[consulta]:
                            novaPilha = list(pilha)
                            
                            # Desempilha se não for lambda e a pilha não for vazia
                            if consulta[2] != "λ" and novaPilha:
                                novaPilha.pop()
                                
                            # Empilha se não for lambda
                            if empilha != "λ":
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
                topo = pilha[-1] if pilha else "λ"
                
                consultas = [(estado, simbolo, topo), (estado, simbolo, "λ")]
                if not pilha:
                    consultas = [(estado, simbolo, "λ")]
                    
                for consulta in consultas:
                    if consulta in self.transicoes:
                        for novoEstado, empilha in self.transicoes[consulta]:
                            novaPilha = list(pilha)

                            # Desempilha se não for lambda e a pilha não for vazia
                            if consulta[2] != "λ" and novaPilha:
                                novaPilha.pop()
                                
                            if empilha != "λ":
                                for s in reversed(empilha):
                                    novaPilha.append(s)
                                    
                            proximas.add((novoEstado, i + 1, tuple(novaPilha)))
            
            configs = expandeLambda(proximas)
            if not configs:
                return False

        # Segundo a especificação, as palavras são reconhecidas quando lidas completamente e a pilha está vazia. [cite: 75]
        return any(len(pilha) == 0 for estado, idx, pilha in configs)

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