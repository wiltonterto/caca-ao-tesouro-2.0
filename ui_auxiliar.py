import pygame
import cores
from constantes import LARGURA_TELA, ALTURA_TELA, VERDE_DESTAQUE, PRETO_UI, Y_NOVA_RODADA, Y_VOLTAR_MENU

def desenhar_texto_centralizado(tela, texto, fonte, cor, centro_x, centro_y):
    """Função auxiliar para desenhar texto de forma simplificada."""
    texto_render = fonte.render(texto, True, cor)
    retangulo_texto = texto_render.get_rect(center=(centro_x, centro_y))
    tela.blit(texto_render, retangulo_texto)


def desenhar_tela_fim_jogo(tela, img_fundo, mensagem, fonte_titulo, fonte_botoes, 
                           btn_nova_rodada, btn_voltar, msg_btn_1, msg_btn_2):
    """Desenha a tela de Game Over/Transição com botões com efeito hover."""
    tela.blit(img_fundo, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # 1. Desenha o título (Mensagem Central)
    # Lógica para quebra de linha de mensagens longas (Modo Morte Súbita)
    if '!' in mensagem and '(' in mensagem and ')' in mensagem:
        partes = mensagem.split('!', 1) 
        texto_linha_1 = partes[0].strip() + "!" 
        texto_linha_2 = partes[1].strip() if len(partes) > 1 else ""

        y_base = ALTURA_TELA / 2 - 50 
        offset_quebra = 30 
        
        desenhar_texto_centralizado(tela, texto_linha_1, fonte_titulo, PRETO_UI, 
                                    LARGURA_TELA / 2, y_base - offset_quebra/2)
                                    
        desenhar_texto_centralizado(tela, texto_linha_2, fonte_titulo, PRETO_UI, 
                                    LARGURA_TELA / 2, y_base + offset_quebra/2)
                                    
    else:
        # Mensagem padrão (EMPATE!/Próxima Rodada)
        desenhar_texto_centralizado(tela, mensagem, fonte_titulo, PRETO_UI, 
                                    LARGURA_TELA / 2, ALTURA_TELA / 2 - 50)

    # 2. Botão 1 (Nova Rodada / Novo Jogo)
    cor_btn_1 = VERDE_DESTAQUE if btn_nova_rodada.collidepoint((mouse_x, mouse_y)) else PRETO_UI
    desenhar_texto_centralizado(tela, msg_btn_1, fonte_botoes, cor_btn_1, 
                                btn_nova_rodada.centerx, btn_nova_rodada.centery)

    # 3. Botão 2 (Voltar ao Menu)
    cor_btn_2 = VERDE_DESTAQUE if btn_voltar.collidepoint((mouse_x, mouse_y)) else PRETO_UI
    desenhar_texto_centralizado(tela, msg_btn_2, fonte_botoes, cor_btn_2, 
                                btn_voltar.centerx, btn_voltar.centery)