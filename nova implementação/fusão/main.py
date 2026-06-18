from extra_alfabeto import ler_afd_com_alfabeto # importando função da implementação da AF
from ap import automato_de_pilha # importando função da implementação da APs
 
# função para abrir arquivo e tratar possivel erro de abertura do arquivo
def abrir_arquivo(nome_arquivo): 
    try:
        return open(nome_arquivo, 'r', encoding='utf-8') 
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não pode ser aberto.")
        return None

# AF
def processar_arquivo_af(arquivo_af):
    arquivo = abrir_arquivo(arquivo_af)
    if arquivo is None:
        return

    linhas = arquivo.readlines()
    arquivo.close() 
    print("Arquivo lido e fechado com sucesso. Processando...")

    ler_afd_com_alfabeto(linhas) 

# MT
def processar_arquivo_mt(arquivo_mt):
    arquivo = abrir_arquivo(arquivo_mt)
    if arquivo is None:
        return
    
    arquivo.close() 
    print("Arquivo lido e fechado com sucesso. Processando...")

# ALL
def processar_arquivo_all(arquivo_all):
    arquivo = abrir_arquivo(arquivo_all)
    if arquivo is None:
        return

    arquivo.close() 
    print("Arquivo lido e fechado com sucesso. Processando...")

# AP
def processar_arquivo_ap(arquivo_ap):
    arquivo = abrir_arquivo(arquivo_ap)

    if arquivo is None:
        return

    linhas = arquivo.readlines()
    arquivo.close()
    print("Arquivo lido e fechado com sucesso. Processando...")

    automato_de_pilha(linhas)
 
# função principal para chamar as funções de processamento dos arquivos
if __name__ == "__main__":
    print("SIMULADOR MULTI-AUTOMATOS UNIFICADO\nFormatos de simulador suportados: @AF, @MT, @ALL e @AP")

    # @AF
    print("\nAbrindo 'entrada_af.txt'. Resultado @AF:")
    processar_arquivo_af("entrada_af.txt")

    # @MT
    print("\nAbrindo 'entrada_mt.txt'. Resultado @MT:")
    processar_arquivo_mt("entrada_mt.txt")

    # @ALL
    print("\nAbrindo 'entrada_all.txt'. Resultado @ALL:")
    processar_arquivo_all("entrada_all.txt")

    # @AP
    print("\nAbrindo 'entrada_ap.txt'. Resultado @AP:")
    processar_arquivo_ap("entrada_ap.txt")