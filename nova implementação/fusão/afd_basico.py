class AFD:
    estados: set[str] # Conjuto de Todos os Estados
    estado_inicial: str 
    estados_finais: set[str] # Conjunto de estados Fnais
    transicoes: dict[tuple[str, str], str] # Conjunto de Transições

    def __init__(self):
        self.estados = set() 
        self.estado_inicial = ""
        self.estados_finais = set() 
        self.transicoes = {} 

    def adicionar_transicao(self, estado_origem, simbolo, estado_destino): # Adiciona uma nova transicao ao conjunto
        self.transicoes[(estado_origem, simbolo)] = estado_destino

    def validar_palavra(self, palavra):
        estado_atual = self.estado_inicial

        # Altera o estado atual a depender do simbolo atual + estado atual e se existir transicao para isso
        for simbolo in palavra:
            if (estado_atual, simbolo) not in self.transicoes:
                return False # Não existe transicao com esse simbolo nesse estado_atual. Retorna que a palavra não pode ser lida por inteiro

            # Existe transicao valida, passando para o proximo estado
            estado_atual = self.transicoes[(estado_atual, simbolo)]

        # Como a palavra foi lida por inteiro, confere se estamos em algum estado final
        return estado_atual in self.estados_finais

def ler_afd(linhas):
    afd = AFD()

    i = 0

    # Q:
    afd.estados = set(linhas[i].strip().split()[1:])
    i += 1

    # I:
    afd.estado_inicial = linhas[i].strip().split()[1]
    i += 1

    # F:
    afd.estados_finais = set(linhas[i].strip().split()[1:])
    i += 1

    # Transições
    while linhas[i].strip() != "---":
        
        esquerda, direita = linhas[i].split("|")
        estado_origem, seta, estado_destino = esquerda.strip().split()
        simbolos = direita.strip().split()

        for simbolo in simbolos:
            afd.adicionar_transicao(estado_origem, simbolo, estado_destino)

        i += 1

    i += 1

    palavras = [linha.rstrip("\n") for linha in linhas[i:]]

    return afd, palavras

def processar_arquivo(nome_arquivo):
    with open(nome_arquivo, "r") as arq:
        linhas = arq.readlines()

    afd, palavras = ler_afd(linhas)

    resultados = []

    for palavra in palavras:

        if afd.validar_palavra(palavra):
            resultados.append("OK")
        else:
            resultados.append("X")

    return resultados