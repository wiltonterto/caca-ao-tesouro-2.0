import pygame
import random
import recursos
import tabuleiro
import os 
from ui_auxiliar import desenhar_texto_centralizado, desenhar_tela_fim_jogo
from constantes import * 
import cores
import menu_inicial

# Define o número total de rodadas para o Melhor de 3 (assumindo que 3 é a constante RODADAS_TOTAL)
RODADAS_TOTAL = 3 

# --- Estrutura do Dicionário de Estado ---
def inicializar_estado_config_e_jogo(modo_jogo_selecionado, estado_config_existente):
    """
    Cria e retorna o estado completo de configuração e partida.
    Requer o estado_config_existente para obter o tamanho e os nomes.
    """
    
    # 1. Estado de Configuração (Copia os valores existentes)
    estado_config = estado_config_existente.copy()
    
    # 2. Inicializa o Tabuleiro
    linhas, colunas = MAPA_TAMANHOS[estado_config['tamanho_tabuleiro']]
    num_buracos_rodada = NUM_BURACOS
    if modo_jogo_selecionado == MODO_MORTE_SUBITA:
        # Usa a constante correta para o modo Morte Súbita (deve ser 1)
        num_buracos_rodada = NUM_BURACOS_MORTE 
    
    tabuleiro_solucao = tabuleiro.inicializar_tabuleiro(linhas, colunas, NUM_TESOUROS, num_buracos_rodada)
    tabuleiro_visivel = [[False for _ in range(colunas)] for _ in range(linhas)]
    
    # 3. Estado da Partida (Cria as variáveis de jogo)
    estado_partida = {
        'modo_jogo_real': modo_jogo_selecionado,
        'pontos_j1': 0, 
        'pontos_j2': 0, 
        'vitorias_j1': 0,
        'vitorias_j2': 0,
        'jogador_da_vez': 1,
        'celulas_reveladas': 0,
        'rodada_atual': 1,
        'fim_de_jogo': False, 
        'fim_da_rodada': False,
        'mensagem_final': "",
        'mensagem_rodada': "",
        'tabuleiro_solucao': tabuleiro_solucao,
        'tabuleiro_visivel': tabuleiro_visivel,
        'NUM_LINHAS': linhas,
        'NUM_COLUNAS': colunas,
        'total_celulas': linhas * colunas,
        'num_buracos_rodada': num_buracos_rodada
    }
    
    return estado_config, estado_partida

# --------------------------------------------------------------------------------------
# --- FUNÇÃO PRINCIPAL (CONTROLADOR MESTRE) ---
# --------------------------------------------------------------------------------------

def main():
    pygame.init()
    pygame.mixer.init() 
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Caça ao Tesouro")
    
    RECURSOS = recursos.carregar_recursos()
    fonte_titulo = RECURSOS['fontes']['titulo']
    fonte_botoes = RECURSOS['fontes']['botoes']
    fonte_placar = RECURSOS['fontes']['placar']
    IMG_FUNDO_JOGO = RECURSOS['fundos']['jogo']
    IMG_GAME_OVER = RECURSOS['fundos']['game_over']
    
    # --- VARIÁVEIS DO LOOP PRINCIPAL ---
    modo_principal = MODO_MENU_PRINCIPAL
    
    # ESTADOS INICIAIS
    estado_config = {
        'som_ligado': True,
        'tamanho_tabuleiro': '4x4',
        'nome_j1': 'JOGADOR 1',
        'nome_j2': 'JOGADOR 2',
    }
    estado_partida = None 
    modo_jogo_real = None # O modo de jogo selecionado
    
    # --- Inicialização da Música de Fundo (Usa o estado_config) ---
    caminho_bgm = RECURSOS['musica'].get('menu')
    if caminho_bgm and os.path.exists(caminho_bgm): # Importante: verifica se existe
        try:
            pygame.mixer.music.load(caminho_bgm)
            if estado_config['som_ligado']:
                pygame.mixer.music.play(-1) 
        except pygame.error as e:
            print(f"Erro ao carregar música de fundo: {e}")
            
    # --- CÁLCULO DE OFFSET E BOTÕES ---
    CENTRO_TELA_X = LARGURA_TELA // 2
    
    OFFSET_X = 0 
    OFFSET_Y = 0
    BASE_OFFSET_Y = 200 
    TAMANHO_PADRAO_4X4 = 4 * LADO_CELULA

    botao_nova_rodada = pygame.Rect(CENTRO_TELA_X - LARGURA_BOTAO_FIM // 2, Y_NOVA_RODADA, LARGURA_BOTAO_FIM, ALTURA_BOTAO_FIM)
    botao_voltar_menu = pygame.Rect(CENTRO_TELA_X - LARGURA_BOTAO_FIM // 2, Y_VOLTAR_MENU, LARGURA_BOTAO_FIM, ALTURA_BOTAO_FIM)
    botao_sair_jogo = pygame.Rect(90, ALTURA_TELA - 88, 150, 40)
    
    botao_em_hover_anterior = None
    jogo_ativo = True

    # --------------------------------------------------------------------------------------
    # --- LOOP PRINCIPAL DO JOGO/MENU ---
    # --------------------------------------------------------------------------------------
    
    while jogo_ativo:
        
        # === FLUXO: MENU PRINCIPAL / AJUSTES / REGRAS ===
        if modo_principal in [MODO_MENU_PRINCIPAL, MODO_AJUSTES, MODO_REGRAS]:
            
            modo_principal, estado_config['som_ligado'], estado_config['tamanho_tabuleiro'], modo_jogo_real = menu_inicial.tela_de_menu(
                tela, LARGURA_TELA, ALTURA_TELA, RECURSOS, 
                estado_config['som_ligado'], estado_config['tamanho_tabuleiro']
            )
            
            # Gerenciamento da BGM (Se mudou nos Ajustes)
            if estado_config['som_ligado'] and caminho_bgm and not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1) 
            elif not estado_config['som_ligado']:
                pygame.mixer.music.stop()
            
            if modo_principal is None or modo_principal == MODO_SAIR:
                jogo_ativo = False
                break
            
            if modo_principal == MODO_INPUT_NOMES:
                if estado_config['som_ligado'] and caminho_bgm: pygame.mixer.music.stop()
                continue
            
            continue # Volta ao início do loop para re-executar o menu
            
        # === FLUXO: INPUT DE NOMES ===
        if modo_principal == MODO_INPUT_NOMES:
            
            modo_input, estado_config_retornado, modo_jogo_real_retornado = menu_inicial.tela_input_nomes(
                tela, LARGURA_TELA, ALTURA_TELA, fonte_titulo, fonte_botoes, RECURSOS,
                estado_config, modo_jogo_real
            )
            
            if modo_input is None: 
                jogo_ativo = False
                break
                
            # ATUALIZAÇÃO EXPLÍCITA DO ESTADO
            estado_config = estado_config_retornado.copy() 
            modo_jogo_real = modo_jogo_real_retornado
            
            # Prepara o estado da partida (usa o modo_jogo_real e a config atualizada)
            estado_config, estado_partida = inicializar_estado_config_e_jogo(modo_jogo_real, estado_config) 
            
            # Recalcula offsets (necessário para o desenho do tabuleiro)
            TAMANHO_TABULEIRO = estado_partida['NUM_COLUNAS'] * LADO_CELULA
            OFFSET_X = CENTRO_TELA_X - (TAMANHO_TABULEIRO // 2)
            OFFSET_Y = BASE_OFFSET_Y - (TAMANHO_TABULEIRO - TAMANHO_PADRAO_4X4) // 2
            
            modo_principal = MODO_INICIAR_PARTIDA
            continue

        # === FLUXO: PARTIDA ATIVA ===
        if modo_principal == MODO_INICIAR_PARTIDA:
            
            # --- Funções Auxiliares de Rodada ---
            def resetar_rodada_partida(estado_partida):
                """Reseta apenas o estado do tabuleiro e os pontos para a próxima rodada."""
                linhas, colunas = estado_partida['NUM_LINHAS'], estado_partida['NUM_COLUNAS']
                num_buracos = estado_partida['num_buracos_rodada']
                
                # Recria o tabuleiro para a nova rodada
                estado_partida['tabuleiro_solucao'] = tabuleiro.inicializar_tabuleiro(linhas, colunas, NUM_TESOUROS, num_buracos)
                estado_partida['tabuleiro_visivel'] = [[False for _ in range(colunas)] for _ in range(linhas)]
                
                estado_partida['celulas_reveladas'] = 0 
                estado_partida['pontos_j1'] = 0 
                estado_partida['pontos_j2'] = 0 
                estado_partida['jogador_da_vez'] = 1 # O jogador 1 sempre começa a rodada
                estado_partida['fim_da_rodada'] = False 
                estado_partida['mensagem_final'] = "" # Limpa a mensagem da tela
                return estado_partida 

            mouse_pos = pygame.mouse.get_pos()
            
            # --- Tratamento de Eventos (Clique/Mouse) ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jogo_ativo = False
                    
                # Lógica de Botões na Tela de Fim de Jogo ou Fim de Rodada
                if estado_partida['fim_de_jogo'] or estado_partida['fim_da_rodada']:
                    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        
                        if botao_voltar_menu.collidepoint(evento.pos):
                            modo_principal = MODO_MENU_PRINCIPAL 
                            if estado_config['som_ligado'] and caminho_bgm: pygame.mixer.music.play(-1)
                            continue
                            
                        # Lógica de Nova Rodada/Novo Jogo
                        if botao_nova_rodada.collidepoint(evento.pos):
                            
                            # LÓGICA CORRIGIDA: Continua para a próxima rodada do Melhor de 3
                            if estado_partida['modo_jogo_real'] == MODO_MELHOR_DE_3 and estado_partida['fim_da_rodada'] and not estado_partida['fim_de_jogo']:
                                estado_partida['rodada_atual'] += 1
                                estado_partida = resetar_rodada_partida(estado_partida) 
                                continue
                            
                            # Lógica para Novo Jogo Completo (qualquer modo que terminou)
                            elif estado_partida['fim_de_jogo']:
                                estado_config, estado_partida = inicializar_estado_config_e_jogo(estado_partida['modo_jogo_real'], estado_config)
                                continue
                            
                    if estado_partida['fim_de_jogo'] or estado_partida['fim_da_rodada']: continue
                
                # LÓGICA DE CLIQUE DO TABULEIRO/BOTÃO SAIR
                if not estado_partida['fim_de_jogo'] and not estado_partida['fim_da_rodada'] and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    
                    if botao_sair_jogo.collidepoint(evento.pos):
                        modo_principal = MODO_MENU_PRINCIPAL
                        if estado_config['som_ligado'] and caminho_bgm: pygame.mixer.music.play(-1)
                        continue

                    # Processamento da Jogada
                    mouse_x, mouse_y = evento.pos
                    coluna_clicada = (mouse_x - OFFSET_X) // LADO_CELULA
                    linha_clicada = (mouse_y - OFFSET_Y) // LADO_CELULA

                    if (0 <= linha_clicada < estado_partida['NUM_LINHAS'] and 
                        0 <= coluna_clicada < estado_partida['NUM_COLUNAS'] and 
                        not estado_partida['tabuleiro_visivel'][linha_clicada][coluna_clicada]):
                        
                        estado_partida['tabuleiro_visivel'][linha_clicada][coluna_clicada] = True
                        conteudo = estado_partida['tabuleiro_solucao'][linha_clicada][coluna_clicada]
                        jogador_atual = estado_partida['jogador_da_vez']

                        # Lógica de Pontuação e Fim de Rodada/Jogo para MODOS PADRÃO E MELHOR DE 3
                        if estado_partida['modo_jogo_real'] in [MODO_PADRAO, MODO_MELHOR_DE_3]:
                             estado_partida['celulas_reveladas'] += 1
                             if conteudo == 'T':
                                 estado_partida['pontos_j1'] += 100 if jogador_atual == 1 else 0
                                 estado_partida['pontos_j2'] += 100 if jogador_atual == 2 else 0
                                 recursos.tocar_som('bau', RECURSOS, estado_config)
                             elif conteudo == 'B':
                                 estado_partida['pontos_j1'] = max(0, estado_partida['pontos_j1'] - 50) if jogador_atual == 1 else estado_partida['pontos_j1']
                                 estado_partida['pontos_j2'] = max(0, estado_partida['pontos_j2'] - 50) if jogador_atual == 2 else estado_partida['pontos_j2']
                                 recursos.tocar_som('buraco', RECURSOS, estado_config)
                             else:
                                 recursos.tocar_som('numero', RECURSOS, estado_config)
                             estado_partida['jogador_da_vez'] = 2 if jogador_atual == 1 else 1
                             
                             # Lógica de Fim de Rodada/Jogo
                             if estado_partida['celulas_reveladas'] == estado_partida['total_celulas']:
                                 
                                 # 1. Determinar o vencedor da RODADA
                                 vencedor_rodada_num = 0
                                 vencedor_rodada_nome = "EMPATE"
                                 
                                 if estado_partida['pontos_j1'] > estado_partida['pontos_j2']:
                                     vencedor_rodada_num = 1
                                     vencedor_rodada_nome = estado_config['nome_j1']
                                     
                                 elif estado_partida['pontos_j2'] > estado_partida['pontos_j1']:
                                     vencedor_rodada_num = 2
                                     vencedor_rodada_nome = estado_config['nome_j2']
                                     
                                 # 🟢 Lógica para MODO MELHOR DE 3
                                 if estado_partida['modo_jogo_real'] == MODO_MELHOR_DE_3:
                                     
                                     # Contabiliza a vitória
                                     if vencedor_rodada_num == 1:
                                         estado_partida['vitorias_j1'] += 1
                                     elif vencedor_rodada_num == 2:
                                         estado_partida['vitorias_j2'] += 1
                                     
                                     vitorias_j1 = estado_partida['vitorias_j1']
                                     vitorias_j2 = estado_partida['vitorias_j2']
                                     
                                     # 2. Verifica Vencedor FINAL (2 vitórias ou 3ª rodada completa)
                                     if vitorias_j1 == 2 or vitorias_j2 == 2 or estado_partida['rodada_atual'] == RODADAS_TOTAL:
                                         # FIM DO JOGO
                                         estado_partida['fim_de_jogo'] = True
                                         
                                         vencedor_final = estado_config['nome_j1'] if vitorias_j1 > vitorias_j2 else estado_config['nome_j2']
                                         
                                         # Mensagem Final
                                         estado_partida['mensagem_final'] = f"VENCEDOR FINAL: {vencedor_final}"
                                         recursos.tocar_som('vitoria', RECURSOS, estado_config) # 🟢 Toca o som de vitória no FINAL
                                         
                                     else:
                                         # FIM DA RODADA, CONTINUA PARA PRÓXIMA
                                         estado_partida['fim_da_rodada'] = True
                                         
                                         # Mensagem da Rodada (Rodada 1 ou 2)
                                         estado_partida['mensagem_final'] = f"VENCEDOR DA RODADA {estado_partida['rodada_atual']}: {vencedor_rodada_nome}"
                                         
                                 # Lógica para MODO PADRÃO
                                 else: # MODO PADRÃO
                                     estado_partida['fim_de_jogo'] = True
                                     estado_partida['mensagem_final'] = f"FIM DA PARTIDA! VENCEDOR: {vencedor_rodada_nome}"
                                     recursos.tocar_som('vitoria', RECURSOS, estado_config) # 🟢 Toca o som de vitória no MODO PADRÃO

                        # -------------------------------------------------------------------------
                        # 🟢 LÓGICA CORRIGIDA PARA O MODO MORTE SÚBITA
                        # -------------------------------------------------------------------------
                        elif estado_partida['modo_jogo_real'] == MODO_MORTE_SUBITA:
                            estado_partida['celulas_reveladas'] += 1 # Conta a célula revelada
                            
                            if conteudo == 'T':
                                estado_partida['pontos_j1'] += 100 if jogador_atual == 1 else 0
                                estado_partida['pontos_j2'] += 100 if jogador_atual == 2 else 0
                                recursos.tocar_som('bau', RECURSOS, estado_config)
                                # O turno sempre passa
                                estado_partida['jogador_da_vez'] = 2 if jogador_atual == 1 else 1 
                                
                            elif conteudo == 'B':
                                # 🟢 FIM DE JOGO: Acionado APENAS pelo Buraco.
                                recursos.tocar_som('buraco', RECURSOS, estado_config)
                                estado_partida['fim_de_jogo'] = True
                                
                                # Determina o vencedor pelo placar (desempate com tratamento de empate)
                                if estado_partida['pontos_j1'] > estado_partida['pontos_j2']:
                                     vencedor = estado_config['nome_j1']
                                     estado_partida['mensagem_final'] = f"MORTE SÚBITA! VENCEDOR: {vencedor}"
                                     recursos.tocar_som('vitoria', RECURSOS, estado_config)
                                elif estado_partida['pontos_j2'] > estado_partida['pontos_j1']:
                                     vencedor = estado_config['nome_j2']
                                     estado_partida['mensagem_final'] = f"MORTE SÚBITA! VENCEDOR: {vencedor}"
                                     recursos.tocar_som('vitoria', RECURSOS, estado_config)
                                else: # Empate de pontos
                                     estado_partida['mensagem_final'] = f"MORTE SÚBITA! EMPATE de Pontos!"
                                     # Não toca som de vitória em caso de empate
                                     
                                # O jogo termina, então não passa o turno
                            else:
                                # Célula Vazia/Número: turno passa.
                                recursos.tocar_som('numero', RECURSOS, estado_config)
                                estado_partida['jogador_da_vez'] = 2 if jogador_atual == 1 else 1


            # --- Lógica de Desenho ---
            tela.blit(IMG_FUNDO_JOGO, (0, 0))
            tabuleiro.desenhar_tabuleiro(tela, estado_partida['tabuleiro_visivel'], estado_partida['tabuleiro_solucao'], 
                                         RECURSOS, OFFSET_X, OFFSET_Y) 

            # 2. Desenho do HUD (Nomes, Placar, e Vitórias)
            POS_SCORE_J1 = (120, 380) 
            POS_J1_Vez = (165, 105) 
            POS_J2_Vez = (660, 105) 
            
            desenhar_texto_centralizado(tela, f"{estado_partida['pontos_j1']} PTS", fonte_placar, cores.preto, POS_SCORE_J1[0], POS_SCORE_J1[1])
            desenhar_texto_centralizado(tela, f"{estado_partida['pontos_j2']} PTS", fonte_placar, cores.preto, LARGURA_TELA - POS_SCORE_J1[0], POS_SCORE_J1[1])
            
            # Exibe placar de Vitórias no Modo Melhor de 3
            if estado_partida['modo_jogo_real'] == MODO_MELHOR_DE_3:
                 desenhar_texto_centralizado(tela, f"VITÓRIAS: {estado_partida['vitorias_j1']}", fonte_botoes, cores.preto, POS_J1_Vez[0], POS_J1_Vez[1] + 35)
                 desenhar_texto_centralizado(tela, f"VITÓRIAS: {estado_partida['vitorias_j2']}", fonte_botoes, cores.preto, POS_J2_Vez[0], POS_J2_Vez[1] + 35)


            cor_j1 = VERDE_DESTAQUE if estado_partida['jogador_da_vez'] == 1 and not (estado_partida['fim_de_jogo'] or estado_partida['fim_da_rodada']) else cores.preto
            cor_j2 = VERDE_DESTAQUE if estado_partida['jogador_da_vez'] == 2 and not (estado_partida['fim_de_jogo'] or estado_partida['fim_da_rodada']) else cores.preto

            desenhar_texto_centralizado(tela, estado_config['nome_j1'], fonte_botoes, cor_j1, POS_J1_Vez[0], POS_J1_Vez[1])
            desenhar_texto_centralizado(tela, estado_config['nome_j2'], fonte_botoes, cor_j2, POS_J2_Vez[0], POS_J2_Vez[1])

            # 3. Desenho de Botões e Telas de Fim
            if not estado_partida['fim_de_jogo'] and not estado_partida['fim_da_rodada']:
                  # Lógica de HOVER:
                cor_btn_saida = VERDE_DESTAQUE if botao_sair_jogo.collidepoint(mouse_pos) else cores.preto
            
                desenhar_texto_centralizado(
                    tela, "Voltar ao Menu", fonte_botoes, cor_btn_saida, 
                    botao_sair_jogo.centerx, botao_sair_jogo.centery
                    )
            
            elif estado_partida['fim_de_jogo'] or estado_partida['fim_da_rodada']:
                
                # O texto do botão muda dependendo se o jogo acabou ou se é apenas uma rodada
                msg_nova_acao = "PRÓXIMA RODADA"
                if estado_partida['fim_de_jogo']:
                    msg_nova_acao = "NOVO JOGO"

                desenhar_tela_fim_jogo(
                    tela, IMG_GAME_OVER, estado_partida['mensagem_final'], 
                    fonte_titulo, fonte_botoes, 
                    botao_nova_rodada, botao_voltar_menu, 
                    msg_nova_acao, "VOLTAR AO MENU" # Usa o texto dinâmico
                )

            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()