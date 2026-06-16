from extra_alfabeto import ler_afd_com_alfabeto

with open("entrada.txt") as arq:
    linhas = arq.readlines()

afd, palavras = ler_afd_com_alfabeto(linhas)

for palavra in palavras:

    if afd.validar_palavra(palavra):
        print("OK")
    else:
        print("X")