# Módulo: ui_auxiliar.py
import pygame
import cores
from constantes import LARGURA_TELA, ALTURA_TELA, VERDE_DESTAQUE, PRETO_UI

def desenhar_texto_centralizado(tela, texto, fonte, cor, centro_x, centro_y):
    """Função auxiliar para desenhar texto de forma simplificada."""
    texto_render = fonte.render(texto, True, cor)
    retangulo_texto = texto_render.get_rect(center=(centro_x, centro_y))
    tela.blit(texto_render, retangulo_texto)


def desenhar_caixa_input(tela, retangulo, texto, fonte, cor_base, cor_borda, cursor_visivel=False, ativo=False):
    """
    Desenha o texto e cursor do input. (Adaptado para o design da sua arte).
    """

    cor_ativa = VERDE_DESTAQUE
    
    # LÓGICA DE TEXTO/PLACEHOLDER:
    if ativo and not texto.strip():
        texto_a_renderizar = "DIGITE O NOME..."
        cor_texto_final = cor_ativa
    elif not texto.strip():
        texto_a_renderizar = "DIGITE O NOME..."
        cor_texto_final = cor_base
    else:
        texto_a_renderizar = texto
        cor_texto_final = cor_ativa if ativo else cor_base
        
    # Desenha o texto
    text_surface = fonte.render(texto_a_renderizar, True, cor_texto_final)
    
    # Centraliza o texto verticalmente e alinha no centro do retângulo
    texto_rect = text_surface.get_rect(center=retangulo.center)
    
    # Ajuste o alinhamento (offset de -50 para centralizar no design da cápsula)
    tela.blit(text_surface, (texto_rect.x - 12, texto_rect.y)) 

    # Desenha o cursor piscando
    if cursor_visivel and ativo:
        cursor_x = texto_rect.x - 12 + text_surface.get_width() + 2 
        
        cursor_rect = pygame.Rect(cursor_x, 
                                  texto_rect.y,
                                  3, fonte.get_height())
        pygame.draw.rect(tela, cor_texto_final, cursor_rect)


def desenhar_tela_fim_jogo(tela, img_fundo, mensagem, fonte_titulo, fonte_botoes, 
                           btn_nova_rodada, btn_voltar, msg_btn_1, msg_btn_2):
    """
    Desenha a tela de Game Over/Transição com botões com efeito hover.
    CORRIGIDO: Implementação da quebra de linha para mensagem final longa.
    """
    tela.blit(img_fundo, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # --- 1. Lógica de Quebra de Linha para Mensagem Longa ---
    
    texto_linha_1 = mensagem
    texto_linha_2 = ""
    
    # Procura um ponto de quebra para mensagens longas (FIM DA PARTIDA! VENCEDOR:...)
    if "VENCEDOR:" in mensagem:
        # Quebra em "Primeira Parte" e "VENCEDOR: Jogador X"
        partes = mensagem.split("VENCEDOR:", 1)
        texto_linha_1 = partes[0].strip() 
        texto_linha_2 = "VENCEDOR: " + partes[1].strip()

    # Define as posições verticais na tela
    CENTRO_Y_CAPSULA = ALTURA_TELA // 2 - 42 
    OFFSET_QUEBRA = 35 # Espaço entre as linhas

    if texto_linha_2:
        # Se quebrado em duas linhas, centraliza no espaço da cápsula
        desenhar_texto_centralizado(tela, texto_linha_1, fonte_titulo, PRETO_UI, 
                                    LARGURA_TELA / 2, CENTRO_Y_CAPSULA - OFFSET_QUEBRA/2)
        desenhar_texto_centralizado(tela, texto_linha_2, fonte_titulo, PRETO_UI, 
                                    LARGURA_TELA / 2, CENTRO_Y_CAPSULA + OFFSET_QUEBRA/2)
    else:
        # Mensagem padrão (para mensagens curtas como EMPATE!)
        desenhar_texto_centralizado(tela, mensagem, fonte_titulo, PRETO_UI, 
                                    LARGURA_TELA / 2, CENTRO_Y_CAPSULA)

    # 2. Botão 1 (Nova Rodada / Novo Jogo)
    cor_btn_1 = VERDE_DESTAQUE if btn_nova_rodada.collidepoint((mouse_x, mouse_y)) else PRETO_UI
    desenhar_texto_centralizado(tela, msg_btn_1, fonte_botoes, cor_btn_1, 
                                btn_nova_rodada.centerx, btn_nova_rodada.centery)

    # 3. Botão 2 (Voltar ao Menu)
    cor_btn_2 = VERDE_DESTAQUE if btn_voltar.collidepoint((mouse_x, mouse_y)) else PRETO_UI
    desenhar_texto_centralizado(tela, msg_btn_2, fonte_botoes, cor_btn_2, 
                                btn_voltar.centerx, btn_voltar.centery)