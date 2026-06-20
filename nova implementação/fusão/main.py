import os

from extra_alfabeto import ler_afd_com_alfabeto # importando função da implementação da AF
from ap import AutomatoDePilha #importando classe da implementação da AP
from afn import leituraAFN #importando classe da implementaçao do AFN

# função principal para chamar as funções de processamento dos arquivos
if __name__ == "__main__":
    print("SIMULADOR MULTI-AUTOMATOS UNIFICADO\nFormatos de simulador suportados: @AF, @AFN, @MT, @ALL e @AP\n")

    # pedindo o nome do arquivo de entrada para o usuário
    arquivoEntrada = input("Digite o arquivo de entrada: ")
    print(f"\nProcessando o arquivo '{arquivoEntrada}'...\nResultados:")

    # criando o caminho do arquivo de entrada   
    caminho = os.path.join('arquivos', arquivoEntrada)

    # tentando abrir o arquivo de entrada
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            entrada = arquivo.read()

    # tratando o erro caso não consiga abrir o arquivo de entrada
    except FileNotFoundError:
        print(f"\nErro: arquivo '{caminho}' não encontrado.")
        exit()

    vetLinhas = entrada.split('\n')
    tipoAutomato = vetLinhas.pop(0)

    match tipoAutomato:
        case "@AF":
            ler_afd_com_alfabeto(vetLinhas)
            
        case "@AP":
            AutomatoDePilha.leituraPilha(vetLinhas)

        case "@AFN":
            leituraAFN(vetLinhas)

        case "@MT":
            print("Simulador de Máquina de Turing AINDA não implementado.") #TODO: fazer essa maquina

        case "@ALL":
            print("Simulador de Máquina de Turing AINDA não implementado.") #TODO: fazer essa maquin