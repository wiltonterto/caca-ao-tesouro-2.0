# Módulo: recursos.py
import pygame
from constantes import LARGURA_TELA, ALTURA_TELA, LADO_CELULA
import cores
import os # Importar 'os' é útil, embora não estritamente necessário para este arquivo, para padronização.

RECURSOS = {} 
CAMINHO_FONTE = 'recursos/stitch.ttf' 
FONTE_FALLBACK = "Arial" 

def carregar_recursos():
    """Carrega todas as fontes, sons e imagens do jogo e armazena em um dicionário."""
    
    global RECURSOS

    # 1. Carregamento de Sons
    sons = {}
    try:
        sons['bau'] = pygame.mixer.Sound('recursos/som_bau.wav')
        sons['buraco'] = pygame.mixer.Sound('recursos/som_buraco.wav')
        sons['numero'] = pygame.mixer.Sound('recursos/som_numero.wav')
        sons['vitoria'] = pygame.mixer.Sound('recursos/som_vitoria.wav')
        sons['hover_menu'] = pygame.mixer.Sound('recursos/som_botao.wav')
    except pygame.error as e:
        print(f"Erro ao carregar um arquivo de som: {e}. O jogo continuará sem som.")
        sons = {k: None for k in ['bau', 'buraco', 'numero', 'vitoria', 'hover_menu']}

    # 2. Carregamento de Fontes
    fontes = {}
    try:
        fontes['titulo'] = pygame.font.Font(CAMINHO_FONTE, 40)
        fontes['botoes'] = pygame.font.Font(CAMINHO_FONTE, 20)
        fontes['placar'] = pygame.font.Font(CAMINHO_FONTE, 20)
    except:
        fontes['titulo'] = pygame.font.SysFont(FONTE_FALLBACK, 40, bold=True)
        fontes['botoes'] = pygame.font.SysFont(FONTE_FALLBACK, 20)
        fontes['placar'] = pygame.font.SysFont(FONTE_FALLBACK, 20)

    # 3. Carregamento de Imagens de Fundo
    fundos = {}
    fallback = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    fallback.fill(cores.branco)
    
    try:
        # Nota: Convert_alpha() é geralmente melhor para fundos e UI para garantir transparência
        fundos['menu'] = pygame.transform.scale(pygame.image.load('recursos/tela_inicial.png').convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
        fundos['ajustes'] = pygame.transform.scale(pygame.image.load('recursos/ajustes.png').convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
        fundos['jogo'] = pygame.transform.scale(pygame.image.load('recursos/fundo_tabuleiro.png').convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
        fundos['game_over'] = pygame.transform.scale(pygame.image.load('recursos/game_over.png').convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
        
        # 🟢 CORREÇÃO: Ativa o carregamento da sua nova arte (assumindo o nome 'fundo_input_nomes.png')
        fundos['input_nomes'] = pygame.transform.scale(pygame.image.load('recursos/fundo_input_nomes.png').convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
        
    except pygame.error as e:
        print(f"Erro ao carregar imagem de fundo: {e}.")
        # Garante que todas as chaves tenham um fallback para evitar KeyErrors no loop principal
        fundos = {k: fallback for k in ['menu', 'ajustes', 'jogo', 'game_over', 'input_nomes']} 

    # 4. Carregamento de Imagens do Tabuleiro
    imagens_tabuleiro = {}
    try:
        imagens_tabuleiro['tesouro'] = pygame.transform.scale(pygame.image.load('recursos/tesouro.JPEG'), (LADO_CELULA, LADO_CELULA))
        imagens_tabuleiro['buraco'] = pygame.transform.scale(pygame.image.load('recursos/buraco.JPEG'), (LADO_CELULA, LADO_CELULA))
        imagens_tabuleiro['celula_fechada'] = pygame.transform.scale(pygame.image.load('recursos/celula_fechada.JPEG'), (LADO_CELULA, LADO_CELULA))

        nomes_numeros = {'0': 'zero', '1': 'um', '2': 'dois', '3': 'tres', '4': 'quatro'}
        imagens_tabuleiro['numeros'] = {}
        for numero, nome_arquivo in nomes_numeros.items():
            imagens_tabuleiro['numeros'][numero] = pygame.transform.scale(
                pygame.image.load(f'recursos/{nome_arquivo}.JPEG'), (LADO_CELULA, LADO_CELULA)
            )

    except pygame.error as e:
        print(f"Erro ao carregar imagem de tabuleiro: {e}.")
        # Sem imagens de tabuleiro, o jogo não pode continuar, mas o dicionário existe
        imagens_tabuleiro = {}

    # 5. Carregamento da Música de Fundo (BGM)
    musica = {}
    try:
        musica['menu'] = 'recursos/musica_menu.mp3' 
    except:
        musica['menu'] = None

    return {
        'sons': sons,
        'fontes': fontes,
        'fundos': fundos,
        'imagens_tabuleiro': imagens_tabuleiro,
        'musica': musica
    }

# Esta função PRECISA receber o dicionário de estado para saber se o som está ligado.
def tocar_som(som_nome, recursos, estado_config):
    """Toca um som somente se a opção de som estiver ligada no estado_config."""
    som = recursos['sons'].get(som_nome)
    # 🛑 NOTA: Assumindo que estado_config é o dicionário mestre, e não apenas o som.
    if estado_config.get('som_ligado', False) and som:
        som.play()