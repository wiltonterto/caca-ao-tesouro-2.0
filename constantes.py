# --- Constantes de Modos de Jogo (Movidas de menu_inicial.py) ---
MODO_PADRAO = 'padrao'
MODO_MELHOR_DE_3 = 'melhor_de_3'
MODO_MORTE_SUBITA = 'morte_subita'
MODO_AJUSTES = 'ajustes'  
MODO_REGRAS = 'regras'    
MODO_SAIR = 'sair'        
MODO_RECOMECO = 'recomecar' 

# --- Constantes Visuais do Jogo (Movidas de main.py) ---
LARGURA_TELA = 825 
ALTURA_TELA = 660 
LADO_CELULA = 85 

# Constantes de Conteúdo do Tabuleiro
NUM_TESOUROS = 6 
NUM_BURACOS = 3 
NUM_BURACOS_MORTE = 1
RODADAS_TOTAL = 3 

# --- Constantes Visuais Específicas do Menu (Movidas de menu_inicial.py) ---
PRETO_UI = (0, 0, 0) 
VERDE_DESTAQUE = (144, 238, 144) # Usado para hover no menu e indicador de vez no jogo
COR_TITULO = (30, 30, 30) 
CINZA_CLARO = (220, 220, 220) 

# Ajustes de Layout (Proporcionais a 825x660)
LARGURA_QUADRADO = 142 
ALTURA_QUADRADO = 142 
ESPACO_QUADRADO = 200 
Y_BOTOES_AJUSTES = 265 

# Cores de Estado
COR_BOTAO_LIGADO = VERDE_DESTAQUE
COR_BOTAO_DESLIGADO = CINZA_CLARO

# Botões de Fim de Jogo
LARGURA_BOTAO_FIM = 250
ALTURA_BOTAO_FIM = 50
Y_NOVA_RODADA = ALTURA_TELA // 2 + 170 
Y_VOLTAR_MENU = ALTURA_TELA // 2 + 238