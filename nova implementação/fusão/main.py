from extra_alfabeto import ler_afd_com_alfabeto # importando função da implementação da AF
from ap import AutomatoDePilha
    
# função principal para chamar as funções de processamento dos arquivos
if __name__ == "__main__":
    print("SIMULADOR MULTI-AUTOMATOS UNIFICADO\nFormatos de simulador suportados: @AF, @MT, @ALL e @AP")

    print("digite o arquivo de entrada:")
    arquivoEntrada = input()

    with open('nova implementação/fusão/' + arquivoEntrada, 'r', encoding='utf-8') as arquivo:

        entrada = arquivo.read()

    vetLinhas = entrada.split('\n')
    tipoAutomato = vetLinhas.pop(0)

    match tipoAutomato:
        case "@AF":
            ler_afd_com_alfabeto(vetLinhas)
            
        case "@AP":
            AutomatoDePilha.leituraPilha(vetLinhas)

        #fazer o resto dos cases para as outras maquinas