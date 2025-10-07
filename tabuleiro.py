# Módulo: tabuleiro.py
import random
import pygame
from constantes import LADO_CELULA

def inicializar_tabuleiro(linhas, colunas, num_tesouros, num_buracos):
    """
    Cria e retorna o tabuleiro (a solução do mapa).
    A contagem de tesouros vizinhos considera APENAS os 4 vizinhos cardinais.
    """
    tabuleiro = [[0 for _ in range(colunas)] for _ in range(linhas)]

    # 1. Distribui os tesouros ('T')
    tesouros_plantados = 0
    while tesouros_plantados < num_tesouros:
        l = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro[l][c] == 0:
            tabuleiro[l][c] = 'T'
            tesouros_plantados += 1

    # 2. Distribui os buracos ('B')
    buracos_plantados = 0
    while buracos_plantados < num_buracos:
        l = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro[l][c] == 0:
            tabuleiro[l][c] = 'B'
            buracos_plantados += 1

    # 3. Calcula os números (Tesouros vizinhos) - CORREÇÃO: APENAS 4 DIREÇÕES
    for l in range(linhas):
        for c in range(colunas):
            if tabuleiro[l][c] == 0:
                vizinhos = 0
                
                # Definindo os deslocamentos para Cardinais (Cima, Baixo, Esquerda, Direita)
                cardinais = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                
                for dl, dc in cardinais:
                    vizinho_l, vizinho_c = l + dl, c + dc

                    # Checa se o vizinho está dentro dos limites do tabuleiro
                    if (0 <= vizinho_l < linhas and 
                        0 <= vizinho_c < colunas and 
                        tabuleiro[vizinho_l][vizinho_c] == 'T'):
                        vizinhos += 1
                
                tabuleiro[l][c] = str(vizinhos)
    
    return tabuleiro


def desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, recursos, offset_x, offset_y):
    """Desenha o estado atual do tabuleiro na tela."""
    
    img_tesouro = recursos['imagens_tabuleiro']['tesouro']
    img_buraco = recursos['imagens_tabuleiro']['buraco']
    img_celula_fechada = recursos['imagens_tabuleiro']['celula_fechada']
    img_numeros = recursos['imagens_tabuleiro']['numeros']

    for linha in range(len(tabuleiro_visivel)):
        for coluna in range(len(tabuleiro_visivel[0])):
            x = coluna * LADO_CELULA + offset_x 
            y = linha * LADO_CELULA + offset_y

            if tabuleiro_visivel[linha][coluna]:
                # Célula aberta
                conteudo = tabuleiro_solucao[linha][coluna]
                
                if conteudo == 'T':
                    tela.blit(img_tesouro, (x, y))
                elif conteudo == 'B':
                    tela.blit(img_buraco, (x, y))
                else:
                    if conteudo in img_numeros:
                        tela.blit(img_numeros[conteudo], (x, y))
            else:
                # Célula fechada
                tela.blit(img_celula_fechada, (x, y))