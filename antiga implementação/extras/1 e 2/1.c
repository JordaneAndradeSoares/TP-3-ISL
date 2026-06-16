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

int indice_simbolo(char simbolo, char alfabeto[], int tamanho_alfabeto)
{
    for (int i = 0; i < tamanho_alfabeto; i++)
    {
        if (alfabeto[i] == simbolo)
        {
            return i;
        }
    }

    return -1;
}

int main()
{
    const int maximo_estados = 100;
    const int maximo_linha = 256;
    const int maximo_alfabeto = 128;

    int quantidade_de_estados = 0;
    int estado_inicial = -1;
    int tamanho_alfabeto = 0;

    char estados[maximo_estados][8];
    char alfabeto[maximo_alfabeto];

    int finais[maximo_estados];
    int transicoes[maximo_estados][maximo_alfabeto];

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

        for (int j = 0; j < maximo_alfabeto; j++)
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

    // S:

    if (fgets(linha, sizeof(linha), arquivo) == NULL)
    {
        fclose(arquivo);
        return 1;
    }

    if (strncmp(linha, "S:", 2) != 0)
    {
        printf("Erro: linha S: nao encontrada.\n");

        fclose(arquivo);
        return 1;
    }

    for (int i = 2; linha[i] != '\0' && linha[i] != '\n'; i++)
    {
        if (linha[i] != ' ')
        {
            alfabeto[tamanho_alfabeto] = linha[i];
            tamanho_alfabeto++;
        }
    }

    // I:

    if (fgets(linha, sizeof(linha), arquivo) == NULL)
    {
        fclose(arquivo);
        return 1;
    }

    char nome_inicial[8];

    sscanf(linha, "I: %7s", nome_inicial);

    estado_inicial =
        buscar_estado(
            estados,
            nome_inicial,
            quantidade_de_estados
        );

    // F:

    if (fgets(linha, sizeof(linha), arquivo) == NULL)
    {
        fclose(arquivo);
        return 1;
    }

    token = strtok(linha + 3, " \n");

    while (token != NULL)
    {
        int indice =
            buscar_estado(
                estados,
                token,
                quantidade_de_estados
            );

        if (indice != -1)
        {
            finais[indice] = 1;
        }

        token = strtok(NULL, " \n");
    }

    // Transicoes

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

        int indice_origem =
            buscar_estado(
                estados,
                origem,
                quantidade_de_estados
            );

        int indice_destino =
            buscar_estado(
                estados,
                destino,
                quantidade_de_estados
            );

        char simbolos[128];

        strcpy(simbolos, barra + 1);

        token = strtok(simbolos, " \n");

        while (token != NULL)
        {
            int indice =
                indice_simbolo(
                    token[0],
                    alfabeto,
                    tamanho_alfabeto
                );

            if (indice != -1)
            {
                transicoes[indice_origem][indice] =
                    indice_destino;
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
            int indice =
                indice_simbolo(
                    linha[i],
                    alfabeto,
                    tamanho_alfabeto
                );

            if (indice == -1)
            {
                rejeitada = 1;
                break;
            }

            if (transicoes[estado_atual][indice] == -1)
            {
                rejeitada = 1;
                break;
            }

            estado_atual =
                transicoes[estado_atual][indice];
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