import pygame
import random
import config 
import cores
import menu_inicial
import recursos
import tabuleiro
from ui_auxiliar import desenhar_texto_centralizado, desenhar_tela_fim_jogo
from constantes import * # Importa todas as constantes (MODO_PADRAO, LARGURA_TELA, etc.)

# --- Funções Auxiliares de Estado (Fora do main() para melhor escopo) ---

def resetar_jogo_completo(modo_jogo_atual):
    """Reinicia o estado completo do jogo, incluindo o tamanho do tabuleiro se alterado."""
    
    # 1. Recalcula o tabuleiro (usa o config.py, que é modificado no menu)
    NUM_LINHAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][0] 
    NUM_COLUNAS = config.MAPA_TAMANHOS[config.TAMANHO_TABULEIRO][1] 
    total_celulas = NUM_LINHAS * NUM_COLUNAS
    
    # 2. Define a quantidade de buracos
    num_buracos_rodada = NUM_BURACOS
    if modo_jogo_atual == MODO_MORTE_SUBITA:
        num_buracos_rodada = NUM_BURACOS_MORTE
        
    # 3. Cria o tabuleiro (solução e visível)
    tabuleiro_solucao = tabuleiro.inicializar_tabuleiro(NUM_LINHAS, NUM_COLUNAS, NUM_TESOUROS, num_buracos_rodada)
    tabuleiro_visivel = [[False for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)]
    
    # 4. Retorna o novo estado
    return {
        'pontos_j1': 0, 'pontos_j2': 0, 'vitorias_j1': 0, 'vitorias_j2': 0,
        'jogador_da_vez': 1,
        'celulas_reveladas': 0,
        'rodada_atual': 1,
        'jogo_ativo': True,
        'fim_de_jogo': False, 'fim_da_rodada': False,
        'mensagem_final': "", 'mensagem_rodada': "",
        'tabuleiro_solucao': tabuleiro_solucao,
        'tabuleiro_visivel': tabuleiro_visivel,
        'NUM_LINHAS': NUM_LINHAS,
        'NUM_COLUNAS': NUM_COLUNAS,
        'total_celulas': total_celulas,
        'num_buracos_rodada': num_buracos_rodada
    }


# --------------------------------------------------------------------------------------
# --- FUNÇÃO PRINCIPAL ---
# --------------------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.mixer.init() 
    
    # --- 1. Inicialização e Carregamento de Recursos ---
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Caça ao Tesouro")
    
    RECURSOS = recursos.carregar_recursos()
    
    # Chamada inicial ao menu (obtem o modo de jogo)
    modo_jogo = menu_inicial.tela_de_menu(tela, LARGURA_TELA, ALTURA_TELA, RECURSOS)

    if modo_jogo is None or modo_jogo == MODO_SAIR:
        pygame.quit()
        return

    # Extrai recursos
    fonte_titulo = RECURSOS['fontes']['titulo']
    fonte_botoes = RECURSOS['fontes']['botoes']
    fonte_placar = RECURSOS['fontes']['placar']
    IMG_FUNDO_JOGO = RECURSOS['fundos']['jogo']
    IMG_GAME_OVER = RECURSOS['fundos']['game_over']
    
    # 2. Inicializa o estado do jogo (primeiro jogo)
    estado = resetar_jogo_completo(modo_jogo)
    
    # --- Funções Auxiliares de Fluxo de Jogo (Dentro do main para acessar 'estado' e 'modo_jogo') ---

    def ir_para_menu():
        nonlocal modo_jogo, estado
        # Acessa as constantes globais importadas (LARGURA_TELA, ALTURA_TELA)
        novo_modo = menu_inicial.tela_de_menu(
            tela, LARGURA_TELA, ALTURA_TELA, RECURSOS
        )
        
        if novo_modo is None or novo_modo == MODO_SAIR:
            estado['jogo_ativo'] = False
            return True # Sinaliza que saiu
        
        # Se voltou do menu, atualiza o modo de jogo e reseta o estado
        modo_jogo = novo_modo
        estado = resetar_jogo_completo(modo_jogo)
        return False # Sinaliza que não saiu, apenas resetou

    def resetar_rodada():
        estado['tabuleiro_solucao'] = tabuleiro.inicializar_tabuleiro(estado['NUM_LINHAS'], estado['NUM_COLUNAS'], NUM_TESOUROS, NUM_BURACOS)
        estado['tabuleiro_visivel'] = [[False for _ in range(estado['NUM_COLUNAS'])] for _ in range(estado['NUM_LINHAS'])] 
        estado['celulas_reveladas'] = 0 
        estado['pontos_j1'] = 0 
        estado['pontos_j2'] = 0 
        estado['jogador_da_vez'] = 1
        estado['fim_da_rodada'] = False 

    # --- CÁLCULO DE OFFSET E BOTÕES (Após a inicialização do estado) ---
    CENTRO_TELA_X = LARGURA_TELA // 2
    TAMANHO_TABULEIRO = estado['NUM_COLUNAS'] * LADO_CELULA
    OFFSET_X = CENTRO_TELA_X - (TAMANHO_TABULEIRO // 2)
    
    BASE_OFFSET_Y = 200 
    TAMANHO_PADRAO_4X4 = 4 * LADO_CELULA
    OFFSET_Y = BASE_OFFSET_Y - (TAMANHO_TABULEIRO - TAMANHO_PADRAO_4X4) // 2
    
    # Retângulos dos Botões Finais
    botao_nova_rodada = pygame.Rect(CENTRO_TELA_X - LARGURA_BOTAO_FIM // 2, Y_NOVA_RODADA, LARGURA_BOTAO_FIM, ALTURA_BOTAO_FIM)
    botao_voltar_menu = pygame.Rect(CENTRO_TELA_X - LARGURA_BOTAO_FIM // 2, Y_VOLTAR_MENU, LARGURA_BOTAO_FIM, ALTURA_BOTAO_FIM)
    
    # Botão de Saída (Tela de Jogo Ativa)
    X_SAIDA = 90 
    Y_SAIDA = ALTURA_TELA - 88 
    LARGURA_BTN_SAIDA = 150
    ALTURA_BTN_SAIDA = 40
    botao_sair_jogo = pygame.Rect(X_SAIDA, Y_SAIDA, LARGURA_BTN_SAIDA, ALTURA_BTN_SAIDA)

    botao_em_hover_anterior = None # Rastreia o Rect que estava em hover no frame anterior
    
    # --------------------------------------------------------------------------------------
    # --- LOOP PRINCIPAL DO JOGO ---
    # --------------------------------------------------------------------------------------
    
    while estado['jogo_ativo']:
        mouse_pos = pygame.mouse.get_pos()
        botao_atual_em_hover = None 
        
        # --- Tratamento de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado['jogo_ativo'] = False
            
            # Lógica de Botões na Tela de Fim de Jogo ou Fim de Rodada
            if estado['fim_de_jogo'] or estado['fim_da_rodada']:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    
                    # 1. Botão VOLTAR AO MENU (Tela Final)
                    if botao_voltar_menu.collidepoint(evento.pos):
                        if ir_para_menu(): return
                        
                    # 2. Botão NOVA RODADA / NOVO JOGO (Tela Final)
                    elif botao_nova_rodada.collidepoint(evento.pos):
                        
                        if modo_jogo == MODO_MELHOR_DE_3 and estado['fim_da_rodada'] and estado['rodada_atual'] < RODADAS_TOTAL:
                            # Próxima Rodada (Melhor de 3)
                            estado['rodada_atual'] += 1
                            resetar_rodada()
                            
                        elif estado['fim_de_jogo']:
                            # Novo Jogo (Qualquer modo)
                            estado = resetar_jogo_completo(modo_jogo)

                if estado['fim_de_jogo'] or estado['fim_da_rodada']:
                    continue

            # LÓGICA DE CLIQUE DO BOTÃO VOLTAR (Tela de Jogo Ativa)
            if not estado['fim_de_jogo'] and not estado['fim_da_rodada'] and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                if botao_sair_jogo.collidepoint((mouse_x, mouse_y)):
                    if ir_para_menu(): return
                    continue

                # --- Bloco de Clique nas Células do Tabuleiro (Lógica do Jogo) ---
                coluna_clicada = (mouse_x - OFFSET_X) // LADO_CELULA
                linha_clicada = (mouse_y - OFFSET_Y) // LADO_CELULA

                if (0 <= linha_clicada < estado['NUM_LINHAS'] and 
                    0 <= coluna_clicada < estado['NUM_COLUNAS'] and 
                    not estado['tabuleiro_visivel'][linha_clicada][coluna_clicada]):
                    
                    estado['tabuleiro_visivel'][linha_clicada][coluna_clicada] = True
                    conteudo = estado['tabuleiro_solucao'][linha_clicada][coluna_clicada]
                    
                    jogador_atual = estado['jogador_da_vez']

                    if modo_jogo == MODO_MELHOR_DE_3 or modo_jogo == MODO_PADRAO:
                        estado['celulas_reveladas'] += 1
                        
                        # Lógica de Pontuação e Som (Padrão/Melhor de 3)
                        if conteudo == 'T':
                            estado['pontos_j1'] += 100 if jogador_atual == 1 else 0
                            estado['pontos_j2'] += 100 if jogador_atual == 2 else 0
                            recursos.tocar_som('bau', RECURSOS, config.SOM_LIGADO)
                        elif conteudo == 'B':
                            estado['pontos_j1'] = max(0, estado['pontos_j1'] - 50) if jogador_atual == 1 else estado['pontos_j1']
                            estado['pontos_j2'] = max(0, estado['pontos_j2'] - 50) if jogador_atual == 2 else estado['pontos_j2']
                            recursos.tocar_som('buraco', RECURSOS, config.SOM_LIGADO)
                        else:
                            recursos.tocar_som('numero', RECURSOS, config.SOM_LIGADO)

                        # Troca o turno
                        estado['jogador_da_vez'] = 2 if jogador_atual == 1 else 1
                            
                        # --- Verificação de Fim de Rodada/Jogo (MODO PADRÃO/MELHOR DE 3) ---
                        if estado['celulas_reveladas'] == estado['total_celulas']:
                            vencedor_rodada = 0
                            if estado['pontos_j1'] > estado['pontos_j2']: vencedor_rodada = 1
                            elif estado['pontos_j2'] > estado['pontos_j1']: vencedor_rodada = 2
                            
                            if modo_jogo == MODO_MELHOR_DE_3:
                                if vencedor_rodada == 1: estado['vitorias_j1'] += 1
                                elif vencedor_rodada == 2: estado['vitorias_j2'] += 1
                                
                                # Verifica se o jogo ACABOU (melhor de 3)
                                # FIM: 3 Rodadas concluídas OU vencedor antecipado (2 vitórias)
                                if estado['rodada_atual'] == RODADAS_TOTAL or estado['vitorias_j1'] >= 2 or estado['vitorias_j2'] >= 2:
                                    estado['fim_de_jogo'] = True
                                    if estado['vitorias_j1'] > estado['vitorias_j2']: estado['mensagem_final'] = f"JOGADOR 1 VENCEU {estado['vitorias_j1']}x{estado['vitorias_j2']}!"
                                    elif estado['vitorias_j2'] > estado['vitorias_j1']: estado['mensagem_final'] = f"JOGADOR 2 VENCEU {estado['vitorias_j2']}x{estado['vitorias_j1']}!"
                                    else: estado['mensagem_final'] = f"EMPATE GERAL! {estado['vitorias_j1']}x{estado['vitorias_j2']}"
                                    recursos.tocar_som('vitoria', RECURSOS, config.SOM_LIGADO)
                                else:
                                    # Jogo continua: Fim de Rodada, Transição
                                    estado['fim_da_rodada'] = True
                                    if vencedor_rodada > 0: estado['mensagem_rodada'] = f"Rodada {estado['rodada_atual']} | Jogador {vencedor_rodada} VENCEU!"
                                    else: estado['mensagem_rodada'] = f"Rodada {estado['rodada_atual']} | EMPATE!"
                                
                            elif modo_jogo == MODO_PADRAO:
                                estado['fim_de_jogo'] = True
                                if vencedor_rodada == 1: estado['mensagem_final'] = "JOGADOR 1 VENCEU!"
                                elif vencedor_rodada == 2: estado['mensagem_final'] = "JOGADOR 2 VENCEU!"
                                else: estado['mensagem_final'] = "EMPATE!"
                                recursos.tocar_som('vitoria', RECURSOS, config.SOM_LIGADO)
                                
                    # --- LÓGICA DO MODO MORTE SÚBITA ---
                    elif modo_jogo == MODO_MORTE_SUBITA:
                        if conteudo == 'T':
                            estado['pontos_j1'] += 100 if jogador_atual == 1 else 0
                            estado['pontos_j2'] += 100 if jogador_atual == 2 else 0
                            recursos.tocar_som('bau', RECURSOS, config.SOM_LIGADO)
                            estado['jogador_da_vez'] = 2 if jogador_atual == 1 else 1 # Troca o turno

                        elif conteudo == 'B':
                            # Encontrou Buraco: FIM DE JOGO
                            recursos.tocar_som('buraco', RECURSOS, config.SOM_LIGADO)
                            estado['fim_de_jogo'] = True

                            if estado['pontos_j1'] > estado['pontos_j2']: 
                                estado['mensagem_final'] = f"JOGADOR 1 VENCEU! (Buraco encontrado por J{jogador_atual})"
                                recursos.tocar_som('vitoria', RECURSOS, config.SOM_LIGADO)
                            elif estado['pontos_j2'] > estado['pontos_j1']: 
                                estado['mensagem_final'] = f"JOGADOR 2 VENCEU! (Buraco encontrado por J{jogador_atual})"
                                recursos.tocar_som('vitoria', RECURSOS, config.SOM_LIGADO)
                            else:
                                estado['mensagem_final'] = f"EMPATE! (Buraco encontrado por J{jogador_atual})"
                        
                        else: 
                            # Encontrou número ou célula vazia: Turno passa
                            recursos.tocar_som('numero', RECURSOS, config.SOM_LIGADO)
                            estado['jogador_da_vez'] = 2 if jogador_atual == 1 else 1 # Troca o turno


        # --- Lógica de Desenho ---
        tela.blit(IMG_FUNDO_JOGO, (0, 0))
        tabuleiro.desenhar_tabuleiro(tela, estado['tabuleiro_visivel'], estado['tabuleiro_solucao'], 
                                     RECURSOS, OFFSET_X, OFFSET_Y) 

        # 2. Desenho do HUD (Placar e Vez)
        POS_SCORE_J1 = (120, 380) 
        POS_J1_Vez = (165, 105) 
        POS_SCORE_J2 = (695, 380) 
        POS_J2_Vez = (660, 105) 
        
        desenhar_texto_centralizado(tela, f"{estado['pontos_j1']} PTS", fonte_placar, cores.preto, POS_SCORE_J1[0], POS_SCORE_J1[1])
        desenhar_texto_centralizado(tela, f"{estado['pontos_j2']} PTS", fonte_placar, cores.preto, POS_SCORE_J2[0], POS_SCORE_J2[1])

        cor_j1 = VERDE_DESTAQUE if estado['jogador_da_vez'] == 1 and not (estado['fim_de_jogo'] or estado['fim_da_rodada']) else cores.preto
        cor_j2 = VERDE_DESTAQUE if estado['jogador_da_vez'] == 2 and not (estado['fim_de_jogo'] or estado['fim_da_rodada']) else cores.preto

        desenhar_texto_centralizado(tela, "Jogador 1", fonte_botoes, cor_j1, POS_J1_Vez[0], POS_J1_Vez[1])
        desenhar_texto_centralizado(tela, "Jogador 2", fonte_botoes, cor_j2, POS_J2_Vez[0], POS_J2_Vez[1])

        # 3. Desenho do Botão "Voltar ao Menu" (Tela de Jogo Ativa)
        if not estado['fim_de_jogo'] and not estado['fim_da_rodada']:
            cor_btn_saida = VERDE_DESTAQUE if botao_sair_jogo.collidepoint(mouse_pos) else cores.preto
            
            desenhar_texto_centralizado(
                tela, "Voltar ao Menu", fonte_botoes, cor_btn_saida, 
                botao_sair_jogo.centerx, botao_sair_jogo.centery
            )
            
            if botao_sair_jogo.collidepoint(mouse_pos):
                botao_atual_em_hover = botao_sair_jogo

            if config.SOM_LIGADO and RECURSOS['sons'].get('hover_menu'):
                if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                    RECURSOS['sons']['hover_menu'].play()
            
            botao_em_hover_anterior = botao_atual_em_hover
        
        # 4. Desenho das Telas de Transição / Fim
        if estado['fim_de_jogo'] or estado['fim_da_rodada']:
            
            mensagem_a_exibir = estado['mensagem_rodada'] if estado['fim_da_rodada'] else estado['mensagem_final']
            
            if modo_jogo == MODO_MELHOR_DE_3 and estado['fim_da_rodada']:
                msg_btn_1 = "Próxima Rodada"
            else:
                msg_btn_1 = "Novo Jogo"
            
            msg_btn_2 = "Voltar ao Menu"
            
            desenhar_tela_fim_jogo(
                tela, IMG_GAME_OVER, mensagem_a_exibir, 
                fonte_titulo, fonte_botoes, 
                botao_nova_rodada, botao_voltar_menu, 
                msg_btn_1, msg_btn_2
            )
            
            # LÓGICA DE HOVER E SOM DOS BOTÕES FINAIS
            if botao_nova_rodada.collidepoint(mouse_pos):
                botao_atual_em_hover = botao_nova_rodada
            elif botao_voltar_menu.collidepoint(mouse_pos):
                botao_atual_em_hover = botao_voltar_menu

            if config.SOM_LIGADO and RECURSOS['sons'].get('hover_menu'):
                if botao_atual_em_hover is not None and botao_atual_em_hover != botao_em_hover_anterior:
                    RECURSOS['sons']['hover_menu'].play()

            botao_em_hover_anterior = botao_atual_em_hover
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()