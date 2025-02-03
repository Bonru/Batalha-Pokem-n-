import pygame
from datetime import datetime as dt
from random import randint as r

#Inicia o pygame
pygame.init()

#Configurações
FPS = 60
tam_x = 800
tam_y = 600
tam_tela = (tam_x, tam_y)
rodar = True
telas = 0
font = pygame.font.Font('.\Fontes\ontePygame.ttf', 26)
ok = pygame.mixer.Sound('.\Sons\outrosom.ogg')
select = pygame.mixer.Sound('.\Sons\selecionar.ogg')
icon = pygame.image.load('.\Imagens\ikon.png')

#Cores
BLACK = (0, 0, 0) # (RED, GREEN, BLUE)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 120, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
DARK_PURPLE = (150, 0, 150)
DARK_GRAY = (50, 50, 50)
LIGHT_BLUE = (150, 150, 255)
LIGHT_PURPLE = (255, 150, 255)
LIGHT_GRAY = (200, 200, 200)
LIGHT_GREEN = (150, 255, 150)

#Iniciar
tela = pygame.display.set_mode(tam_tela) #Seta a tela
pygame.display.set_caption('SIMULADOR DE BATALHAS POKEMON') #Seta o título
pygame.display.set_icon(icon)#Seta o ícone
pygame.time.Clock().tick(FPS) #Seta o FPS

#Superfícies que serão usadas
menu = pygame.Surface([tam_x,tam_y])
barra_texto = pygame.Surface([tam_x, tam_y-int(tam_y/1.5)])
hud = pygame.Surface([tam_x, tam_y/1.5])
tela_escolhej1 = pygame.Surface([tam_x,tam_y])

#Pokemons
pokelist = {
    0: 'PIKACHU',
    1: 'CHARMANDER',
    2: 'SQUIRTLE',
    3: 'BULBASAUR',
    4: 'GENGAR',
    5: 'RHYDON', 
    6: 'MEWTWO',
    7: 'DITTO'
}

#dano dos golpes
d_golpes = {
    0: ("Choq. do Trovao", 15),
    1: ("Cauda Metalica", 10),
    2: ("Atk Rapido", 8),
    3: ("Encarar", 0),
    4: ("Lanca Chamas", 13),
    5: ("Furia", 5),
    6: ("Garra Metalica", 10),
    7: ("Golpear", 9),
    8: ("Jato da Agua", 12),
    9: ("Bolhas", 10),
    10: ("Atk de Cipo", 13),
    11: ("Absorver", 8, 6),
    12: ("Raio Solar", 15),
    13: ("Arranhao", 11),
    14: ("Maldicao", 14),
    15: ("Autodestruicao", 200),
    16: ("Terremoto", 18),
    17: ("Megachifre", 11),
    18: ("Psiquico", 16),
    19: ("", 0),
    20: ("Transformar", 0),
    21: ("Bomba de Lama", 9)
}

#Imagens display da batalha:
barra_p1 = ".\Imagens\Barra_2.png" #.\Pimagens\Barra_2.png
barra_p2 = ".\Imagens\Barra_1.png"

#classe responsável por trabalhar com textos
class Texto():
    def __init__(self, pos_x, pos_y, size):
        self.text = ''
        self.cor = None
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.font = pygame.font.Font('.\Fontes\pokemon_fire_red.ttf', size)
    def mudarTamanho(self, size):
        self.size = size
        self.font = pygame.font.Font('.\Fontes\pokemon_fire_red.ttf', size)
    def mudarTexto(self, text, cor):
        self.text = text
        self.cor = cor
        self.texto = self.font.render(self.text, True, self.cor)
    def exibir(self, surf):
        if '*' in self.text:
            for text in range(0, len(self.text.split('*'))):
                self.texto = self.font.render(self.text.split('*')[text], True, self.cor)
                textoRect = self.texto.get_rect()
                textoRect.centery = self.pos_y+25*text
                textoRect.left = self.pos_x
                surf.blit(self.texto, textoRect)
        else:
            textoRect = self.texto.get_rect()
            textoRect.centery = self.pos_y
            textoRect.left = self.pos_x
            surf.blit(self.texto, textoRect)

#usada para trabalhar com os diferentes golpes do jogo       
class Golpes():
    def __init__(self, pk):
        #Lista a sequencia de golpes de cada pokemon
        self.golpelist = {
            0: ('Choq. do Trovao', 'Cauda Metalica', 'Atk Rapido', 'Encarar'),
            1: ('Lanca Chamas', 'Furia', 'Garra Metalica', 'Golpear'),
            2: ('Jato da Agua', 'Bolhas', 'Encarar', 'Golpear'),
            3: ('Atk de Cipo', 'Absorver', 'Raio Solar', 'Atk Rapido'),
            4: ('Encarar', 'Arranhao', 'Maldicao', 'Bomba de Lama'),
            5: ('Autodestruicao', 'Terremoto', 'Cauda Metalica', 'Megachifre'),
            6: ('Psiquico', 'Choq. do Trovao', 'Lanca Chamas', 'Raio Solar'),
            7: ('', 'Transformar','','')
        }
        self.golpes = self.golpelist[pk]
    def exibirGolpes(self): #Texto dos golpes na tela
        ppbar = pygame.image.load('.\Imagens\Pp_bar.png')
        ppbar_scale = pygame.transform.scale(ppbar,(tam_x,int(tam_y/3)))
        tela.blit(ppbar_scale,(0,(tam_y//3)*2))        
    
    def selecionar_golpes(self): #Setinha para selecionar os golpes
        cursor = 0
        posições = {
            0:[tam_x//13.3+10,tam_y//1.1], #col1 lin1
            1:[tam_x//13.3+10,tam_y//1.3],#col1 lin2
            2:[tam_x//2.66,tam_y//1.1],#col2 lin1
            3:[tam_x//2.66,tam_y//1.3]#col2 lin2
        }
        for posicionar in posições:
            nomes_golpes = Texto(posições[posicionar][0], posições[posicionar][1], 40)
            nomes_golpes.mudarTexto(self.golpes[posicionar], DARK_GRAY)
            nomes_golpes.exibir(tela)
        golpes = True
        while golpes:
            col1 = int(tam_x//15)
            col2 =  int(tam_x//2.8)
            lin1 =  int(tam_y//1.3)
            lin2 = int(tam_y//1.1)

            posicoes = {   
                0:((col1,lin1-8),(col1+8,lin1),(col1,lin1+8)),#golpe2
                1:((col1,lin2-8),(col1+8,lin2),(col1,lin2+8)), #golpe4
                2:((col2,lin1-8),(col2+8,lin1),(col2,lin1+8)), #golpe1
                3:((col2,lin2-8),(col2+8,lin2),(col2,lin2+8))#golpe3
            }

            pygame.draw.polygon(
                tela, (PURPLE),
                [posicoes[cursor][0],posicoes[cursor][1],posicoes[cursor][2]]
            )

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    golpes = False
                    pygame.quit()
                    break

                if ev.type == pygame.KEYDOWN:

                    # Manipulando o cursor:
                    if ev.key == pygame.K_UP:
                       cursor -= 1
                    elif ev.key == pygame.K_DOWN:
                        cursor += 1
                    elif ev.key == pygame.K_LEFT:
                        cursor -= 2
                    elif ev.key == pygame.K_RIGHT:
                       cursor += 2

                    #escolheu a ação
                    elif ev.key == pygame.K_RETURN:
                        aux = posicoes[cursor]
                        if aux == posicoes[0]:
                            return self.golpes[1]
                            golpes = False
                        elif aux == posicoes[1]:
                            return self.golpes[0]
                            golpes = False
                        elif aux == posicoes[2]:
                            return self.golpes[3]
                            golpes = False
                        elif aux == posicoes[3]:
                            return self.golpes[2]
                            golpes = False

                    elif ev.key == pygame.K_ESCAPE:#o esc pode ser usado para desfazer a ação
                        return ''

                    # Verificando os limites do cursor:
                    if cursor >= len(posicoes):
                        cursor -= len(posicoes)
                    elif cursor < 0:
                        cursor += len(posicoes)

                n = 0
                while n <= len(posicoes) - 1:
                    if n != posicoes[cursor]:
                        pygame.draw.polygon(
                            tela, LIGHT_GRAY, posicoes[n]
                        )
                        n += 1
                    else:
                        n += 1
            pygame.display.update()
        pass

#classe que irá ajudar a moldar o layout base
class Opcoes():
    def __init__(self, s):
        self.surface = s
        opcoes = pygame.image.load(".\Imagens\Fgt_options.png")
        opcoes_scale = pygame.transform.scale(opcoes,(int(tam_x/2), int(tam_y - tam_y/1.5)))
        self.surface.blit(opcoes_scale, (tam_x//2, 0))
        tela.blit(self.surface, (0, int(tam_y/1.5)))

#classe que irá ajudar a moldar o layout base e exibir mensagens
class Barra_de_Texto():
    def __init__(self, text, s):
        self.surface = s
        self.text = text
        self.text_bar = pygame.image.load(".\Imagens\Text_bar.png")
        self.text_bar_scale = pygame.transform.scale(self.text_bar,(tam_x, tam_y - int(tam_y/1.5)))
        self.surface.blit(self.text_bar_scale, (0, 0))
        tela.blit(self.surface, (0, int(tam_y/1.5)))

    def mudarTexto(self, text):
        self.text = text
        
    def exibirTexto(self):
        self.text_bar = pygame.image.load(".\Imagens\Text_bar.png")
        self.text_bar_scale = pygame.transform.scale(self.text_bar,(tam_x, tam_y - int(tam_y/1.5)))
        self.surface.blit(self.text_bar_scale, (0, 0))
        tela.blit(self.surface, (0, int(tam_y/1.5)))
        if '*' in self.text:
            for text in range(0, len(self.text.split('*'))):
                texto = font.render(self.text.split('*')[text], True, WHITE)
                self.surface.blit(texto, (40, 30+25*text))
                tela.blit(self.surface, (0, int(tam_y/1.5)))
        else:
            texto = font.render(self.text, True, WHITE)
            self.surface.blit(texto, (40, 30))
            tela.blit(self.surface, (0, int(tam_y/1.5)))
        pygame.display.update()

#reproduza a animação e efeitos de alguns golpes específicos
def animar(pos_x, pos_y, animacao, fms, repeat, timerz):
    sprites = []
    for i in range(0, fms):
        sprites.append(pygame.transform.scale(pygame.image.load(f'.\Imagens\{animacao}\{i}.png'), (120, 120)))
    for current_sprite in range(0, int(fms*repeat)):
        tela.blit(tela_escolhej1, (0, 0))
        image = sprites[current_sprite]
        imageRect = image.get_rect()
        imageRect.centerx = pos_x
        imageRect.centery = pos_y
        tela.blit(image, imageRect)
        tempo = int(dt.now().microsecond / 1000)
        current = tempo-1
        while (tempo-current) % timerz != 0:
            tempo = int(dt.now().microsecond / 1000)
        pygame.display.update()

#define as características de cada pokemon
class Personagem():
    def __init__(self, pk, frentecostas):
        self.pk = pk
        self.nome = pokelist[self.pk]
        self.lista = {
                       #HP, AT, DF, Sp
            'PIKACHU': (35, 55, 40, 90),
            'CHARMANDER': (39, 52, 43, 65),
            'SQUIRTLE':(44, 48, 65, 43),
            'BULBASAUR':(45, 49, 49, 45),
            'GENGAR':(60, 65, 60, 110),
            'RHYDON':(80, 85, 95, 25),
            'MEWTWO':(106, 110, 90, 130),
            'DITTO':(48, 48, 48, 48)
        }
        self.hp_max = self.lista[self.nome][0]
        self.hp = self.hp_max
        self.at = self.lista[self.nome][1]
        self.df = self.lista[self.nome][2]
        self.sp = self.lista[self.nome][3]
        self.barulho = pygame.mixer.Sound(f'.\Sons\{pokelist[pk].lower()}.ogg')
        self.frente = pygame.image.load(f'.\Imagens\{self.nome.lower().capitalize()}_Frente.png')
        self.costas = pygame.image.load(f'.\Imagens\{self.nome.lower().capitalize()}_costas.png')
        self.frente_scale = pygame.transform.scale(self.frente, (150, 150))
        self.costas_scale = pygame.transform.scale(self.costas, (200, 200))
        self.ordem = [self.costas, self.frente]
        self.frentecostas = frentecostas
        self.poisoned = False
        self.desintoxicacao = 0
        self.fugir = False
        self.pocoes = 5
    
    def rugir(self):
        self.barulho.play()
    
    def envenenado(self):
        return self.poisoned

    def desenharVida(self, position, prop, surf):
        if position == 0:
            barra_cinza = pygame.draw.rect(surf, GRAY, (600, 323, 172, 12))
            pygame.draw.rect(surf, LIGHT_GREEN, (600, 323, 172*prop, 12))
            pokebarra1 = pygame.image.load(barra_p1)
            pokebarra1_scale = pygame.transform.scale(pokebarra1, (375, 150))
            textHp1 = Texto(barra_cinza.centerx, barra_cinza.centery, 18)
            textHp1.mudarTexto(f'HP:{int(self.hp)}/{self.hp_max}', WHITE)
            nome1 = Texto(barra_cinza.centerx, 290, 48)
            nome1.mudarTexto(self.nome, DARK_GRAY)
            nome1.pos_x = barra_cinza.centerx - (nome1.texto.get_rect().width)
            textHp1.pos_x = barra_cinza.centerx - (textHp1.texto.get_rect().width/2)
            surf.blit(pokebarra1_scale, (425, 250))
            nome1.exibir(surf)
            textHp1.exibir(surf)
            tela.blit(surf,(0,0))
            pygame.display.update()
        elif position == 1:
            barra_cinza2 = pygame.draw.rect(surf, GRAY, (118, 50, 140, 12))
            pygame.draw.rect(surf, LIGHT_GREEN, (118, 50, 140*prop, 12))
            pokebarra2 = pygame.image.load(barra_p2)
            pokebarra2_scale = pygame.transform.scale(pokebarra2, (281, 76))
            textHp2 = Texto(barra_cinza2.centerx, barra_cinza2.centery, 18)
            nome1 = Texto(barra_cinza2.centerx, 30, 30)
            nome1.mudarTexto(self.nome, DARK_GRAY)
            nome1.pos_x = barra_cinza2.centerx - (nome1.texto.get_rect().width)
            textHp2.mudarTexto(f'HP:{int(self.hp)}/{self.hp_max}', WHITE)
            textHp2.pos_x = barra_cinza2.centerx - (textHp2.texto.get_rect().width/2)
            surf.blit(pokebarra2_scale, (10, 10))
            nome1.exibir(surf)
            textHp2.exibir(surf)
            tela.blit(surf,(0,0))
            pygame.display.update()
    
    def proporcao_vida(self):
        return (self.hp/self.hp_max)
    
    def rectangle(self, obj_rect, x, bottom):
        self.obj_rect = obj_rect.get_rect()
        self.obj_rect.centerx = x
        self.obj_rect.bottom = bottom
        return self.obj_rect
    
    def mover_hp(self, vida, surf): #executa a animação das barras de vida descendo e subindo
        if (self.hp + vida) <= 0:
            for life in range(0, int(self.hp)+2):
                if self.hp > 0:
                    self.hp -= 1
                tempo = int(dt.now().microsecond / 1000)
                current = tempo-1
                while (tempo-current) % 30 != 0:
                    tempo = int(dt.now().microsecond / 1000)
                self.desenharVida(self.frentecostas, self.proporcao_vida(), surf)
        elif (self.hp + vida) > 0:
            for life in range(0, abs(vida)):
                if (self.hp + vida) < self.hp_max:
                    self.hp += (vida/abs(vida))
                elif self.hp < self.hp_max:
                    self.hp += (vida/abs(vida))
                tempo = int(dt.now().microsecond / 1000)
                current = tempo-1
                while (tempo-current) % 30 != 0:
                    tempo = int(dt.now().microsecond / 1000)
                self.desenharVida(self.frentecostas, self.proporcao_vida(), surf)
    
    def Ataque(self, inimigo, dano, surf):
        inimigo.mover_hp(dano, surf)

def fade(tam, tickle): #executa uma transição de tela entre o menu e a tela de batalha
    fade = pygame.Surface(tam)
    fade.fill(BLACK)
    for alpha in range(0, 50):
        fade.set_alpha(alpha)
        tela.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(tickle)

def menu_p():#cria o menu para seleção dos pokemons
    
    repetir = True
    pygame.mixer.music.load('.\Musica\Musica_chaguitas.mp3') #Música que eu botei pra ficar de fundo no menu
    pygame.mixer.music.play(-1) #Para dar o Loop
    pygame.mixer.music.set_volume(0.25) #Para diminuir o volume, kkk. Muito alto.
    while repetir:
        #Configurações
        pygame.time.Clock().tick(240) #Altera o FPS para 240 para dar a ilusão de que tudo acontece na hora e não haver delay no aúdio
        count = 0 #Um contador :D 
        pos_sel = 0 #O seletor principal
        cor1 = RED #Cor do seletor 1
        cor2 = GREEN #Cor do seletor 2
        pos_sel1 = 0  # Posição inicial do Seletor Jogador 1
        pos_sel2 = 0  # Posição inicial do Seletor Jogador 2
        basicFont = pygame.font.SysFont(None, 48) #Fonte 1
        basicFont1 = pygame.font.SysFont(None, 36) #Fonte 2, mesma fonte, tamanho diferente
        playerFont = pygame.font.SysFont(None, 40) #Fonte 3, mesma fonte, tamanho diferente
        pronto_jogador1 = False #Indica se o jogador 1 está pronto
        pronto_jogador2 = False #Indica se o jogador 2 está pronto
        passar = False #Loop
        poketext = { #TEXTO DA POKELIST
            0: (pokelist[0], True, YELLOW),
            1: (pokelist[1], True, ORANGE),
            2: (pokelist[2], True, BLUE),
            3: (pokelist[3], True, GREEN),
            4: (pokelist[4], True, DARK_PURPLE),
            5: (pokelist[5], True, LIGHT_GRAY),
            6: (pokelist[6], True, LIGHT_PURPLE),
            7: (pokelist[7], True, PURPLE)
        }
        pokemons = [] #Pokemons escolhidos

        #Iniciar

        while passar == False:

            #tela.fill(BLACK) — NUNCA TOQUE NO CÓDIGO COMENTADO DE ALGUÉM
            menu1 = pygame.image.load(".\Imagens\menu1.png")
            menu1_scale = pygame.transform.scale(menu1,(int(tam_x*1.5),int(tam_y*1.5)))
            menu1_scaleRect = menu1_scale.get_rect()
            menu1_scaleRect.centerx = tela.get_rect().centerx
            menu1_scaleRect.centery = 360
            menu.blit(menu1_scale, menu1_scaleRect)

            #Gráfico
            pygame.draw.rect(menu, WHITE, (tela.get_rect().centerx-130, tela.get_rect().centery-160, 260, 400)) #Borda Branca
            pygame.draw.rect(menu, BLACK, (tela.get_rect().centerx-125, tela.get_rect().centery-155, 250, 390)) #Interior Preto
            y_sel2 = ((77)*pos_sel2)+189  # Eixo y da setinha do jogador 2
            if pronto_jogador1 == True:  # Se o jogador 1 já escolheu, cria a seta do jogador 2
                setinha2 = pygame.draw.polygon(menu, cor2, ((tela.get_rect().centerx+120, y_sel2-5), (tela.get_rect().centerx+120, y_sel2+5), (tela.get_rect().centerx+109, y_sel2)))
            if pos_sel1 < 0 or pos_sel1 > 4:  # Se a posição da seta do jogador1 for negativa, muda a cor para preto
                # Isso é por causa que chega um momento que a seta sai da tela, e pra não aparecer eu fiz isso.
                cor1 = BLACK
                y_sel1 = 189 # Eu fiz isso pra permanecer na tela, por causa do background
            else:  # Caso contrário, mude para vermelho
                # OBS: Isso é necessário apenas para a vermelha, porque, depois da verde, o menu para.
                cor1 = RED
                y_sel1 = ((77)*pos_sel1)+189  # Eixo y da setinha do jogador 1
            
            setinha = pygame.draw.polygon(menu, cor1, ((tela.get_rect().centerx-120, y_sel1-5), (tela.get_rect().centerx-120,y_sel1+5), (tela.get_rect().centerx-109, y_sel1)))  # Seta do jogador 1 = desenhar(ponto 1, ponto2, ponto3)

            if pronto_jogador1 == False:
                pos_sel1 = pos_sel
            elif pronto_jogador2 == False:
                pos_sel2 = pos_sel
            sample1 = pygame.image.load(f'.\Imagens\{pokelist[pos_sel1+count].lower().capitalize()}_Frente.png')
            sample1_scale = pygame.transform.scale2x(sample1)
            sample2 = pygame.image.load(f'.\Imagens\{pokelist[pos_sel2+count].lower().capitalize()}_Frente.png')
            sample2_scale = pygame.transform.scale2x(sample2)
                
            #Texto — apenas isto, gera os textos
            titulo = basicFont.render('CHOOSE YOUR POKEMON', True, WHITE)
            tituloRect = titulo.get_rect() #Transforma o texto em um retângulo, para podermos manipular de uma maneira mais simples
            tituloRect.centerx = tela.get_rect().centerx
            tituloRect.centery = 60
            p1 = playerFont.render('PLAYER 1', True, WHITE)
            p1Rect = p1.get_rect()
            p1Rect.centerx = (tela.get_rect().centerx-160)/2
            p1Rect.centery = 500
            p2 = playerFont.render('PLAYER 2', True, WHITE)
            p2Rect = p1.get_rect()
            p2Rect.centerx = 800-((tela.get_rect().centerx-160)/2)
            p2Rect.centery = 500
            poke1 = basicFont1.render(poketext[pos_sel1+count][0], poketext[pos_sel1+count][1], poketext[pos_sel1+count][2]) #Gera o nome do pokemon onde o seletor está
            poke1Rect = poke1.get_rect()
            poke1Rect.centerx = p1Rect.centerx
            poke1Rect.centery = 550
            namepoke2 = poketext[pos_sel2+count]
            if pronto_jogador1 == False: poke2 = basicFont1.render('NONE', True, GREEN)
            else: poke2 = basicFont1.render(namepoke2[0], namepoke2[1], namepoke2[2])
            poke2Rect = poke2.get_rect()
            poke2Rect.centerx = p2Rect.centerx
            poke2Rect.centery = 550

            #Renderizar
            menu.blit(titulo, tituloRect)
            menu.blit(p1, p1Rect)
            menu.blit(p2, p2Rect)
            menu.blit(poke1, poke1Rect)
            menu.blit(poke2, poke2Rect)
            menu.blit(sample1_scale, (poke1Rect.centerx - (sample1_scale.get_rect().width/2), poke1Rect.centery-sample1_scale.get_rect().height-150))
            if pronto_jogador1 == True:
                menu.blit(sample2_scale, (poke2Rect.centerx - (sample2_scale.get_rect().width/2), poke2Rect.centery-sample2_scale.get_rect().height-150))
            for i in range(0, 5):
                nomesPokemons = basicFont1.render(poketext[i+count][0], poketext[i+count][1], poketext[i+count][2])
                nomesPokemons_rect = nomesPokemons.get_rect()
                nomesPokemons_rect.centerx = tela.get_rect().centerx
                nomesPokemons_rect.centery = ((77)*i)+189
                menu.blit(nomesPokemons, nomesPokemons_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and pronto_jogador2 == False:
                        select.play()
                        if pos_sel > 0:
                            pos_sel -= 1
                        elif count > 0:
                            count -= 1
                            if pronto_jogador1 == True:
                                pos_sel1 += 1
                    if event.key == pygame.K_DOWN and pronto_jogador2 == False:
                        select.play()
                        if pos_sel < 4:
                            pos_sel += 1
                        elif count < len(pokelist)-5:
                            count += 1
                            if pronto_jogador1 == True:
                                pos_sel1 -= 1
                    if event.key == pygame.K_RETURN:
                        ok.play()
                        if pronto_jogador1 == False:
                            pronto_jogador1 = True
                            pokemons.append(pos_sel+count)
                            pygame.mixer.Sound(f'.\Sons\{pokelist[pos_sel+count].lower()}.ogg').play()
                        elif pronto_jogador1 == True and pronto_jogador2 == False:
                            pronto_jogador2 = True
                            pokemons.append(pos_sel+count)
                            pygame.mixer.Sound(f'.\Sons\{pokelist[pos_sel+count].lower()}.ogg').play()
                        elif pronto_jogador1 == True and pronto_jogador2 == True:
                            if pokemons[0] == 0 and pokemons[1] == 0:
                                pygame.mixer.Sound('.\Sons\pikachu-starter.ogg').play()
                            repetir = False
                            passar = True
                    if event.key == pygame.K_BACKSPACE:
                        passar = True
            tela.blit(menu,(0,0))
            pygame.display.update()
        
    pygame.mixer.music.fadeout(2000)
    pygame.time.Clock().tick(FPS)
    fade(tam_tela, 10)
    
    return pokemons

def mochila_p(pk):# abre a tela da mochila e retorna o item selecionado
    mochila = True
    cont =  0
    tamanho = (tam_x/3,tam_y/5),(tam_x/3*2,tam_y/5),(tam_x/3*2,tam_y/4*3),(tam_x/3,tam_y/4*3)
    display_mochila = pygame.Surface([tam_x,tam_y])

    p_cursor = {
        0: (f"{pk.pocoes}x Poção",tam_x//2,tam_y//3),
        1: ("Introcoin",tam_x//2,tam_y//2),
        2: ("Veneno",tam_x//2,tam_y//3*2)
    }
    
    while mochila == True:
        tela.blit(display_mochila,(0,0))
        display_mochila.fill(PURPLE)
        pygame.draw.polygon(
        display_mochila, LIGHT_PURPLE, (tamanho))
        
        for i in p_cursor:
            if cont == i:
                text = font.render(p_cursor[i][0], True, BLACK)
            else:
                text = font.render(p_cursor[i][0], True, BLUE)
            text_rect = text.get_rect()
            text_rect.center = (
                p_cursor[i][1],
                p_cursor[i][2]
            )
            #text_size = (text.get_width(), text.get_height())
            display_mochila.blit(text, text_rect)#button.text_offset(text_size))
        
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN: #Se o evento for uma tecla pressionada:
                if ev.key == pygame.K_UP:
                    cont -= 1
                elif ev.key == pygame.K_DOWN:
                    cont += 1
                elif ev.key == pygame.K_RETURN:
                    mochila = False

                elif ev.key == pygame.K_ESCAPE:#usado para sair da mochila
                    return ''    
            # Verificando os limites do cursor:
                if cont >= len(p_cursor):
                    cont -= len(p_cursor)
                elif cont < 0:
                    cont += len(p_cursor)
        pygame.display.update()
    del display_mochila
    pygame.display.flip()
    if p_cursor[cont][0] == f'{pk.pocoes}x Poção' and pk.pocoes == 0:#conta o número de poçoes disponíveis
        return ''
    else:
        return cont

def selecionar(pk):#seleciona a ação que será feita pelo pokemon
    cursor = 0
    running = True
    while running:
        col1 = int(tam_x/2.1)*1.63 
        col2 = int(tam_x/(40/9))*2.4 
        lin1 = int(tam_y/(4/3))*1.05
        lin2 = int(tam_y/(10/9))

        bagitens = {
            0: 'Poção',
            1: 'Introcoin',
            2: 'Veneno',
            '': ''
        }

        posicoes = {   
            0:((col2,lin1-8),(col2+8,lin1),(col2,lin1+8)), #ataque
            1:((col1,lin1-8),(col1+8,lin1),(col1,lin1+8)),#mochila
            2:((col1,lin2-8),(col1+8,lin2),(col1,lin2+8)), #fugir
            #3:((col2,lin2-8),(col2+8,lin2),(col2,lin2+8))#pokemon
        }

        pygame.draw.polygon(
            tela, (PURPLE),
            [posicoes[cursor][0],posicoes[cursor][1],posicoes[cursor][2]]
        )

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                pygame.quit()
                break

            if ev.type == pygame.KEYDOWN:

                # Manipulando o cursor:
                aux = posicoes[cursor]
                if aux == posicoes[0]:
                    if ev.key == pygame.K_LEFT:
                        cursor += 1
                    elif ev.key == pygame.K_RIGHT:
                        cursor += 1
                    elif ev.key == pygame.K_UP:
                        cursor += 2
                    elif ev.key == pygame.K_DOWN:
                        cursor += 2
                elif aux == posicoes[1]:
                    if ev.key == pygame.K_LEFT:
                        cursor -= 1
                    elif ev.key == pygame.K_RIGHT:
                        cursor -= 1
                    elif ev.key == pygame.K_UP:
                        cursor += 1
                    elif ev.key == pygame.K_DOWN:
                        cursor += 1
                elif aux == posicoes[2]:
                    if ev.key == pygame.K_LEFT:
                        cursor -= 2
                    elif ev.key == pygame.K_RIGHT:
                        cursor -= 2
                    elif ev.key == pygame.K_UP:
                        cursor -= 1
                    elif ev.key == pygame.K_DOWN:
                        cursor -= 1

                #escolheu a ação
                if ev.key == pygame.K_RETURN:
                    aux = posicoes[cursor]
                    if aux == posicoes[1]:
                        bagvalor = mochila_p(pk)
                        valor = bagitens[bagvalor]
                        running = False
                    elif aux == posicoes[2]:
                        valor = 'Fugir'
                        running = False
                    elif aux == posicoes[0]:
                        g = Golpes(pk.pk)
                        g.exibirGolpes()
                        valor = g.selecionar_golpes()
                        running = False
                    
                # Verificando os limites do cursor:
                if cursor >= len(posicoes):
                    cursor -= len(posicoes)
                elif cursor < 0:
                    cursor += cursor*(-1)
            n = 0
            while n <= len(posicoes) - 1:
                if n != posicoes[cursor]:
                    pygame.draw.polygon(
                        tela, LIGHT_GRAY, posicoes[n]
                    )
                n += 1
        pygame.display.update()
    return valor

def config_select(pk1, pk2, s, p):
    cord = [0, 1]
    pk1.frentecostas = cord[p]
    pk2.frentecostas = cord[p-1]       
    FundoPokemon = pygame.image.load(".\Imagens\FundoPokemon.png")#
    FundoPokemon_scale = pygame.transform.scale(FundoPokemon,(tam_x,int(tam_y/1.5)))#
    s.blit(FundoPokemon_scale,(0,0))#
    s.blit(pk1.costas_scale, pk1.rectangle(pk1.costas_scale, 160, 402))#
    s.blit(pk2.frente_scale,  pk2.rectangle(pk2.frente_scale, 560, 230))#
    pk1.desenharVida(pk1.frentecostas, pk1.proporcao_vida(), s)
    pk2.desenharVida(pk2.frentecostas, pk2.proporcao_vida(), s)

def musica(pk1, pk2):#toca a música da batalha B)
    pygame.mixer.music.load('.\Musica\Musica_batalha.mp3')
    pygame.mixer.music.play(-1)
    pk1.rugir()
    pygame.time.delay(700)
    pk2.rugir()

def ação(ação, pk, pk_adv, rd, fury):#comanda o que será feito dependendo da ação de cada turno
    fc = [pk_adv.frente_scale, pk_adv.costas_scale]
    for ataque in d_golpes:
        if ação in d_golpes[ataque]:
            if ação == "Absorver":
                pk.rugir()
                pk.Ataque(pk_adv, d_golpes[ataque][1]*(-1), tela_escolhej1)
                pk.Ataque(pk, d_golpes[ataque][2], tela_escolhej1)
            elif ação == "Autodestruicao":
                pk.rugir()
                animar(pk.obj_rect.centerx, pk.obj_rect.centery, 'Autodestruicao', 8, 1, 100)
                pk.Ataque(pk, d_golpes[ataque][1]*(-1), tela_escolhej1)
                animar(pk_adv.obj_rect.centerx, pk_adv.obj_rect.centery, 'Autodestruicao', 8, 1, 100)
                pk.Ataque(pk_adv, d_golpes[ataque][1]*(-1), tela_escolhej1)
            elif ação == 'Transformar':
                vidinha = pk.proporcao_vida
                pk.__init__(pk_adv.pk, pk.frentecostas)
                pk.proporcao_vida = vidinha
                pk.nome = pokelist[7]
            elif ação == 'Bolhas':
                pk.rugir()
                animar(pk_adv.obj_rect.centerx, pk_adv.obj_rect.centery, 'Bolhas', 12, 1, 50)
                pk.Ataque(pk_adv, d_golpes[ataque][1]*(-1), tela_escolhej1)
            elif ação == 'Furia':
                pk.rugir()
                for golpeando in range(0, fury):
                    animar(pk_adv.obj_rect.centerx, pk_adv.obj_rect.centery, 'Golpear', 5, 1, 100)
                    pk.Ataque(pk_adv, d_golpes[ataque][1]*(-1), tela_escolhej1)
            else:
                pk.rugir()
                animar(pk_adv.obj_rect.centerx, pk_adv.obj_rect.centery, 'Golpear', 5, 1, 100)
                pk.Ataque(pk_adv, d_golpes[ataque][1]*(-1), tela_escolhej1)

    if ação == 'Poção':
        pk.rugir()
        pk.Ataque(pk, 20, tela_escolhej1) #Chama o comando de atacar, só que ao invés de atacar o pokemon inimigo, ele ataca a sí mesmo e também recupera vida.
        pk.pocoes -= 1

    elif ação == 'Introcoin':
        pk.rugir()
    
    elif ação == 'Veneno':
        pk_adv.poisoned = True
        pk_adv.desintoxicacao = rd
    
    elif ação == 'Fugir':
        pk.fugir = True
    
    if pk.poisoned == True:#avalia os rounds do veneno
        if (rd-pk.desintoxicacao) < 3:
            pk.rugir()
            pk.Ataque(pk, -7, tela_escolhej1)
        else:
            pk.poisoned = False
        

def luta(pJogador1, pJogador2): #configura o loop entre os turnos até a derrota de um dos pokemons
    musica(pJogador1, pJogador2)
    rodadas = 0
    while pJogador1.hp > 0 and pJogador2.hp > 0 and (pJogador1.fugir == False and pJogador2.fugir == False):
        ordem = [pJogador1, pJogador2]
        rodadas += 1
        acao = []
        while len(acao) < 2:
            config_select(ordem[len(acao)],ordem[len(acao)-1],tela_escolhej1, 0)
            tela.blit(tela_escolhej1, (0, 0))
            pygame.display.update()
            bar = Barra_de_Texto(f"O que você quer*fazer?", barra_texto)#texto para identificar de quem é a vez
            bar.exibirTexto()
            op = Opcoes(barra_texto)
            action = selecionar(ordem[len(acao)])
            if action != '':#isso serve para invalidar golpes vazios de Ditto e para usar 'esc' como um meio de voltar
                acao.append(action)
        config_select(ordem[0],ordem[1],tela_escolhej1, 0)
        for qqcoisa in range(0, len(acao)):
            furioso = 0
            qcoisa = qqcoisa
            if qqcoisa == 0:
                if pJogador1.sp < pJogador2.sp:
                    ordem.reverse()
                    acao.reverse()
                if "Poção" == acao[1]:
                    ordem.reverse()
                    acao.reverse()
                if "Atk Rapido" == acao[1]:
                    ordem.reverse()
                    acao.reverse()
                
            if ordem[qqcoisa].hp > 0 and ordem[qqcoisa-1].fugir == False:#passa as mensagens do que está acontecendo no jogo
                for ataque in d_golpes:
                    if acao[qcoisa] in d_golpes[ataque]:
                        if acao[qcoisa] == 'Absorver':
                            bar.mudarTexto(f"{ordem[qqcoisa].nome} usou {acao[qcoisa]}*e roubou {d_golpes[ataque][1]} de vida de {ordem[qqcoisa-1].nome}!")
                            bar.exibirTexto()
                        elif acao[qcoisa] == 'Transformar':
                            bar.mudarTexto(f"{ordem[qqcoisa].nome} usou {acao[qcoisa]}*e se transformou no {ordem[qqcoisa-1].nome}!")
                            bar.exibirTexto()
                        elif acao[qcoisa] == 'Furia':
                            furioso = r(1, 5)
                            bar.mudarTexto(f'{ordem[qqcoisa].nome} usou {acao[qcoisa]}*e atacou {furioso} vezes o*{ordem[qqcoisa-1].nome}!')
                            bar.exibirTexto()
                        else:
                            bar.mudarTexto(f"{ordem[qqcoisa].nome} usou {acao[qcoisa]}*e deu {d_golpes[ataque][1]} de dano!")
                            bar.exibirTexto()
                if acao[qcoisa] == 'Poção':
                    bar.mudarTexto(f"{ordem[qqcoisa].nome} usou {acao[qcoisa]}*e curou {int(ordem[qqcoisa].hp_max - ordem[qqcoisa].hp) if ordem[qqcoisa].hp_max - ordem[qqcoisa].hp < 20 else 20} de hp!")
                    bar.exibirTexto()
                elif acao[qcoisa] == 'Veneno':
                    bar.mudarTexto(f'{ordem[qqcoisa].nome} usou {acao[qcoisa]} no {ordem[qqcoisa-1].nome}!*Agora ele vai tomar*durante 3 rodadas -7 de dano* por envenenamento!')
                    bar.exibirTexto()
                elif acao[qcoisa] == 'Fugir':
                    bar.mudarTexto(f'{ordem[qqcoisa].nome} fugiu!')
                    bar.exibirTexto()
                elif acao[qqcoisa] == 'Introcoin':
                    bar.mudarTexto(f'{ordem[qqcoisa].nome} mostrou para {ordem[qqcoisa-1].nome} *que tem uma incrível Introcoin.*{ordem[qqcoisa-1].nome} se sente *desestabilizado com a bela moeda.')
                    bar.exibirTexto()
                passar = False
                while passar == False:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                passar = True
                ação(acao[qcoisa], ordem[qqcoisa], ordem[qqcoisa-1], rodadas, furioso)
                if ordem[qqcoisa].desintoxicacao != 0 and ordem[qqcoisa].poisoned == True:#considera o dano caso envenenado
                    bar.mudarTexto(f'{ordem[qqcoisa].nome} tomou 7 de dano por envenenamento!')
                    bar.exibirTexto()
                    passar = False
                    while passar == False:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    passar = True
                elif ordem[qqcoisa].desintoxicacao != 0 and ordem[qqcoisa].poisoned == False:#considera a melhora do veneno após 3 rounds
                    bar.mudarTexto(f'{ordem[qqcoisa].nome} está curado do envenenamento!')
                    bar.exibirTexto()
                    ordem[qqcoisa].desintoxicacao = 0
                    passar = False
                    while passar == False:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    passar = True
    #identificando se houve vítória derrota ou empate
    if pJogador1.hp > 0 and pJogador1.fugir == False:
        bar.mudarTexto(f"{pJogador1.nome} venceu!")
    elif pJogador2.hp > 0 and pJogador2.fugir == False:
        bar.mudarTexto(f"{pJogador2.nome} venceu!")
    elif pJogador2.hp <= 0 and pJogador1.hp <= 0 and pJogador1.fugir == False and pJogador2.fugir == False:
        bar.mudarTexto("EMPATE! Os dois desmaiaram!")
    else:
        bar.mudarTexto("EMPATE! Os dois fugiram!")
    pygame.mixer.music.load('.\Musica\Vitoria.wav') #Musicazinha de fundo
    pygame.mixer.music.play(-1) #Para dar o Loop
    bar.exibirTexto()
    passar = False
    while passar == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    passar = True

#Loop inicial
while rodar:
    
    if telas == 0:
        pokemons = menu_p()
        pokemon1 = Personagem(pokemons[0], 0)
        pokemon2 = Personagem(pokemons[1], 1)
        telas = 1
        

    if telas == 1:
        luta(pokemon1, pokemon2)
        telas = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodar = False
    
    pygame.display.update()