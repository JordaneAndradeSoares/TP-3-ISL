#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int maximo_estados = 100;
const int maximo_linha = 256;
const int maximo_alfabeto = 128;

//  ESTRUTURAS GLOBAIS 
char estados[100][8];
char alfabeto[128];
int finais[100];
int estados_iniciais[100];
int quantidade_de_estados = 0, tamanho_alfabeto = 0;

// Matrizes para o Autómato Finito (AF)
int transicoes_af[100][128][100];

// Estruturas para a Máquina de Turing / ALL
typedef struct {
    int destino;
    char escreve;
    char direcao; // 'D' (direita) ou 'E' (esquerda)
    int definida;
} TransicaoMT;
TransicaoMT transicoes_mt[100][128]; 

// Estruturas para o Autômato de Pilha (AP)
typedef struct {
    int destino;
    char lido;
    char desempilha;
    char empilha[32];
    int definida;
} TransicaoAP;

TransicaoAP transicoes_ap[100][100]; // Até 100 transições por estado

int qtd_transicoes_ap[100];

//  FUNÇÕES DE BUSCA 
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

//  FECHO LAMBDA (AFN) 
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

//  SIMULADOR RECURSIVO DO AUTÔMATO DE PILHA (AP) 
int simular_ap(int estado, int idx_input, const char *input, char *pilha, int topo, int passos) {
    if (passos > 1000) return 0; // Proteção contra loops infinitos de lambda (\)

    // Critério de aceitação do PDF: palavra toda lida E pilha vazia
    if (input[idx_input] == '\0' && topo == 0) {
        return 1; 
    }

    for (int i = 0; i < qtd_transicoes_ap[estado]; i++) {
        TransicaoAP t = transicoes_ap[estado][i];

        int cond_input = (t.lido == '\\') || (input[idx_input] != '\0' && input[idx_input] == t.lido);
        int cond_pilha = (t.desempilha == '\\') || (topo > 0 && pilha[topo - 1] == t.desempilha);

        if (cond_input && cond_pilha) {
            char nova_pilha[1000];
            memcpy(nova_pilha, pilha, topo);
            int novo_topo = topo;

            if (t.desempilha != '\\') {
                novo_topo--;
            }

            if (strcmp(t.empilha, "\\") != 0) {
                int len = strlen(t.empilha);
                for (int j = len - 1; j >= 0; j--) {
                    if (novo_topo < 1000) {
                        nova_pilha[novo_topo++] = t.empilha[j];
                    }
                }
            }

            int proximo_idx = idx_input;
            if (t.lido != '\\') {
                proximo_idx++;
            }

            if (simular_ap(t.destino, proximo_idx, input, nova_pilha, novo_topo, passos + 1)) {
                return 1; 
            }
        }
    }
    return 0; 
}

//  FUNÇÃO PRINCIPAL DE PROCESSAMENTO (IMPLEMENTA O EXTRA 5) 
void processar_arquivo(const char *nome_arquivo) {
    char linha[256];
    int modo_automato = -1; // -1 = Indefinido, 0 = AF, 1 = MT, 2 = ALL, 3 = AP

    FILE *arquivo = fopen(nome_arquivo, "r");
    if (arquivo == NULL) {
        printf("AVISO: Nao foi possivel abrir o arquivo '%s'\n\n", nome_arquivo);
        return;
    }

    printf(" LENDO ARQUIVO: %s \n", nome_arquivo);

    //  RESET COMPLETO DAS VARIÁVEIS GLOBAIS 
    quantidade_de_estados = 0;
    tamanho_alfabeto = 0;
    for (int i = 0; i < maximo_estados; i++) {
        finais[i] = 0;
        estados_iniciais[i] = 0;
        qtd_transicoes_ap[i] = 0;
        for (int j = 0; j < maximo_alfabeto; j++) {
            transicoes_mt[i][j].definida = 0;
            for (int k = 0; k < maximo_estados; k++) transicoes_af[i][j][k] = 0;
        }
    }

    // Configuração inicial padrão do alfabeto com lambda
    alfabeto[tamanho_alfabeto] = '\\';
    int indice_lambda = tamanho_alfabeto++;

    //  LEITURA DO HEADER @TIPO (Exigência do Extra 5) 
    if (fgets(linha, sizeof(linha), arquivo)) {
        linha[strcspn(linha, "\r\n")] = '\0';
        
        if (strncmp(linha, "@AF", 3) == 0) { modo_automato = 0; printf("Tipo detetado: Automato Finito (AF)\n"); }
        else if (strncmp(linha, "@MT", 3) == 0) { modo_automato = 1; printf("Tipo detetado: Maquina de Turing (MT)\n"); }
        else if (strncmp(linha, "@ALL", 4) == 0) { modo_automato = 2; printf("Tipo detetado: Automato Linearmente Limitado (ALL)\n"); }
        else if (strncmp(linha, "@AP", 3) == 0) { modo_automato = 3; printf("Tipo detetado: Automato de Pilha (AP)\n"); }
        else {
            printf("ERRO: Tipo invalido ou cabecalho '@TIPO' ausente na primeira linha!\n");
            fclose(arquivo);
            return;
        }
    }

    //  LEITURA DO RESTANTE DA CONFIGURAÇÃO DO AUTOMATO 
    while (fgets(linha, sizeof(linha), arquivo)) {
        linha[strcspn(linha, "\r\n")] = '\0';
        if (strlen(linha) == 0) continue;
        if (strncmp(linha, "---", 3) == 0) break; 
        
        // Definição de Estados (Q:)
        if (strncmp(linha, "Q:", 2) == 0) {
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
        // Alfabeto da Fita / Pilha (G:)
        else if (strncmp(linha, "G:", 2) == 0) { continue; }
        
        // Estados Iniciais (I:)
        else if (strncmp(linha, "I:", 2) == 0) {
            char *token = strtok(linha + 2, " "); // Ajustado para "I: "
            while (token != NULL) {
                int idx = buscar_estado(token);
                if (idx != -1) estados_iniciais[idx] = 1;
                token = strtok(NULL, " ");
            }
        } 

        // Estados Finais (F:)
        else if (strncmp(linha, "F:", 2) == 0) {
            char *token = strtok(linha + 2, " "); // Ajustado para "F: "
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
                    if (modo_automato == 1 || modo_automato == 2) {
                        if (strlen(token) >= 4 && token[1] == '/') {
                            char lido = token[0];
                            char escreve = token[2];
                            char direcao = token[3];
                            transicoes_mt[idx_origem][(int)lido].destino = idx_destino;
                            transicoes_mt[idx_origem][(int)lido].escreve = escreve;
                            transicoes_mt[idx_origem][(int)lido].direcao = direcao;
                            transicoes_mt[idx_origem][(int)lido].definida = 1;
                        }
                    } 
                    else if (modo_automato == 3) {
                        char *virgula = strchr(token, ',');
                        char *barra_trans = strchr(token, '/');
                        if (virgula && barra_trans) {
                            *virgula = '\0';
                            *barra_trans = '\0';

                            char lido = token[0];
                            char desempilha = (virgula + 1)[0];
                            char empilha[32];
                            strcpy(empilha, barra_trans + 1);

                            *virgula = ',';
                            *barra_trans = '/';

                            int idx = qtd_transicoes_ap[idx_origem];
                            if (idx < 100) {
                                transicoes_ap[idx_origem][idx].destino = idx_destino;
                                transicoes_ap[idx_origem][idx].lido = lido;
                                transicoes_ap[idx_origem][idx].desempilha = desempilha;
                                strcpy(transicoes_ap[idx_origem][idx].empilha, empilha);
                                transicoes_ap[idx_origem][idx].definida = 1;
                                qtd_transicoes_ap[idx_origem]++;
                            }
                        }
                    }
                    else {
                        int idx_simb = indice_simbolo(token[0], tamanho_alfabeto);
                        if (idx_simb != -1) transicoes_af[idx_origem][idx_simb][idx_destino] = 1;
                    }
                    token = strtok(NULL, " \r\n");
                }
            }
        }
    }

    //  PROCESSAMENTO DOS CASOS DE TESTE 

    printf("Resultados:\n");
    if (modo_automato == 1 || modo_automato == 2) {

        // MODO MÁQUINA DE TURING / ALL 
        while (fgets(linha, sizeof(linha), arquivo)) {
            linha[strcspn(linha, "\r\n")] = '\0';
            if (strlen(linha) == 0 && feof(arquivo)) continue;

            char fita[5000];
            memset(fita, '_', sizeof(fita)); 
            fita[sizeof(fita) - 1] = '\0';

            fita[0] = '<'; 
            int tam_palavra = strlen(linha);
            if (tam_palavra > 0) strncpy(&fita[1], linha, tam_palavra); // Corrigido aqui (linha)
            if (modo_automato == 2) fita[1 + tam_palavra] = '>'; 

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
    } 
    else if (modo_automato == 3) {

        // MODO AUTÔMATO DE PILHA (AP) 
        while (fgets(linha, sizeof(linha), arquivo)) {
            linha[strcspn(linha, "\r\n")] = '\0';
            if (strlen(linha) == 0 && feof(arquivo)) continue;

            int estado_inicial = -1;
            for (int i = 0; i < quantidade_de_estados; i++) {
                if (estados_iniciais[i]) { estado_inicial = i; break; }
            }

            char pilha_inicial[1000] = "";
            int topo_inicial = 0;
            int aceito = 0;

            if (estado_inicial != -1) {
                aceito = simular_ap(estado_inicial, 0, linha, pilha_inicial, topo_inicial, 0);
            }

            if (aceito) printf("OK\n"); else printf("X\n");
        }
    }
    else {

        // MODO AUTÔMATO FINITO (AF) 
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
    printf("\n"); 
}

// função principal (main)
int main() {
    // Exigência do Extra 5: Especificar os formatos que o simulador aceita
    printf("SIMULADOR MULTI-AUTOMATOS UNIFICADO\n");
    printf("Tipos de ficheiro suportados: @AF, @MT, @ALL e @AP\n");

    // Executando os arquivos de teste dinamicamente
    processar_arquivo("entrada1.txt"); // Abre, processa e FECHA
    processar_arquivo("entrada2.txt"); // Abre, processa e FECHA
    processar_arquivo("entrada3.txt"); // Abre, processa e FECHA

    return 0;
}