#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int buscar_estado(char estados[][8], char *nome, int quantidade_de_estados)
{
    for (int i = 0; i < quantidade_de_estados; i++)
    {
        if (strcmp(estados[i], nome) == 0)
        {
            return i;
        }
    }

    return -1;
}

int main()
{
    // variáveis
    const int maximo_estados = 100;
    const int maximo_linha = 256;

    int quantidade_de_estados = 0;
    int estado_inicial = -1;

    int finais[maximo_estados];
    int transicoes[maximo_estados][2];

    char estados[maximo_estados][8];
    char linha[maximo_linha];

    FILE *arquivo = fopen("entrada.txt", "r");

    if (arquivo == NULL)
    {
        printf("Erro ao abrir entrada.txt\n");
        return 1;
    }

    for (int i = 0; i < maximo_estados; i++)
    {
        finais[i] = 0;
        for (int j = 0; j < 2; j++)
        {
            transicoes[i][j] = -1;
        }
    }

    // Q:
    if (fgets(linha, sizeof(linha), arquivo) == NULL)
    {
        fclose(arquivo);
        return 1;
    }

    char *token = strtok(linha + 3, " \n");
    while (token != NULL)
    {
        strcpy(estados[quantidade_de_estados], token);
        quantidade_de_estados++;
        token = strtok(NULL, " \n");
    }

    // I:
    if (fgets(linha, sizeof(linha), arquivo) == NULL)
    {
        fclose(arquivo);
        return 1;
    }

    char nome_inicial[8];
    sscanf(linha, "I: %7s", nome_inicial);
    estado_inicial = buscar_estado(estados, nome_inicial, quantidade_de_estados);

    // F:
    if (fgets(linha, sizeof(linha), arquivo) == NULL)
    {
        fclose(arquivo);
        return 1;
    }

    token = strtok(linha + 3, " \n");
    while (token != NULL)
    {
        int indice = buscar_estado(estados, token, quantidade_de_estados);
        if (indice != -1)
        {
            finais[indice] = 1;
        }
        token = strtok(NULL, " \n");
    }

    // Transições
    while (fgets(linha, sizeof(linha), arquivo))
    {
        if (strncmp(linha, "---", 3) == 0)
        {
            break;
        }

        char origem[8];
        char destino[8];

        char *seta = strstr(linha, "->");
        char *barra = strstr(linha, "|");

        if (seta == NULL || barra == NULL)
        {
            continue;
        }

        sscanf(linha, "%7s", origem);
        sscanf(seta + 2, "%7s", destino);

        int indice_origem = buscar_estado(estados, origem, quantidade_de_estados);
        int indice_destino = buscar_estado(estados, destino, quantidade_de_estados);

        char simbolos[100];
        strcpy(simbolos, barra + 1);

        token = strtok(simbolos, " \n");
        while (token != NULL)
        {
            if (strcmp(token, "0") == 0)
            {
                transicoes[indice_origem][0] = indice_destino;
            }
            else if (strcmp(token, "1") == 0)
            {
                transicoes[indice_origem][1] = indice_destino;
            }
            token = strtok(NULL, " \n");
        }
    }

    // Casos de teste
    while (fgets(linha, sizeof(linha), arquivo))
    {
        linha[strcspn(linha, "\n")] = '\0';

        int estado_atual = estado_inicial;
        int rejeitada = 0;

        for (int i = 0; linha[i] != '\0'; i++)
        {
            int simbolo = linha[i] - '0';
            if (simbolo != 0 && simbolo != 1)
            {
                rejeitada = 1;
                break;
            }
            if (transicoes[estado_atual][simbolo] == -1)
            {
                rejeitada = 1;
                break;
            }
            estado_atual = transicoes[estado_atual][simbolo];
        }

        if (!rejeitada && finais[estado_atual])
        {
            printf("OK\n");
        }
        else
        {
            printf("X\n");
        }
    }

    fclose(arquivo);
    return 0;
}