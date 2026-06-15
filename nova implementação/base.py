# Máquina de Turing (ALL)
class TransicaoMT:
    def __init__(self):
        self.destino = 0
        self.escreve = ''
        self.direcao = ''
        self.definida = 0

# Autômato de Pilha (AP)
class TransicaoAP:
    def __init__(self):
        self.destino = 0
        self.lido = ''
        self.desempilha = ''
        self.empilha = ""
        self.definida = 0

# funções de busca
def buscar_estado(nome):
    for i in range(quantidade_de_estados):
        if estados[i] == nome:
            return i
    return -1

def indice_simbolo(simbolo, limite_procura):
    for i in range(limite_procura):
        if alfabeto[i] == simbolo:
            return i
    return -1

# abrindo arquivo
def abrir_arquivo(nome_arquivo):
    try:
        arquivo = open(nome_arquivo, 'r')
        return arquivo
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' arquivo não pode ser aberto.")
        return None

# AF: Autómato Finito Deterministico (AFD) e Autómato Finito Não Deterministico (AFN)
def processar_arquivo_af(arquivo_af, MAXIMO_ESTADOS, MAXIMO_ALFABETO): 
    arquivo = abrir_arquivo(arquivo_af)
    if arquivo is None:
        return
    
    transicoes_af = [[[0] * MAXIMO_ESTADOS for _ in range(MAXIMO_ALFABETO)] for _ in range(MAXIMO_ESTADOS)]

    pass

# Máquina de Turing (MT)
def processar_arquivo_mt(arquivo_mt, MAXIMO_ALFABETO): 
    arquivo = abrir_arquivo(arquivo_mt)
    if arquivo is None:
        return
    
    transicoes_mt = [[TransicaoMT() for _ in range(MAXIMO_ALFABETO)] for _ in range(MAXIMO_ESTADOS)]
    pass

# Autômato Linearmente Limitado (ALL)
def processar_arquivo_all(arquivo_all): 
    arquivo = abrir_arquivo(arquivo_all)
    if arquivo is None:
        return
    
    pass

# Autômato de Pilha (AP)
def processar_arquivo_ap(arquivo_ap, MAXIMO_ESTADOS): 
    arquivo = abrir_arquivo(arquivo_ap)
    if arquivo is None:
        return

    transicoes_ap = [[TransicaoAP() for _ in range(100)] for _ in range(MAXIMO_ESTADOS)]
    qtd_transicoes_ap = [0] * MAXIMO_ESTADOS

    pass

# função principal (main)
if __name__ == "__main__":

    # declarando variaveis 
    MAXIMO_ESTADOS = 100
    MAXIMO_LINHA = 256
    MAXIMO_ALFABETO = 128

    estados = [""] * MAXIMO_ESTADOS
    alfabeto = [""] * MAXIMO_ALFABETO
    finais = [0] * MAXIMO_ESTADOS
    estados_iniciais = [0] * MAXIMO_ESTADOS
    quantidade_de_estados = 0
    tamanho_alfabeto = 0

    print("SIMULADOR MULTI-AUTOMATOS UNIFICADO\nFormatos de simulador suportados: @AF, @MT, @ALL e @AP\n\n") # todos os formatos que o simulador aceita

    # Executando cada arquivo
    processar_arquivo_af("entrada_af.txt", MAXIMO_ESTADOS, MAXIMO_ALFABETO) 
    processar_arquivo_mt("entrada_mt.txt", MAXIMO_ALFABETO) 
    processar_arquivo_all("entrada_all.txt") 
    processar_arquivo_ap("entrada_ap.txt", MAXIMO_ESTADOS) 