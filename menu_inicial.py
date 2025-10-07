import pygame
import config
from constantes import * # Importa todas as constantes de modo e UI
from ui_auxiliar import desenhar_texto_centralizado
from cores import preto # Importa a cor genérica

# A variável de som de hover não é mais global aqui, ela é carregada em recursos.py
# e passada por parâmetro (ou acessada via o objeto de recursos)

# --- Funções Auxiliares de UI (Mantidas por serem exclusivas do Menu) ---

def get_botoes_config(largura_tela):
    """Define as posições e ações de todos os botões do menu."""
    LARGURA_BOTAO = 190 
    ALTURA_BOTAO = 42   
    ESPACO_VERTICAL = 52
    
    x_start = largura_tela // 2 - LARGURA_BOTAO // 2 
    y_start_base = 314
    
    return [
        {'texto': "MODO PADRÃO", 'modo': MODO_PADRAO, 
         'retangulo': pygame.Rect(x_start, y_start_base + 0 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
        
        {'texto': "MELHOR DE 3", 'modo': MODO_MELHOR_DE_3, 
         'retangulo': pygame.Rect(x_start, y_start_base + 1 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
          
        {'texto': "MORTE SÚBITA", 'modo': MODO_MORTE_SUBITA, 
         'retangulo': pygame.Rect(x_start, y_start_base + 2 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},

        {'texto': "AJUSTES", 'modo': MODO_AJUSTES, 
         'retangulo': pygame.Rect(x_start, y_start_base + 3 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},

        {'texto': "REGRAS", 'modo': MODO_REGRAS, 
         'retangulo': pygame.Rect(x_start, y_start_base + 4 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
          
        {'texto': "SAIR", 'modo': MODO_SAIR, 
         'retangulo': pygame.Rect(x_start, y_start_base + 5 * ESPACO_VERTICAL, LARGURA_BOTAO, ALTURA_BOTAO)},
    ]


# --- Função da Tela de Regras ---

def tela_de_regras(tela, largura_tela, altura_tela, fonte_botoes, recursos):
    """
    Mostra a tela de regras em duas páginas com navegação.
    """
    
    som_hover = recursos['sons'].get('hover_menu')

    # 1. Carregamento e Redimensionamento das Imagens (Carregadas via recursos.py)
    try:
        # Assumindo que você tem recursos/regras_jogo.png e regras_jogo_1.png
        img_regras_1 = pygame.image.load('recursos/regras_jogo.png').convert_alpha()
        img_regras_1 = pygame.transform.scale(img_regras_1, (largura_tela, altura_tela))
        
        img_regras_2 = pygame.image.load('recursos/regras_jogo_1.png').convert_alpha()
        img_regras_2 = pygame.transform.scale(img_regras_2, (largura_tela, altura_tela))

    except pygame.error as e:
        print(f"Erro ao carregar imagens de regras: {e}. Verifique os nomes.")
        return MODO_REGRAS
        
    # 2. Definição do Botão
    LARGURA_BOTAO = 190 
    ALTURA_BOTAO = 42
    CENTRO_X = largura_tela // 2
    POS_Y_BOTAO = altura_tela - 90 
    
    botao_acao = pygame.Rect(CENTRO_X - LARGURA_BOTAO // 2, POS_Y_BOTAO, LARGURA_BOTAO, ALTURA_BOTAO)
    
    pagina_atual = 1
    botao_em_hover_anterior = None 
    
    # 3. Loop da Tela de Regras
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        botao_atual_em_hover = None
        
        # Desenha o fundo da página atual
        if pagina_atual == 1:
            tela.blit(img_regras_1, (0, 0))
            texto_botao = "PRÓXIMO"
        else: # página_atual == 2
            tela.blit(img_regras_2, (0, 0))
            texto_botao = "VOLTAR AO MENU"
        
        # Lógica do Botão Hover e Som
        if botao_acao.collidepoint((mouse_x, mouse_y)):
            cor_btn = VERDE_DESTAQUE
            botao_atual_em_hover = botao_acao
        else:
            cor_btn = PRETO_UI

        if config.SOM_LIGADO and som_hover: 
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                som_hover.play()
        
        # Desenha o texto do botão
        desenhar_texto_centralizado(tela, texto_botao, fonte_botoes, cor_btn, botao_acao.centerx, botao_acao.centery)

        # Atualiza o estado de hover
        botao_em_hover_anterior = botao_atual_em_hover
        
        # 4. Tratamento de Eventos (Cliques)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_acao.collidepoint(evento.pos):
                    if pagina_atual == 1:
                        pagina_atual = 2
                    else:
                        # Retorna MODO_REGRAS (que faz o loop do menu continuar)
                        return MODO_REGRAS

        pygame.display.flip()

# --- Função da Tela de Ajustes ---

def tela_de_ajustes(tela, largura_tela, altura_tela, fonte_botoes, recursos):
    
    som_hover = recursos['sons'].get('hover_menu')
    
    x_center = largura_tela // 2
    img_fundo_ajustes = recursos['fundos']['ajustes']
    
    x_som = x_center - ESPACO_QUADRADO 
    x_5x5 = x_center
    x_6x6 = x_center + ESPACO_QUADRADO
    
    botoes_ajustes = [
        {'texto': "SOM", 'acao': 'som', 
         'retangulo': pygame.Rect(x_som - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
        
        {'texto': "5X5", 'acao': '5x5', 
         'retangulo': pygame.Rect(x_5x5 - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
        
        {'texto': "6X6", 'acao': '6x6', 
         'retangulo': pygame.Rect(x_6x6 - LARGURA_QUADRADO // 2, Y_BOTOES_AJUSTES, LARGURA_QUADRADO, ALTURA_QUADRADO)},
    ]
    
    LARGURA_BTN_VOLTAR = 200
    ALTURA_BTN_VOLTAR = 50
    
    botao_voltar = pygame.Rect(x_center - LARGURA_BTN_VOLTAR // 2, altura_tela - 110, LARGURA_BTN_VOLTAR, ALTURA_BTN_VOLTAR)
    
    botao_em_hover_anterior = None
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        botao_atual_em_hover = None 
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos_clique = evento.pos
                
                # Clique no Botão VOLTAR
                if botao_voltar.collidepoint(mouse_pos_clique):
                    return MODO_AJUSTES 
                
                # Lógica de Clique nos Botões de Ajuste
                for botao in botoes_ajustes:
                    if botao['retangulo'].collidepoint(mouse_pos_clique):
                        acao = botao['acao']
                        
                        if acao == 'som':
                            config.SOM_LIGADO = not config.SOM_LIGADO
                            
                        elif acao in ["5x5", "6x6"]:
                            config.TAMANHO_TABULEIRO = acao
                        
        
        # --- Lógica de Desenho ---
        tela.blit(img_fundo_ajustes, (0, 0))
        
        # Desenha os 3 Botões de Ajuste
        for botao in botoes_ajustes:
            rect = botao['retangulo']
            
            # 1. Verifica o estado de SELEÇÃO PERMANENTE 
            esta_selecionado = (botao['acao'] == 'som' and config.SOM_LIGADO) or \
                             (botao['acao'] in ["5x5", "6x6"] and config.TAMANHO_TABULEIRO == botao['acao'])
            
            # 2. Lógica de COR do Texto
            cor_texto = PRETO_UI 
            
            if esta_selecionado:
                cor_texto = VERDE_DESTAQUE
            
            if rect.collidepoint(mouse_pos):
                cor_texto = VERDE_DESTAQUE 
                botao_atual_em_hover = rect # Rastreia o hover
            
            # 3. Desenha o texto do botão
            desenhar_texto_centralizado(tela, botao['texto'], fonte_botoes, cor_texto, rect.centerx, rect.centery)


        # --- Desenha o botão VOLTAR ---
        cor_texto_voltar = PRETO_UI 
        
        if botao_voltar.collidepoint(mouse_pos):
            cor_texto_voltar = VERDE_DESTAQUE
            botao_atual_em_hover = botao_voltar 
            
        desenhar_texto_centralizado(tela, "VOLTAR", fonte_botoes, cor_texto_voltar, botao_voltar.centerx, botao_voltar.centery)
        
        # LÓGICA DO SOM DE HOVER (Centralizada e robusta)
        if config.SOM_LIGADO and som_hover: 
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                som_hover.play()

        botao_em_hover_anterior = botao_atual_em_hover
        
        pygame.display.flip()

# --- Função Principal do Menu ---

def tela_de_menu(tela, largura_tela, altura_tela, recursos):
    """
    Exibe a tela de menu inicial, usa a imagem de fundo e gerencia a seleção de modo de jogo.
    """
    
    img_fundo_menu = recursos['fundos']['menu']
    img_fundo_ajustes = recursos['fundos']['ajustes']
    fonte_botoes = recursos['fontes']['botoes']
    fonte_titulo = recursos['fontes']['titulo']
    som_hover = recursos['sons'].get('hover_menu')
    
    botoes_config = get_botoes_config(largura_tela)
    
    botao_em_hover_anterior = None 
    
    while True:
        mouse_pos = pygame.mouse.get_pos() 
        botao_atual_em_hover = None 
        
        # --- Tratamento de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                # Verifica qual botão foi clicado
                for botao in botoes_config:
                    if botao['retangulo'].collidepoint((mouse_x, mouse_y)):
                        modo_escolhido = botao['modo']

                        if modo_escolhido == MODO_AJUSTES:
                            resultado_ajustes = tela_de_ajustes(
                                tela, largura_tela, altura_tela, 
                                fonte_botoes, recursos
                            )
                            if resultado_ajustes is None:
                                return None
                            
                        elif modo_escolhido == MODO_SAIR:
                            return None 
                            
                        elif modo_escolhido in [MODO_PADRAO, MODO_MORTE_SUBITA, MODO_MELHOR_DE_3]:
                            return modo_escolhido
                            
                        elif modo_escolhido == MODO_REGRAS:
                            resultado_regras = tela_de_regras(tela, largura_tela, altura_tela, fonte_botoes, recursos)
                            
                            if resultado_regras is None:
                                return None 
        
        # --- Lógica de Desenho ---
        tela.blit(img_fundo_menu, (0, 0))
        
        # Desenha os Botões e o Efeito Hover
        for botao in botoes_config:
            retangulo = botao['retangulo']
            texto = botao['texto']
            
            # Define a Cor do Texto (Lógica de HOVER)
            if retangulo.collidepoint(mouse_pos):
                cor_texto = VERDE_DESTAQUE 
                botao_atual_em_hover = retangulo
            else:
                cor_texto = PRETO_UI 
            
            # Desenha o Texto
            desenhar_texto_centralizado(tela, texto, fonte_botoes, cor_texto, retangulo.centerx, retangulo.centery)
        
        # LÓGICA DO SOM DE HOVER
        if config.SOM_LIGADO and som_hover:
            if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                som_hover.play()

        # ATUALIZA o estado para o próximo loop
        botao_em_hover_anterior = botao_atual_em_hover
        
        pygame.display.flip()