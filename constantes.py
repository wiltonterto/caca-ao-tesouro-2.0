# Módulo: constantes.py
# Todas as variáveis aqui são CONSTANTES imutáveis

# --- Constantes de Modos de Jogo ---
MODO_PADRAO = 'padrao'
MODO_MELHOR_DE_3 = 'melhor_de_3'
MODO_MORTE_SUBITA = 'morte_subita'
MODO_AJUSTES = 'ajustes'  
MODO_REGRAS = 'regras'    
MODO_SAIR = 'sair'        
MODO_RECOMECO = 'recomecar' 
MODO_INICIAR_PARTIDA = 'iniciar_partida'
MODO_INPUT_NOMES = 'input_nomes' 
MODO_MENU_PRINCIPAL = 'menu_principal' # Novo estado para o loop principal

# --- Constantes Visuais do Jogo ---
LARGURA_TELA = 825 
ALTURA_TELA = 660 
LADO_CELULA = 85 

# Constantes de Conteúdo do Tabuleiro
NUM_TESOUROS = 6 
NUM_BURACOS = 3 
NUM_BURACOS_MORTE = 1
RODADAS_TOTAL = 3 

# Mapeamento do tamanho
MAPA_TAMANHOS = {
    "4x4": (4, 4),
    "5x5": (5, 5) 
}

# --- Constantes Visuais Específicas do Menu ---
PRETO_UI = (0, 0, 0) 
VERDE_DESTAQUE = (0, 128, 0) 
COR_TITULO = (30, 30, 30) 
CINZA_CLARO = (220, 220, 220) 

# Ajustes de Layout dos Botões 4x4, 5x5, Som, etc.
LARGURA_QUADRADO = 142 
ALTURA_QUADRADO = 142 
ESPACO_QUADRADO = 200 
Y_BOTOES_AJUSTES = 265 
ESPACO_QUADRADO_PEQUENO = 150 

# --- UI - Layout da Tela de Input de Nomes (NOVAS CONSTANTES) ---
LARGURA_INPUT_NOME = 450
ALTURA_INPUT_NOME = 60 # Altura da cápsula
ESPACO_VERTICAL_INPUT = 80

# Posição Y dos elementos para a tela de input
Y_TITULO_INPUT = 223                         # Título: "INFORME OS NOMES"
Y_INPUT_J1 = Y_TITULO_INPUT + 110           # Primeira cápsula (JOGADOR 1)
Y_INPUT_J2 = Y_TITULO_INPUT + 200 # Segunda cápsula (JOGADOR 2)

# Botão de Iniciar Jogo
LARGURA_BOTAO_JOGAR = 200
ALTURA_BOTAO_JOGAR = 50
Y_BOTAO_INICIAR_JOGO = Y_TITULO_INPUT + 328

# Botões de Fim de Jogo (M3 e Padrão)
LARGURA_BOTAO_FIM = 250
ALTURA_BOTAO_FIM = 50
Y_NOVA_RODADA = ALTURA_TELA // 2 + 170 
Y_VOLTAR_MENU = ALTURA_TELA // 2 + 238