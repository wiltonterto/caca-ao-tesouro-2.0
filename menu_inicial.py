# Módulo: menu_inicial.py
import pygame
from constantes import * 
from ui_auxiliar import desenhar_texto_centralizado, desenhar_caixa_input
import cores
import recursos
import time 

# --- Funções Auxiliares de UI ---

def get_botoes_config(largura_tela):
    """Retorna as configurações de layout para o menu principal."""
    LARGURA_BOTAO = 190 
    ALTURA_BOTAO = 42   
    ESPACO_VERTICAL = 52
    
    x_start = largura_tela // 2 - LARGURA_BOTAO // 2 
    y_start_base = 314
    
    return [
        {'texto': "MODO PADRÃO", 'modo': MODO_PADRAO, 'retangulo': pygame.Rect(x_start, y_start_base + 0 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
        {'texto': "MELHOR DE 3", 'modo': MODO_MELHOR_DE_3, 'retangulo': pygame.Rect(x_start, y_start_base + 1 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
        {'texto': "MORTE SÚBITA", 'modo': MODO_MORTE_SUBITA, 'retangulo': pygame.Rect(x_start, y_start_base + 2 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
        {'texto': "AJUSTES", 'modo': MODO_AJUSTES, 'retangulo': pygame.Rect(x_start, y_start_base + 3 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
        {'texto': "REGRAS", 'modo': MODO_REGRAS, 'retangulo': pygame.Rect(x_start, y_start_base + 4 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
        {'texto': "SAIR", 'modo': MODO_SAIR, 'retangulo': pygame.Rect(x_start, y_start_base + 5 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
    ]

# --- Função da Tela de Regras ---

def tela_de_regras(tela, largura_tela, altura_tela, fonte_botoes, recursos, estado_config):
    
    som_hover = recursos['sons'].get('hover_menu')
    
    try:
        img_regras_1 = pygame.image.load('recursos/regras_jogo.png').convert_alpha()
        img_regras_1 = pygame.transform.scale(img_regras_1, (largura_tela, altura_tela))
        
        img_regras_2 = pygame.image.load('recursos/regras_jogo_1.png').convert_alpha()
        img_regras_2 = pygame.transform.scale(img_regras_2, (largura_tela, altura_tela))
    except pygame.error as e:
        print(f"Erro ao carregar imagens de regras: {e}. Retornando ao menu.")
        return MODO_REGRAS, estado_config['som_ligado'], estado_config['tamanho_tabuleiro'], None 
        
    LARGURA_BOTAO = 190 
    ALTURA_BOTAO = 42
    CENTRO_X = largura_tela // 2
    POS_Y_BOTAO = altura_tela - 90 
    
    botao_acao = pygame.Rect(CENTRO_X - LARGURA_BOTAO // 2, POS_Y_BOTAO, LARGURA_BOTAO, ALTURA_BOTAO)
    
    pagina_atual = 1
    botao_em_hover_anterior = None 
    
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_atual_em_hover = None
        
        if pagina_atual == 1:
            tela.blit(img_regras_1, (0, 0))
            texto_botao = "PRÓXIMO"
        else:
            tela.blit(img_regras_2, (0, 0))
            texto_botao = "VOLTAR AO MENU"
        
        if botao_acao.collidepoint((mouse_x, mouse_y)):
            cor_btn = VERDE_DESTAQUE
            botao_atual_em_hover = botao_acao
        else:
            cor_btn = PRETO_UI

        if estado_config['som_ligado'] and som_hover: 
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                som_hover.play()
        
        desenhar_texto_centralizado(tela, texto_botao, fonte_botoes, cor_btn, botao_acao.centerx, botao_acao.centery)
        botao_em_hover_anterior = botao_atual_em_hover
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None, estado_config['som_ligado'], estado_config['tamanho_tabuleiro'], None 
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_acao.collidepoint(evento.pos):
                    if pagina_atual == 1:
                        pagina_atual = 2
                    else:
                        return MODO_REGRAS, estado_config['som_ligado'], estado_config['tamanho_tabuleiro'], None

        pygame.display.flip()

# --- Função da Tela de Ajustes ---

def tela_de_ajustes(tela, largura_tela, altura_tela, fonte_botoes, recursos, som_ligado_atual, tamanho_atual):
    
    som_hover = recursos['sons'].get('hover_menu')
    img_fundo_ajustes = recursos['fundos']['ajustes']
    
    # Variáveis locais que serão modificadas
    som_ligado = som_ligado_atual
    tamanho_tabuleiro = tamanho_atual
    
    x_center = largura_tela // 2
    x_som = x_center - ESPACO_QUADRADO_PEQUENO * 1.5 
    x_4x4 = x_center - ESPACO_QUADRADO_PEQUENO * 0.5 
    x_5x5 = x_center + ESPACO_QUADRADO_PEQUENO * 0.5
    
    botoes_ajustes = [
        {'texto': "SOM", 'acao': 'som', 'retangulo': pygame.Rect(x_som - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
        {'texto': "4X4", 'acao': '4x4', 'retangulo': pygame.Rect(x_4x4 - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
        {'texto': "5X5", 'acao': '5x5', 'retangulo': pygame.Rect(x_5x5 - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
        {'texto': "VOLTAR", 'acao': 'voltar_ajustes', 'retangulo': pygame.Rect(x_center - 100, altura_tela - 110, 200, 50)},
    ]

    botao_em_hover_anterior = None
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        botao_atual_em_hover = None
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None, som_ligado, tamanho_tabuleiro, None 
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos_clique = evento.pos
                
                for botao in botoes_ajustes:
                    if botao['retangulo'].collidepoint(mouse_pos_clique):
                        acao = botao['acao']
                        
                        if acao == 'som':
                            som_ligado = not som_ligado 
                            
                        elif acao in ["4x4", "5x5"]:
                            tamanho_tabuleiro = acao      
                        
                        elif acao == 'voltar_ajustes':
                             return MODO_AJUSTES, som_ligado, tamanho_tabuleiro, None 

        # --- Lógica de Desenho e Hover ---
        tela.blit(img_fundo_ajustes, (0, 0))
        
        for botao in botoes_ajustes:
            rect = botao['retangulo']
            esta_selecionado = (botao['acao'] == 'som' and som_ligado) or \
                             (botao['acao'] in ["4x4", "5x5"] and tamanho_tabuleiro == botao['acao'])
            
            cor_texto = PRETO_UI 
            if esta_selecionado or rect.collidepoint(mouse_pos):
                cor_texto = VERDE_DESTAQUE 
                botao_atual_em_hover = rect 
            
            desenhar_texto_centralizado(tela, botao['texto'], fonte_botoes, cor_texto, rect.centerx, rect.centery)

        if som_ligado and som_hover: 
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                som_hover.play()

        botao_em_hover_anterior = botao_atual_em_hover
        pygame.display.flip()

# --- Função da Tela de Input de Nomes ---

# Retorna: [Modo, estado_config MODIFICADO, modo_jogo_real]
def tela_input_nomes(tela, largura_tela, altura_tela, fonte_titulo, fonte_botoes, recursos, estado_config, modo_jogo_real):
    
    som_hover = recursos['sons'].get('hover_menu')
    # Tenta carregar a arte customizada, senão usa o fundo do menu
    img_fundo = recursos['fundos'].get('input_nomes', recursos['fundos']['menu']) 
    
    # Variáveis LOCAIS para manipulação
    nome_j1 = estado_config['nome_j1']
    nome_j2 = estado_config['nome_j2']
    som_ligado = estado_config['som_ligado']
    
    input_ativo = 1 # 1 para J1, 2 para J2
    
    x_center = largura_tela // 2
    
    # 🟢 DEFINIÇÃO DOS RETÂNGULOS COM NOVAS CONSTANTES DE LAYOUT
    ret_j1 = pygame.Rect(x_center - LARGURA_INPUT_NOME // 2, Y_INPUT_J1, LARGURA_INPUT_NOME, ALTURA_INPUT_NOME)
    ret_j2 = pygame.Rect(x_center - LARGURA_INPUT_NOME // 2, Y_INPUT_J2, LARGURA_INPUT_NOME, ALTURA_INPUT_NOME)
    ret_iniciar = pygame.Rect(x_center - LARGURA_BOTAO_JOGAR // 2, Y_BOTAO_INICIAR_JOGO, LARGURA_BOTAO_JOGAR, ALTURA_BOTAO_JOGAR)
    
    # Controle do cursor piscando (milisegundos)
    cursor_timer = 0
    cursor_visivel = True
    
    botao_em_hover_anterior = None
    clock = pygame.time.Clock()
    
    while True:
        # Atualiza o timer do cursor
        cursor_timer += clock.tick() / 1000.0
        if cursor_timer > 0.5:
            cursor_visivel = not cursor_visivel
            cursor_timer = 0
            
        mouse_pos = pygame.mouse.get_pos()
        botao_atual_em_hover = None
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # Retorna None e o estado de configuração ATUAL
                return None, estado_config, None 
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if ret_j1.collidepoint(evento.pos):
                    input_ativo = 1
                    cursor_visivel = True
                    cursor_timer = 0
                elif ret_j2.collidepoint(evento.pos):
                    input_ativo = 2
                    cursor_visivel = True
                    cursor_timer = 0
                elif ret_iniciar.collidepoint(evento.pos):
                    if not nome_j1.strip(): nome_j1 = "JOGADOR 1"
                    if not nome_j2.strip(): nome_j2 = "JOGADOR 2"
                    
                    estado_config['nome_j1'] = nome_j1
                    estado_config['nome_j2'] = nome_j2
                    # Retorna o sinal MODO_INICIAR_PARTIDA e o estado de configuração MODIFICADO
                    return MODO_INICIAR_PARTIDA, estado_config, modo_jogo_real
            
            # Lógica de Input de Teclado
            if evento.type == pygame.KEYDOWN:
                # 🟢 Lógica de input separada e correta para J1 e J2
                if input_ativo == 1:
                    if evento.key == pygame.K_RETURN:
                        input_ativo = 2
                        cursor_visivel = True
                        cursor_timer = 0
                    elif evento.key == pygame.K_BACKSPACE:
                        nome_j1 = nome_j1[:-1]
                    elif evento.unicode and len(nome_j1) < 12 and evento.key != pygame.K_RETURN:
                        nome_j1 += evento.unicode.upper()
                elif input_ativo == 2:
                    if evento.key == pygame.K_RETURN:
                        if not nome_j1.strip(): nome_j1 = "JOGADOR 1"
                        if not nome_j2.strip(): nome_j2 = "JOGADOR 2"
                        estado_config['nome_j1'] = nome_j1
                        estado_config['nome_j2'] = nome_j2
                        return MODO_INICIAR_PARTIDA, estado_config, modo_jogo_real
                    elif evento.key == pygame.K_BACKSPACE:
                        nome_j2 = nome_j2[:-1]
                    elif evento.unicode and len(nome_j2) < 12 and evento.key != pygame.K_RETURN:
                        nome_j2 += evento.unicode.upper()
                
                cursor_visivel = True
                cursor_timer = 0


        # --- Lógica de Desenho ---
        tela.blit(img_fundo, (0, 0))
        
        # Desenho do Título
        desenhar_texto_centralizado(tela, "INFORME OS NOMES", fonte_titulo, PRETO_UI, largura_tela // 2, Y_TITULO_INPUT)
        
        # Desenho dos Inputs (Cápsulas)
        # O VERDE_DESTAQUE controla a cor do texto/cursor quando ativo. O PRETO_UI é a cor base do texto.
        
        # JOGADOR 1
        desenhar_caixa_input(tela, ret_j1, nome_j1, fonte_botoes, PRETO_UI, VERDE_DESTAQUE, 
                             cursor_visivel=(input_ativo == 1 and cursor_visivel), ativo=(input_ativo == 1))
        
        # JOGADOR 2
        desenhar_caixa_input(tela, ret_j2, nome_j2, fonte_botoes, PRETO_UI, VERDE_DESTAQUE, 
                             cursor_visivel=(input_ativo == 2 and cursor_visivel), ativo=(input_ativo == 2))

        # Desenho do Botão INICIAR JOGO
        cor_iniciar = VERDE_DESTAQUE if ret_iniciar.collidepoint(mouse_pos) else PRETO_UI
        desenhar_texto_centralizado(tela, "INICIAR JOGO", fonte_botoes, cor_iniciar, ret_iniciar.centerx, ret_iniciar.centery)
        
        if som_ligado and som_hover and ret_iniciar.collidepoint(mouse_pos) and ret_iniciar != botao_em_hover_anterior:
             som_hover.play()
             
        botao_em_hover_anterior = ret_iniciar if ret_iniciar.collidepoint(mouse_pos) else None
        
        pygame.display.flip()

# --- Função Principal do Menu ---

def tela_de_menu(tela, largura_tela, altura_tela, recursos, som_ligado_atual, tamanho_atual):
    
    img_fundo_menu = recursos['fundos']['menu']
    fonte_botoes = recursos['fontes']['botoes']
    fonte_titulo = recursos['fontes']['titulo']
    som_hover = recursos['sons'].get('hover_menu')
    
    botoes_config = get_botoes_config(largura_tela)
    
    # Variáveis LOCAIS de estado de configuração (serão retornadas)
    som_ligado = som_ligado_atual
    tamanho_tabuleiro = tamanho_atual
    modo_jogo_real = None 
    
    botao_em_hover_anterior = None 
    
    while True:
        mouse_pos = pygame.mouse.get_pos() 
        botao_atual_em_hover = None 
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None, som_ligado, tamanho_tabuleiro, None 
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                for botao in botoes_config:
                    if botao['retangulo'].collidepoint((mouse_x, mouse_y)):
                        modo_escolhido = botao['modo']
                        
                        # Se for AJUSTES
                        if modo_escolhido == MODO_AJUSTES:
                            _, som_ligado, tamanho_tabuleiro, _ = tela_de_ajustes(
                                tela, largura_tela, altura_tela, fonte_botoes, recursos, 
                                som_ligado, tamanho_tabuleiro
                            )

                        # Se for REGRAS
                        elif modo_escolhido == MODO_REGRAS:
                            estado_config_temp = {'som_ligado': som_ligado, 'tamanho_tabuleiro': tamanho_tabuleiro}
                            _, som_ligado, tamanho_tabuleiro, _ = tela_de_regras(
                                tela, largura_tela, altura_tela, fonte_botoes, recursos, estado_config_temp
                            )
                            
                        # Se for SAIR
                        elif modo_escolhido == MODO_SAIR:
                            return None, som_ligado, tamanho_tabuleiro, None
                            
                        # Se for um MODO DE JOGO (Prepara para INPUT DE NOMES)
                        elif modo_escolhido in [MODO_PADRAO, MODO_MORTE_SUBITA, MODO_MELHOR_DE_3]:
                            modo_jogo_real = modo_escolhido
                            return MODO_INPUT_NOMES, som_ligado, tamanho_tabuleiro, modo_jogo_real
                            
        # --- Lógica de Desenho ---
        tela.blit(img_fundo_menu, (0, 0))
        
        for botao in botoes_config:
            retangulo = botao['retangulo']
            texto = botao['texto']
            
            if retangulo.collidepoint(mouse_pos):
                cor_texto = VERDE_DESTAQUE 
                botao_atual_em_hover = retangulo
            else:
                cor_texto = PRETO_UI 
            
            desenhar_texto_centralizado(tela, texto, fonte_botoes, cor_texto, retangulo.centerx, retangulo.centery)
        
        if som_ligado and som_hover:
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                som_hover.play()

        botao_em_hover_anterior = botao_atual_em_hover
        
        pygame.display.flip()