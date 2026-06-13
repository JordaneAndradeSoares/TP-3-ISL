#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int maximo_estados = 100;
const int maximo_linha = 256;
const int maximo_alfabeto = 128;

// --- ESTRUTURAS GLOBAIS (Evita Stack Overflow) ---
char estados[100][8];
char alfabeto[128];
int finais[100];
int estados_iniciais[100];
int quantidade_de_estados = 0, tamanho_alfabeto = 0;

// Matrizes para o Autômato Finito (AF)
int transicoes_af[100][128][100];

// Estruturas para a Máquina de Turing / ALL
typedef struct {
    int destino;
    char escreve;
    char direcao; // 'D' ou 'E'
    int definida;
} TransicaoMT;
TransicaoMT transicoes_mt[100][128]; 

// --- FUNÇÕES DE BUSCA ---
int buscar_estado(char *nome) {
    for (int i = 0; i < quantidade_de_estados; i++) {
        if (strcmp(estados[i], nome) == 0) return i;
    }
    return -1;
}

int indice_simbolo(char simbolo, int limite_procura) {
    for (int i = 0; i < limite_procura; i++) {
        if (alfabeto[i] == simbolo) return i;
    }
    return -1;
}

// --- FECHO LAMBDA (AFN) ---
void fecho_lambda(int estados_ativos[], int indice_lambda) {
    if (indice_lambda == -1) return;
    int mudou = 1;
    while (mudou) {
        mudou = 0;
        for (int i = 0; i < quantidade_de_estados; i++) {
            if (estados_ativos[i]) {
                for (int j = 0; j < quantidade_de_estados; j++) {
                    if (transicoes_af[i][indice_lambda][j] == 1 && estados_ativos[j] == 0) {
                        estados_ativos[j] = 1;
                        mudou = 1;
                    }
                }
            }
        }
    }
}

// --- FUNÇÃO PRINCIPAL DE PROCESSAMENTO ---
void processar_arquivo(const char *nome_arquivo) {
    char linha[256];
    int modo_mt_all = 0; // 0 = AF, 1 = MT, 2 = ALL

    FILE *arquivo = fopen(nome_arquivo, "r");
    if (arquivo == NULL) {
        printf("AVISO: Nao foi possivel abrir o arquivo '%s'\n\n", nome_arquivo);
        return;
    }

    printf("=== EMULANDO ARQUIVO: %s ===\n", nome_arquivo);

    // --- RESET COMPLETO DAS VARIÁVEIS GLOBAIS (Crucial para não misturar os arquivos) ---
    quantidade_de_estados = 0;
    tamanho_alfabeto = 0;
    for (int i = 0; i < maximo_estados; i++) {
        finais[i] = 0;
        estados_iniciais[i] = 0;
        for (int j = 0; j < maximo_alfabeto; j++) {
            transicoes_mt[i][j].definida = 0;
            for (int k = 0; k < maximo_estados; k++) transicoes_af[i][j][k] = 0;
        }
    }

    // Configuração inicial padrão do alfabeto com lambda
    alfabeto[tamanho_alfabeto] = '\\';
    int indice_lambda = tamanho_alfabeto++;

    // --- LEITURA DO ARQUIVO (Cabeçalho Dinâmico e Transições) ---
    while (fgets(linha, sizeof(linha), arquivo)) {
        linha[strcspn(linha, "\r\n")] = '\0';
        if (strlen(linha) == 0) continue;
        if (strncmp(linha, "---", 3) == 0) break; // Fim do autômato

        // Identificação do Tipo
        if (strncmp(linha, "@MT", 3) == 0) { modo_mt_all = 1; }
        else if (strncmp(linha, "@ALL", 4) == 0) { modo_mt_all = 2; }
        else if (strncmp(linha, "@AF", 3) == 0) { modo_mt_all = 0; }
        
        // Definição de Estados (Q:)
        else if (strncmp(linha, "Q:", 2) == 0) {
            char *token = strtok(linha + 2, " ");
            while (token != NULL) {
                strcpy(estados[quantidade_de_estados++], token);
                token = strtok(NULL, " ");
            }
        } 
        // Definição de Alfabeto de Entrada (S:)
        else if (strncmp(linha, "S:", 2) == 0) {
            tamanho_alfabeto = 0;
            for (int i = 2; linha[i] != '\0'; i++) {
                if (linha[i] != ' ') alfabeto[tamanho_alfabeto++] = linha[i];
            }
            alfabeto[tamanho_alfabeto] = '\\';
            indice_lambda = tamanho_alfabeto++;
        } 
        // Alfabeto da Fita (G:)
        else if (strncmp(linha, "G:", 2) == 0) { continue; }
        
        // Estados Iniciais (I:)
        else if (strncmp(linha, "I:", 2) == 0) {
            char *token = strtok(linha + 3, " ");
            while (token != NULL) {
                int idx = buscar_estado(token);
                if (idx != -1) estados_iniciais[idx] = 1;
                token = strtok(NULL, " ");
            }
        } 
        // Estados Finais (F:)
        else if (strncmp(linha, "F:", 2) == 0) {
            char *token = strtok(linha + 3, " ");
            while (token != NULL) {
                int idx = buscar_estado(token);
                if (idx != -1) finais[idx] = 1;
                token = strtok(NULL, " ");
            }
        } 
        // Processamento das Linhas de Transição
        else {
            char origem[8], destino[8];
            char *seta = strstr(linha, "->");
            char *barra = strstr(linha, "|");
            if (seta == NULL || barra == NULL) continue;

            sscanf(linha, "%7s", origem);
            sscanf(seta + 2, "%7s", destino);
            int idx_origem = buscar_estado(origem);
            int idx_destino = buscar_estado(destino);

            if (idx_origem != -1 && idx_destino != -1) {
                char simbolos[128];
                strcpy(simbolos, barra + 1);
                char *token = strtok(simbolos, " \r\n");
                
                while (token != NULL) {
                    if (modo_mt_all > 0) {
                        if (strlen(token) >= 4 && token[1] == '/') {
                            char lido = token[0];
                            char escreve = token[2];
                            char direcao = token[3];
                            transicoes_mt[idx_origem][(int)lido].destino = idx_destino;
                            transicoes_mt[idx_origem][(int)lido].escreve = escreve;
                            transicoes_mt[idx_origem][(int)lido].direcao = direcao;
                            transicoes_mt[idx_origem][(int)lido].definida = 1;
                        }
                    } else {
                        int idx_simb = indice_simbolo(token[0], tamanho_alfabeto);
                        if (idx_simb != -1) transicoes_af[idx_origem][idx_simb][idx_destino] = 1;
                    }
                    token = strtok(NULL, " \r\n");
                }
            }
        }
    }

    // --- PROCESSAMENTO DOS CASOS DE TESTE ---
    if (modo_mt_all > 0) {
        // --- MODO MÁQUINA DE TURING / ALL ---
        while (fgets(linha, sizeof(linha), arquivo)) {
            linha[strcspn(linha, "\r\n")] = '\0';
            if (strlen(linha) == 0 && feof(arquivo)) continue;

            char fita[5000];
            memset(fita, '_', sizeof(fita)); 
            fita[sizeof(fita) - 1] = '\0';

            fita[0] = '<'; 
            int tam_palavra = strlen(linha);
            if (tam_palavra > 0) strncpy(&fita[1], linha, tam_palavra);
            if (modo_mt_all == 2) fita[1 + tam_palavra] = '>'; 

            int cabecote = 1; 
            int estado_atual = -1;
            for (int i = 0; i < quantidade_de_estados; i++) {
                if (estados_iniciais[i]) { estado_atual = i; break; }
            }

            int passos = 0;
            int executando = (estado_atual != -1);
            int aceito = 0;

            while (executando) {
                passos++;
                if (passos > 10000) break; 
                if (cabecote < 0 || cabecote >= 5000) break; 

                char lido = fita[cabecote];
                TransicaoMT t = transicoes_mt[estado_atual][(int)lido];

                if (t.definida) {
                    fita[cabecote] = t.escreve;
                    estado_atual = t.destino;
                    if (t.direcao == 'D' || t.direcao == 'd') cabecote++;
                    else if (t.direcao == 'E' || t.direcao == 'e') cabecote--;
                } else {
                    if (finais[estado_atual]) aceito = 1; 
                    executando = 0;
                }
            }

            int ultimo_nao_vazio = 0;
            for (int i = sizeof(fita) - 2; i >= 0; i--) {
                if (fita[i] != '_') { ultimo_nao_vazio = i; break; }
            }

            if (aceito) printf("OK "); else printf("X ");
            for (int i = 0; i <= ultimo_nao_vazio; i++) printf("%c", fita[i]);
            printf("\n");
        }
    } else {
        // --- MODO AUTÔMATO FINITO (AF) ---
        while (fgets(linha, sizeof(linha), arquivo)) {
            linha[strcspn(linha, "\r\n")] = '\0';
            if (strlen(linha) == 0 && feof(arquivo)) continue;

            int estados_atuais[100];
            for (int i = 0; i < quantidade_de_estados; i++) estados_atuais[i] = estados_iniciais[i];

            fecho_lambda(estados_atuais, indice_lambda);
            int rejeitada = 0;

            for (int i = 0; linha[i] != '\0'; i++) {
                int indice = indice_simbolo(linha[i], tamanho_alfabeto - 1); 
                if (indice == -1) { rejeitada = 1; break; }

                int proximos_estados[100] = {0};
                for (int e = 0; e < quantidade_de_estados; e++) {
                    if (estados_atuais[e]) {
                        for (int dest = 0; dest < quantidade_de_estados; dest++) {
                            if (transicoes_af[e][indice][dest] == 1) proximos_estados[dest] = 1;
                        }
                    }
                }
                for (int e = 0; e < quantidade_de_estados; e++) estados_atuais[e] = proximos_estados[e];
                fecho_lambda(estados_atuais, indice_lambda);
            }

            int aceito = 0;
            if (!rejeitada) {
                for (int i = 0; i < quantidade_de_estados; i++) {
                    if (estados_atuais[i] && finais[i]) { aceito = 1; break; }
                }
            }
            if (aceito) printf("OK\n"); else printf("X\n");
        }
    }

    fclose(arquivo);
    printf("\n"); // Quebra de linha entre arquivos
}

// --- MAIN ENXUTA ---
int main() {
    // Roda o primeiro arquivo (ex: configurado como Máquina de Turing)
    processar_arquivo("entrada1.txt");

    // Roda o segundo arquivo (ex: configurado como Autômato Linearmente Limitado)
    processar_arquivo("entrada2.txt");

    return 0;
}