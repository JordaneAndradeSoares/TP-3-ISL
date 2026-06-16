# Importa a classe AFD implementada no trabalho básico
from afd_basico import AFD

# Adicionando o suporte a alfabetos arbitrarios definidos pela linha S:
class AFDComAlfabeto(AFD):

    def __init__(self):

        # Inicializa todos os atributos da classe pai (AFD)
        super().__init__()

        # Armazena os símbolos do alfabeto
            # Exemplo:
            # S: abc
            # {'a', 'b', 'c'}
        self.alfabeto = set()

    def validar_palavra(self, palavra):

        # Verifica se todos os símbolos da palavra
        # pertencem ao alfabeto definido na entrada
        for simbolo in palavra:
            if simbolo not in self.alfabeto:
                return False

        # Utiliza o validar palavra do pai normalmente
        return super().validar_palavra(palavra)
    

# Le um arquivo de entrada contendo um AFD com alfabeto arbitrario
def ler_afd_com_alfabeto(linhas):

    afd = AFDComAlfabeto()

    i = 0

    afd.estados = set(linhas[i].strip().split()[1:])
    i += 1

    linha_alfabeto = linhas[i].rstrip("\n")
    afd.alfabeto = set(linha_alfabeto[3:])
    i += 1

    afd.estado_inicial = linhas[i].strip().split()[1]
    i += 1

    afd.estados_finais = set(linhas[i].strip().split()[1:])
    i += 1

    while linhas[i].strip() != "---":

        esquerda, direita = linhas[i].split("|")

        origem, seta, destino = esquerda.strip().split()

        seta = ""

        simbolos = direita.strip().split()

        for simbolo in simbolos:
            afd.adicionar_transicao(origem, simbolo, destino)

        i += 1

    i += 1

    palavras = [linha.rstrip("\n") for linha in linhas[i:]]

    return afd, palavras