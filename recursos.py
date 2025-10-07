import pygame
import os
import cores
from constantes import LARGURA_TELA, ALTURA_TELA, LADO_CELULA, VERDE_DESTAQUE

# Variáveis globais para os recursos carregados
# OBS: O som de hover agora está aqui, não em menu_inicial.py
RECURSOS = {} 
CAMINHO_FONTE = 'recursos/stitch.ttf' 
FONTE_FALLBACK = "Arial" 

def carregar_recursos():
    """Carrega todas as fontes, sons e imagens do jogo e armazena em um dicionário global."""
    
    global RECURSOS

    # 1. Carregamento de Sons
    RECURSOS['sons'] = {}
    try:
        RECURSOS['sons']['bau'] = pygame.mixer.Sound('recursos/som_bau.wav')
        RECURSOS['sons']['buraco'] = pygame.mixer.Sound('recursos/som_buraco.wav')
        RECURSOS['sons']['numero'] = pygame.mixer.Sound('recursos/som_numero.wav')
        RECURSOS['sons']['vitoria'] = pygame.mixer.Sound('recursos/som_vitoria.wav')
        RECURSOS['sons']['hover_menu'] = pygame.mixer.Sound('recursos/som_botao.wav')
    except pygame.error as e:
        print(f"Erro ao carregar um arquivo de som: {e}. O jogo continuará sem som.")
        # Garante que as chaves existam, mesmo que os valores sejam None
        RECURSOS['sons'] = {k: None for k in ['bau', 'buraco', 'numero', 'vitoria', 'hover_menu']}

    # 2. Carregamento de Fontes
    RECURSOS['fontes'] = {}
    try:
        RECURSOS['fontes']['titulo'] = pygame.font.Font(CAMINHO_FONTE, 40)
        RECURSOS['fontes']['botoes'] = pygame.font.Font(CAMINHO_FONTE, 20)
        RECURSOS['fontes']['placar'] = pygame.font.Font(CAMINHO_FONTE, 20)
    except:
        RECURSOS['fontes']['titulo'] = pygame.font.SysFont(FONTE_FALLBACK, 40, bold=True)
        RECURSOS['fontes']['botoes'] = pygame.font.SysFont(FONTE_FALLBACK, 20)
        RECURSOS['fontes']['placar'] = pygame.font.SysFont(FONTE_FALLBACK, 20)

    # 3. Carregamento de Imagens de Fundo (Redimensionamento)
    RECURSOS['fundos'] = {}
    try:
        RECURSOS['fundos']['menu'] = pygame.transform.scale(
            pygame.image.load('recursos/tela_inicial.png').convert(), 
            (LARGURA_TELA, ALTURA_TELA)
        )
        RECURSOS['fundos']['ajustes'] = pygame.transform.scale(
            pygame.image.load('recursos/ajustes.png').convert(), 
            (LARGURA_TELA, ALTURA_TELA)
        )
        RECURSOS['fundos']['jogo'] = pygame.transform.scale(
            pygame.image.load('recursos/fundo_tabuleiro.png').convert(), 
            (LARGURA_TELA, ALTURA_TELA)
        )
        RECURSOS['fundos']['game_over'] = pygame.transform.scale(
            pygame.image.load('recursos/game_over.png').convert_alpha(), 
            (LARGURA_TELA, ALTURA_TELA)
        )
    except pygame.error as e:
        print(f"Erro ao carregar imagem de fundo/game over: {e}.")
        # Fallback de tela branca
        fallback = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        fallback.fill(cores.branco)
        RECURSOS['fundos'] = {k: fallback for k in ['menu', 'ajustes', 'jogo', 'game_over']}

    # 4. Carregamento de Imagens do Tabuleiro (Redimensionamento)
    RECURSOS['imagens_tabuleiro'] = {}
    try:
        RECURSOS['imagens_tabuleiro']['tesouro'] = pygame.transform.scale(pygame.image.load('recursos/tesouro.JPEG'), (LADO_CELULA, LADO_CELULA))
        RECURSOS['imagens_tabuleiro']['buraco'] = pygame.transform.scale(pygame.image.load('recursos/buraco.JPEG'), (LADO_CELULA, LADO_CELULA))
        RECURSOS['imagens_tabuleiro']['celula_fechada'] = pygame.transform.scale(pygame.image.load('recursos/celula_fechada.JPEG'), (LADO_CELULA, LADO_CELULA))

        nomes_numeros = {'0': 'zero', '1': 'um', '2': 'dois', '3': 'tres', '4': 'quatro'}
        RECURSOS['imagens_tabuleiro']['numeros'] = {}
        for numero, nome_arquivo in nomes_numeros.items():
            RECURSOS['imagens_tabuleiro']['numeros'][numero] = pygame.transform.scale(
                pygame.image.load(f'recursos/{nome_arquivo}.JPEG'), (LADO_CELULA, LADO_CELULA)
            )

    except pygame.error as e:
        print(f"Erro ao carregar imagem de tabuleiro: {e}. O jogo pode não funcionar corretamente.")
        # Aqui, o main deve lidar com a falha (você já tinha uma lógica no main para isso)
        
    return RECURSOS

def tocar_som(som_nome, recursos, som_ligado):
    """Função auxiliar para tocar som somente se a opção de som estiver ligada e o som foi carregado."""
    som = recursos['sons'].get(som_nome)
    if som_ligado and som:
        som.play()