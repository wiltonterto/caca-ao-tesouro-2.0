import random
import pygame
from constantes import LADO_CELULA

def inicializar_tabuleiro(linhas, colunas, num_tesouros, num_buracos):
    """
    Cria o tabuleiro do jogo, distribui os tesouros ('T') e buracos ('B'),
    e calcula os números das casas vizinhas (sendo o número o contador de tesouros vizinhos).
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

    # 3. Calcula os números para as casas restantes (Tesouros vizinhos)
    for l in range(linhas):
        for c in range(colunas):
            if tabuleiro[l][c] == 0:
                vizinhos = 0
                
                # Checa os 8 vizinhos (incluindo diagonais) para maior realismo/desafio
                for dl in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dl == 0 and dc == 0:
                            continue  # Ignora a própria célula
                        
                        vizinho_l, vizinho_c = l + dl, c + dc

                        if (0 <= vizinho_l < linhas and 
                            0 <= vizinho_c < colunas and 
                            tabuleiro[vizinho_l][vizinho_c] == 'T'):
                            vizinhos += 1
                
                # O número na célula é a contagem de tesouros vizinhos
                tabuleiro[l][c] = str(vizinhos)
    
    return tabuleiro


def desenhar_tabuleiro(tela, tabuleiro_visivel, tabuleiro_solucao, recursos, offset_x, offset_y):
    """Desenha o estado atual do tabuleiro na tela usando as imagens carregadas."""
    
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
                    # É um número ou célula vazia ('0')
                    if conteudo in img_numeros:
                        tela.blit(img_numeros[conteudo], (x, y))
            else:
                # Célula fechada
                tela.blit(img_celula_fechada, (x, y))