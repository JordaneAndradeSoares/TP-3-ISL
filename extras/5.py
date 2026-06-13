import sys

MAXIMO_ESTADOS = 100
MAXIMO_LINHA = 256
MAXIMO_ALFABETO = 128

# ESTRUTURAS GLOBAIS
estados = [""] * MAXIMO_ESTADOS
alfabeto = [""] * MAXIMO_ALFABETO
finais = [0] * MAXIMO_ESTADOS
estados_iniciais = [0] * MAXIMO_ESTADOS
quantidade_de_estados = 0
tamanho_alfabeto = 0

# Matrizes para o Autómato Finito (AF)
transicoes_af = [[[0] * MAXIMO_ESTADOS for _ in range(MAXIMO_ALFABETO)] for _ in range(MAXIMO_ESTADOS)]

# Estruturas para a Máquina de Turing / ALL
class TransicaoMT:
    def __init__(self):
        self.destino = 0
        self.escreve = ''
        self.direcao = ''
        self.definida = 0

transicoes_mt = [[TransicaoMT() for _ in range(MAXIMO_ALFABETO)] for _ in range(MAXIMO_ESTADOS)]

# Estruturas para o Autômato de Pilha (AP)
class TransicaoAP:
    def __init__(self):
        self.destino = 0
        self.lido = ''
        self.desempilha = ''
        self.empilha = ""
        self.definida = 0

transicoes_ap = [[TransicaoAP() for _ in range(100)] for _ in range(MAXIMO_ESTADOS)]
qtd_transicoes_ap = [0] * MAXIMO_ESTADOS

# FUNÇÕES DE BUSCA
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

# FECHO LAMBDA (AFN)
def fecho_lambda(estados_ativos, indice_lambda):
    if indice_lambda == -1:
        return
    mudou = True
    while mudou:
        mudou = False
        for i in range(quantidade_de_estados):
            if estados_ativos[i]:
                for j in range(quantidade_de_estados):
                    if transicoes_af[i][indice_lambda][j] == 1 and estados_ativos[j] == 0:
                        estados_ativos[j] = 1
                        mudou = True

# SIMULADOR RECURSIVO DO AUTÔMATO DE PILHA (AP)
def simular_ap(estado, idx_input, input_str, pilha, topo, passos):
    if passos > 1000:
        return 0 # Proteção contra loops infinitos de lambda (\)

    # Critério de aceitação do PDF: palavra toda lida E pilha vazia
    if idx_input == len(input_str) and topo == 0:
        return 1

    for i in range(qtd_transicoes_ap[estado]):
        t = transicoes_ap[estado][i]

        char_lido = input_str[idx_input] if idx_input < len(input_str) else '\0'

        cond_input = (t.lido == '\\') or (char_lido != '\0' and char_lido == t.lido)
        cond_pilha = (t.desempilha == '\\') or (topo > 0 and pilha[topo - 1] == t.desempilha)

        if cond_input and cond_pilha:
            nova_pilha = list(pilha)
            novo_topo = topo

            if t.desempilha != '\\':
                novo_topo -= 1

            if t.empilha != "\\":
                tam = len(t.empilha)
                for j in range(tam - 1, -1, -1):
                    if novo_topo < 1000:
                        if novo_topo >= len(nova_pilha):
                            nova_pilha.append(t.empilha[j])
                        else:
                            nova_pilha[novo_topo] = t.empilha[j]
                        novo_topo += 1

            proximo_idx = idx_input
            if t.lido != '\\':
                proximo_idx += 1

            if simular_ap(t.destino, proximo_idx, input_str, nova_pilha, novo_topo, passos + 1):
                return 1

    return 0

# FUNÇÃO PRINCIPAL DE PROCESSAMENTO (IMPLEMENTA O EXTRA 5)
def processar_arquivo(nome_arquivo):
    global quantidade_de_estados, tamanho_alfabeto

    modo_automato = -1 # -1 = Indefinido, 0 = AF, 1 = MT, 2 = ALL, 3 = AP

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print(f"AVISO: Nao foi possivel abrir o arquivo '{nome_arquivo}'\n")
        return

    print(f" LENDO ARQUIVO: {nome_arquivo} ")

    # RESET COMPLETO DAS VARIÁVEIS GLOBAIS
    quantidade_de_estados = 0
    tamanho_alfabeto = 0
    for i in range(MAXIMO_ESTADOS):
        finais[i] = 0
        estados_iniciais[i] = 0
        qtd_transicoes_ap[i] = 0
        for j in range(MAXIMO_ALFABETO):
            transicoes_mt[i][j] = TransicaoMT()
            for k in range(MAXIMO_ESTADOS):
                transicoes_af[i][j][k] = 0

    # Configuração inicial padrão do alfabeto com lambda
    alfabeto[tamanho_alfabeto] = '\\'
    indice_lambda = tamanho_alfabeto
    tamanho_alfabeto += 1

    if not linhas:
        return

    # LEITURA DO HEADER @TIPO (Exigência do Extra 5)
    primeira_linha = linhas[0].strip('\r\n')
    if primeira_linha.startswith("@AF"):
        modo_automato = 0
        print("Tipo detetado: Automato Finito (AF)")
    elif primeira_linha.startswith("@MT"):
        modo_automato = 1
        print("Tipo detetado: Maquina de Turing (MT)")
    elif primeira_linha.startswith("@ALL"):
        modo_automato = 2
        print("Tipo detetado: Automato Linearmente Limitado (ALL)")
    elif primeira_linha.startswith("@AP"):
        modo_automato = 3
        print("Tipo detetado: Automato de Pilha (AP)")
    else:
        print("ERRO: Tipo invalido ou cabecalho '@TIPO' ausente na primeira linha!")
        return

    # LEITURA DO RESTANTE DA CONFIGURAÇÃO DO AUTOMATO
    idx_linha = 1
    while idx_linha < len(linhas):
        linha = linhas[idx_linha].strip('\r\n')
        idx_linha += 1

        if len(linha) == 0:
            continue
        if linha.startswith("---"):
            break

        # Definição de Estados (Q:)
        if linha.startswith("Q:"):
            tokens = linha[2:].split()
            for token in tokens:
                estados[quantidade_de_estados] = token
                quantidade_de_estados += 1

        # Definição de Alfabeto de Entrada (S:)
        elif linha.startswith("S:"):
            tamanho_alfabeto = 0
            for char in linha[2:]:
                if char != ' ':
                    alfabeto[tamanho_alfabeto] = char
                    tamanho_alfabeto += 1
            alfabeto[tamanho_alfabeto] = '\\'
            indice_lambda = tamanho_alfabeto
            tamanho_alfabeto += 1

        # Alfabeto da Fita / Pilha (G:)
        elif linha.startswith("G:"):
            continue

        # Estados Iniciais (I:)
        elif linha.startswith("I:"):
            tokens = linha[2:].split()
            for token in tokens:
                idx = buscar_estado(token)
                if idx != -1:
                    estados_iniciais[idx] = 1

        # Estados Finais (F:)
        elif linha.startswith("F:"):
            tokens = linha[2:].split()
            for token in tokens:
                idx = buscar_estado(token)
                if idx != -1:
                    finais[idx] = 1

        # Processamento das Linhas de Transição
        else:
            if "->" not in linha or "|" not in linha:
                continue

            partes = linha.split("->")
            origem = partes[0].strip()

            subpartes = partes[1].split("|")
            destino = subpartes[0].strip()
            simbolos_str = subpartes[1].strip()

            idx_origem = buscar_estado(origem)
            idx_destino = buscar_estado(destino)

            if idx_origem != -1 and idx_destino != -1:
                tokens = simbolos_str.split()

                for token in tokens:
                    if modo_automato in (1, 2):
                        if len(token) >= 4 and token[1] == '/':
                            lido = token[0]
                            escreve = token[2]
                            direcao = token[3]

                            t_mt = transicoes_mt[idx_origem][ord(lido)]
                            t_mt.destino = idx_destino
                            t_mt.escreve = escreve
                            t_mt.direcao = direcao
                            t_mt.definida = 1

                    elif modo_automato == 3:
                        if ',' in token and '/' in token:
                            pos_virgula = token.find(',')
                            pos_barra = token.find('/')

                            lido = token[0]
                            desempilha = token[pos_virgula + 1]
                            empilha = token[pos_barra + 1:]

                            idx_t = qtd_transicoes_ap[idx_origem]
                            if idx_t < 100:
                                t_ap = transicoes_ap[idx_origem][idx_t]
                                t_ap.destino = idx_destino
                                t_ap.lido = lido
                                t_ap.desempilha = desempilha
                                t_ap.empilha = empilha
                                t_ap.definida = 1
                                qtd_transicoes_ap[idx_origem] += 1
                    else:
                        idx_simb = indice_simbolo(token[0], tamanho_alfabeto)
                        if idx_simb != -1:
                            transicoes_af[idx_origem][idx_simb][idx_destino] = 1

    # PROCESSAMENTO DOS CASOS DE TESTE
    print("Resultados:")

    if modo_automato in (1, 2):
        # MODO MÁQUINA DE TURING / ALL
        while idx_linha < len(linhas):
            linha = linhas[idx_linha].strip('\r\n')
            idx_linha += 1
            if len(linha) == 0:
                continue

            fita = ['_'] * 5000
            fita[0] = '<'

            tam_palavra = len(linha)
            if tam_palavra > 0:
                for i in range(tam_palavra):
                    fita[1 + i] = linha[i]

            if modo_automato == 2:
                fita[1 + tam_palavra] = '>'

            cabecote = 1
            estado_atual = -1

            for i in range(quantidade_de_estados):
                if estados_iniciais[i]:
                    estado_atual = i
                    break

            passos = 0
            executando = (estado_atual != -1)
            aceito = 0

            while executando:
                passos += 1
                if passos > 10000:
                    break
                if cabecote < 0 or cabecote >= 5000:
                    break

                lido = fita[cabecote]
                t = transicoes_mt[estado_atual][ord(lido)]

                if t.definida:
                    fita[cabecote] = t.escreve
                    estado_atual = t.destino
                    if t.direcao in ('D', 'd'):
                        cabecote += 1
                    elif t.direcao in ('E', 'e'):
                        cabecote -= 1
                else:
                    if finais[estado_atual]:
                        aceito = 1
                    executando = False

            ultimo_nao_vazio = 0
            for i in range(len(fita) - 2, -1, -1):
                if fita[i] != '_':
                    ultimo_nao_vazio = i
                    break

            resultado_fita = "".join(fita[:ultimo_nao_vazio + 1])
            if aceito:
                print(f"OK {resultado_fita}")
            else:
                print(f"X {resultado_fita}")

    elif modo_automato == 3:
        # MODO AUTÔMATO DE PILHA (AP)
        while idx_linha < len(linhas):
            linha = linhas[idx_linha].strip('\r\n')
            idx_linha += 1
            if len(linha) == 0:
                continue

            estado_inicial = -1
            for i in range(quantidade_de_estados):
                if estados_iniciais[i]:
                    estado_inicial = i
                    break

            pilha_inicial = [''] * 1000
            topo_inicial = 0
            aceito = 0

            if estado_inicial != -1:
                aceito = simular_ap(estado_inicial, 0, linha, pilha_inicial, topo_inicial, 0)

            if aceito:
                print("OK")
            else:
                print("X")

    else:
        # MODO AUTÔMATO FINITO (AF)
        while idx_linha < len(linhas):
            linha = linhas[idx_linha].strip('\r\n')
            idx_linha += 1
            if len(linha) == 0:
                continue

            estados_atuais = [estados_iniciais[i] for i in range(quantidade_de_estados)]
            fecho_lambda(estados_atuais, indice_lambda)
            rejeitada = 0

            for char in linha:
                indice = indice_simbolo(char, tamanho_alfabeto - 1)
                if indice == -1:
                    rejeitada = 1
                    break

                proximos_estados = [0] * MAXIMO_ESTADOS
                for e in range(quantidade_de_estados):
                    if estados_atuais[e]:
                        for dest in range(quantidade_de_estados):
                            if transicoes_af[e][indice][dest] == 1:
                                proximos_estados[dest] = 1

                estados_atuais = proximos_estados[:]
                fecho_lambda(estados_atuais, indice_lambda)

            aceito = 0
            if not rejeitada:
                for i in range(quantidade_de_estados):
                    if estados_atuais[i] and finais[i]:
                        aceito = 1
                        break

            if aceito:
                print("OK")
            else:
                print("X")

    print() # Linha em branco extra

# função principal (main)
if __name__ == "__main__":
    # Exigência do Extra 5: Especificar os formatos que o simulador aceita
    print("SIMULADOR MULTI-AUTOMATOS UNIFICADO")
    print("Tipos de ficheiro suportados: @AF, @MT, @ALL e @AP")

    # Executando os arquivos de teste dinamicamente
    processar_arquivo("entrada1.txt") # Abre, processa e FECHA
    processar_arquivo("entrada2.txt") # Abre, processa e FECHA
    processar_arquivo("entrada3.txt") # Abre, processa e FECHA