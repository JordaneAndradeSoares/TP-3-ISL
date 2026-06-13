#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int maximo_estados = 100;
const int maximo_linha = 256;
const int maximo_alfabeto = 128;

// VARIÁVEIS GLOBAIS: Movemos a matriz para cá para evitar o Stack Overflow no Windows
int transicoes[100][128][100];
char estados[100][8];
char alfabeto[128];
int finais[100];
int estados_iniciais[100];

int buscar_estado(char estados[][8], char *nome, int quantidade_de_estados) {
    for (int i = 0; i < quantidade_de_estados; i++) {
        if (strcmp(estados[i], nome) == 0) return i;
    }
    return -1;
}

int indice_simbolo(char simbolo, char alfabeto[], int tamanho_alfabeto) {
    for (int i = 0; i < tamanho_alfabeto; i++) {
        if (alfabeto[i] == simbolo) return i;
    }
    return -1;
}

void fecho_lambda(int estados_ativos[], int indice_lambda, int quantidade_de_estados) {
    if (indice_lambda == -1) return;
    int mudou = 1;
    while (mudou) {
        mudou = 0;
        for (int i = 0; i < quantidade_de_estados; i++) {
            if (estados_ativos[i]) {
                for (int j = 0; j < quantidade_de_estados; j++) {
                    if (transicoes[i][indice_lambda][j] == 1 && estados_ativos[j] == 0) {
                        estados_ativos[j] = 1;
                        mudou = 1;
                    }
                }
            }
        }
    }
}

int main() {
    int quantidade_de_estados = 0, tamanho_alfabeto = 0;
    char linha[256];

    FILE *arquivo = fopen("entrada.txt", "r");
    if (arquivo == NULL) {
        printf("ERRO FATAL: Arquivo 'entrada.txt' nao encontrado na pasta atual!\n");
        return 1;
    }

    // Inicialização segura das matrizes
    for (int i = 0; i < maximo_estados; i++) {
        finais[i] = 0;
        estados_iniciais[i] = 0;
        for (int j = 0; j < maximo_alfabeto; j++)
            for (int k = 0; k < maximo_estados; k++) 
                transicoes[i][j][k] = 0;
    }

    // --- Q: ---
    if (fgets(linha, sizeof(linha), arquivo) == NULL) { printf("ERRO Q\n"); return 1; }
    char *inicio_q = strstr(linha, "Q:");
    if (!inicio_q) { printf("ERRO: Linha Q nao encontrada.\n"); return 1; }
    char *token = strtok(inicio_q + 2, " \r\n");
    while (token != NULL) {
        strcpy(estados[quantidade_de_estados++], token);
        token = strtok(NULL, " \r\n");
    }

    // --- S: ---
    if (fgets(linha, sizeof(linha), arquivo) == NULL) { printf("ERRO S\n"); return 1; }
    for (int i = 2; linha[i] != '\0' && linha[i] != '\n' && linha[i] != '\r'; i++) {
        if (linha[i] != ' ') {
            alfabeto[tamanho_alfabeto++] = linha[i];
        }
    }
    alfabeto[tamanho_alfabeto] = '\\';
    int indice_lambda = tamanho_alfabeto++;

    // --- I: ---
    if (fgets(linha, sizeof(linha), arquivo) == NULL) { printf("ERRO I\n"); return 1; }
    token = strtok(linha + 3, " \r\n");
    while (token != NULL) {
        int idx = buscar_estado(estados, token, quantidade_de_estados);
        if (idx != -1) estados_iniciais[idx] = 1;
        token = strtok(NULL, " \r\n");
    }

    // --- F: ---
    if (fgets(linha, sizeof(linha), arquivo) == NULL) { printf("ERRO F\n"); return 1; }
    token = strtok(linha + 3, " \r\n");
    while (token != NULL) {
        int idx = buscar_estado(estados, token, quantidade_de_estados);
        if (idx != -1) finais[idx] = 1;
        token = strtok(NULL, " \r\n");
    }

    // --- Transicoes ---
    while (fgets(linha, sizeof(linha), arquivo)) {
        if (strncmp(linha, "---", 3) == 0) break;
        
        char origem[8], destino[8];
        char *seta = strstr(linha, "->");
        char *barra = strstr(linha, "|");

        if (seta == NULL || barra == NULL) continue;

        sscanf(linha, "%7s", origem);
        sscanf(seta + 2, "%7s", destino);

        int indice_origem = buscar_estado(estados, origem, quantidade_de_estados);
        int indice_destino = buscar_estado(estados, destino, quantidade_de_estados);

        char simbolos[128];
        strcpy(simbolos, barra + 1);
        token = strtok(simbolos, " \r\n");

        while (token != NULL) {
            int indice = indice_simbolo(token[0], alfabeto, tamanho_alfabeto);
            if (indice != -1 && indice_origem != -1 && indice_destino != -1) {
                transicoes[indice_origem][indice][indice_destino] = 1;
            }
            token = strtok(NULL, " \r\n");
        }
    }

    // --- Casos de teste ---
    while (fgets(linha, sizeof(linha), arquivo)) {
        linha[strcspn(linha, "\r\n")] = '\0';
        if (strlen(linha) == 0 && feof(arquivo)) continue;

        int estados_atuais[100];
        for (int i = 0; i < quantidade_de_estados; i++) estados_atuais[i] = estados_iniciais[i];

        fecho_lambda(estados_atuais, indice_lambda, quantidade_de_estados);
        int rejeitada = 0;

        for (int i = 0; linha[i] != '\0'; i++) {
            int indice = indice_simbolo(linha[i], alfabeto, tamanho_alfabeto - 1); 
            if (indice == -1) { rejeitada = 1; break; }

            int proximos_estados[100] = {0};

            for (int e = 0; e < quantidade_de_estados; e++) {
                if (estados_atuais[e]) {
                    for (int dest = 0; dest < quantidade_de_estados; dest++) {
                        if (transicoes[e][indice][dest] == 1) {
                            proximos_estados[dest] = 1;
                        }
                    }
                }
            }
            for (int e = 0; e < quantidade_de_estados; e++) estados_atuais[e] = proximos_estados[e];
            fecho_lambda(estados_atuais, indice_lambda, quantidade_de_estados);
        }

        int aceito = 0;
        if (!rejeitada) {
            for (int i = 0; i < quantidade_de_estados; i++) {
                if (estados_atuais[i] && finais[i]) { aceito = 1; break; }
            }
        }
        if (aceito) printf("OK\n");
        else printf("X\n");
    }

    fclose(arquivo);
    return 0;
}