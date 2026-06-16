from extra_alfabeto import ler_afd_com_alfabeto

class TransicaoMT:
    def __init__(self):
        self.destino = 0
        self.escreve = ''
        self.direcao = ''
        self.definida = 0

class TransicaoAP:
    def __init__(self):
        self.destino = 0
        self.lido = ''
        self.desempilha = ''
        self.empilha = ""
        self.definida = 0

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

def abrir_arquivo(nome_arquivo):
    try:
        return open(nome_arquivo, 'r')
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' arquivo não pode ser aberto.")
        return None

def processar_arquivo_af(arquivo_af, MAXIMO_ESTADOS, MAXIMO_ALFABETO):
    arquivo = abrir_arquivo(arquivo_af)
    if arquivo is None:
        return

    linhas = arquivo.readlines()
    afd, palavras = ler_afd_com_alfabeto(linhas)

    for palavra in palavras:
        if afd.validar_palavra(palavra):
            print("OK")
        else:
            print("X")

def processar_arquivo_mt(arquivo_mt, MAXIMO_ESTADOS, MAXIMO_ALFABETO):
    arquivo = abrir_arquivo(arquivo_mt)
    if arquivo is None:
        return

    transicoes_mt = [[TransicaoMT() for _ in range(MAXIMO_ALFABETO)] for _ in range(MAXIMO_ESTADOS)]
    pass

def processar_arquivo_all(arquivo_all):
    arquivo = abrir_arquivo(arquivo_all)
    if arquivo is None:
        return

    pass

def processar_arquivo_ap(arquivo_ap, MAXIMO_ESTADOS):
    arquivo = abrir_arquivo(arquivo_ap)
    if arquivo is None:
        return

    transicoes_ap = [[TransicaoAP() for _ in range(100)] for _ in range(MAXIMO_ESTADOS)]
    qtd_transicoes_ap = [0] * MAXIMO_ESTADOS

    pass

if __name__ == "__main__":

    MAXIMO_ESTADOS = 100
    MAXIMO_LINHA = 256
    MAXIMO_ALFABETO = 128

    estados = [""] * MAXIMO_ESTADOS
    alfabeto = [""] * MAXIMO_ALFABETO
    finais = [0] * MAXIMO_ESTADOS
    estados_iniciais = [0] * MAXIMO_ESTADOS
    quantidade_de_estados = 0
    tamanho_alfabeto = 0

    print("SIMULADOR MULTI-AUTOMATOS UNIFICADO\nFormatos de simulador suportados: @AF, @MT, @ALL e @AP")

    # @AF
    print("\n@AF (abrindo 'entrada_af.txt'):")
    processar_arquivo_af("entrada_af.txt", MAXIMO_ESTADOS, MAXIMO_ALFABETO)

    # @MT
    print("\n@MT (abrindo 'entrada_mt.txt'):")
    processar_arquivo_mt("entrada_mt.txt", MAXIMO_ESTADOS, MAXIMO_ALFABETO)

    # @ALL
    print("\n@ALL (abrindo 'entrada_all.txt'):")
    processar_arquivo_all("entrada_all.txt")

    # @AP
    print("\n@AP (abrindo 'entrada_ap.txt'):")
    processar_arquivo_ap("entrada_ap.txt", MAXIMO_ESTADOS)