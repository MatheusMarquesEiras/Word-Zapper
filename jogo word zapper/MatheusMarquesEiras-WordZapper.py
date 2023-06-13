import string
import pygame
from pygame import *
from sys import exit
import os
from pathlib import Path
import random
import unicodedata

class usuario:
    def __init__(self,posicao_inicial_x,posicao_inicial_y,velocidade):
        self.nave = pygame.image.load(caminho_arquivo("nave.png"))
        self.rect = pygame.Rect(posicao_inicial_x, posicao_inicial_y, self.nave.get_width(), self.nave.get_height())
        self.rect.topleft = posicao_inicial_x,posicao_inicial_y
        self.velocidade = velocidade

        self.tiro_disparado = False

    def move(self):
        janela.blit(self.nave,self.rect)
        
        if pygame.key.get_pressed()[K_a]:
            self.rect.x -= self.velocidade
            if self.rect.x < -5:
                self.rect.x += self.velocidade

        if pygame.key.get_pressed()[K_d]:
            self.rect.x += self.velocidade
            if self.rect.x >= 760:
                self.rect.x -= self.velocidade

        if pygame.key.get_pressed()[K_s]:
            self.rect.y += self.velocidade
            if self.rect.y >= 425:
                self.rect.y -= self.velocidade

        if pygame.key.get_pressed()[K_w]:
            self.rect.y -= self.velocidade
            if self.rect.y < 150:
                self.rect.y += self.velocidade

    def volta_comeco(self):
        self.rect.x = 380
        self.rect.y = 400
    
    def tiro(self):
        if pygame.key.get_pressed()[K_SPACE] and not self.tiro_disparado:
            tiro = disparo(self.rect.center[0],self.rect.top)
            grupoTiros.add(tiro)

            self.tiro_disparado = True
        elif not pygame.key.get_pressed()[K_SPACE]:
            self.tiro_disparado = False

class disparo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(caminho_arquivo("tiro.png"))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global listaOpcoes
        global palavraSorteada
        global palavraSorteadaNormalizada
        global letrasPalavra
        global listaVerificacao
        global jogando
        global venceu
        global perdeu
        global acertouErrado
        self.rect.y -= 10

        for i in range(26):
            
            if self.rect.colliderect(listaOpcoes[i].retangulo) and not listaOpcoes[i].colidiu:
                self.kill()  
                listaOpcoes[i].cor = (0,0,0)

                listaOpcoes[i].colidiu = True

                if listaOpcoes[i].letra in palavraSorteadaNormalizada:
                    for letra in range (len(palavraSorteadaNormalizada)):
                        if palavraSorteadaNormalizada[letra] == listaOpcoes[i].letra:
                            letrasPalavra[letra].letra = palavraSorteada[letra]
                            listaVerificacao[letra] = palavraSorteada[letra]
                            if "_" not in listaVerificacao:
                                venceu = True
                else:
                    acertouErrado += 5

        if self.rect.y < 0:  
            self.kill()

class botao():
    def __init__(self,texto,x,y,largura,altura,funcao):
        # Atributos padrões para verificações por motivos de performace
        self.clicou = False

        # Especifica o retangulo que sera desenhado
        self.retanguloConteiner = pygame.Rect(x,y,largura,altura)
        self.corBotao = (100,100,100)

        # escreve o texto na superficie
        self.texto = fonte_texto.render(texto,True,(255,255,255))
        # Obtem o tamanho do texto e o guarda dentro do retangulo que ira conter-lo
        self.retanguloTamnhoTexto = self.texto.get_rect(center=(self.retanguloConteiner.centerx, self.retanguloConteiner.centery))

        self.funcao = funcao

    def desenha_botao(self):
        # Desenha o retangulo especificado
        pygame.draw.rect(janela,self.corBotao,self.retanguloConteiner,border_radius=10)
        # Coloca o retangulo na tela
        janela.blit(self.texto,self.retanguloTamnhoTexto)

    def click(self):
        # Obtem a posição do maouse
        mouse = pygame.mouse.get_pos()

        # Verifica se o mouse esta dentro do botão
        if self.retanguloConteiner.collidepoint(mouse):
            # Muda a cor do botão quando o mouse esta dentro dele
            self.corBotao = (55,55,55)

            # Verifica se foi clicado com o botao esquerdo
            if pygame.mouse.get_pressed()[0]:
                # Significa que ele clicou e somente uma booleana ira ser atribuida a essa variavel
                self.clicou = True
                
            # Quando a condição acima deixar de ser verdadeira, ou seja, o jogador deixou de pressionar o botão, então a booleana volta a ser falsa por padrão e a ação é executada
            else:
                # Isso é feito dessa forma por conta de que ao se colocar uma grande quantidade de frames na execução do jogo, essa ação seria executada várias vezes, o que pode comprometer a performace do jogo em determinados dispositivos
                if self.clicou == True:
                    self.clicou = False
                    self.funcao()
        else:
            self.corBotao = (100,100,100)

class alfabeto():
    def __init__(self,letra, fonteLetra, Retangulo, velocidade, larguraFonte, alturaFonte):
        self.letra = letra
        self.fonteLetra = fonteLetra
        self.retangulo = Retangulo
        self.velocidade = velocidade
        self.larguraFonte = larguraFonte
        self.alturaFonte = alturaFonte
        self.cor = (255,255,255)
        self.colidiu = False 

    def desenha_lista_movendo(self):
        
        letraTela = self.fonteLetra.render(self.letra, True, self.cor)
        janela.blit(letraTela, self.retangulo)

        self.retangulo.x -= self.velocidade

        if self.retangulo.x < 0:
            self.retangulo.x = 1700
            self.cor = (255,255,255)
            self.colidiu = False

class letra():
    def __init__(self,letra,fonteUsada,x,y,larguraFonte,alturaFonte):
        self.letra = letra
        self.fonteUsada = fonteUsada
        self.x = x
        self.y = y
        self.larguraFonte = larguraFonte
        self.alturaFonte = alturaFonte
        self.cor = (255,255,255)

    def desenha_letras(self):
        retangulo = pygame.draw.rect(janela,(255,0,0),(self.x,500,self.larguraFonte,self.alturaFonte))

        letraTela = self.fonteUsada.render(self.letra, True, self.cor)

        x_letra = retangulo.centerx - letraTela.get_width() // 2
        y_letra = retangulo.centery - letraTela.get_height() // 2

        # Desenha a letra na posição correta
        janela.blit(letraTela, (x_letra, y_letra))

class asteroide():
    def __init__(self,retangulo,velocidade,ladoComeco:str):
        self.imagem = pygame.image.load(caminho_arquivo("asteroide.png"))
        self.retangulo = retangulo
        self.velocidade = velocidade
        self.ladoComeco = ladoComeco.lower()
        self.batida = False

    def desenha_asteroide(self):
        janela.blit(self.imagem,self.retangulo)

    def atualiza_posicao(self):
        global bateu
        global listaAsteroides
        if self.retangulo.colliderect(jogador.rect) and not self.batida:
            bateu += 5
            self.batida = True
        if self.ladoComeco == "direita":
            self.retangulo.x -= self.velocidade

            if self.retangulo.x < - 100:
                self.retangulo.x = 800
                self.batida = False

        if self.ladoComeco == "esquerda":
            self.retangulo.x += self.velocidade

            if self.retangulo.x > 900:
                self.retangulo.x = 0
                self.batida = False
                
def desenha_retangulo_conteiner_palavra():
    pygame.draw.rect(janela,(21,0,80),(25,475,750,100),border_radius=90)

def desenha_retangulo_conteiner_contador():
    pygame.draw.rect(janela,(28,130,173),(330,25,120,70),border_radius=90)

def caminho_arquivo(nome:str):
    caminho = os.path.dirname(os.path.realpath(__file__))
    caminhoAbsoluto = os.path.join(caminho, "assets/", nome)
    return caminhoAbsoluto

def escreve_texto(texto,fonte,corTexto,posicaoX,posicaoY):
    textoEscrito = fonte.render(texto,True,corTexto)
    janela.blit(textoEscrito,(posicaoX,posicaoY))

def escreve_texto_envelopado(superficie, texto, fonteTexto, corTexto, retanguloTexto, margem, corRetanguloConteiner, aa=False):
    y = retanguloTexto.top

    # altura da fonte fornecida com base em uma string de exemplo
    fontHeight = fonteTexto.size("Tg")[1]

    pygame.draw.rect(janela,corRetanguloConteiner,retanguloTexto)

    # enquanto tiver texto a ser processado
    while texto:
        i = 1
        
        # Acha o tamanho maximo que o retangulo conporta na sua largura a propria interação nao for maior que o texto analizada
        while fonteTexto.size(texto[:i])[0] < (retanguloTexto.width - (margem * 2)) and i < len(texto):
            i += 1

        # Se o texto ja foi envelopado ele procura pela ultima aparição do " " ente as palavras e começa aleitura de là
        if i < len(texto):
            i = texto.rfind(" ", 0, i) + 1

        # Renderiza o pequeno pedaço do texto
        textoRenderizado = fonteTexto.render(texto[:i], aa, corTexto)

        superficie.blit(textoRenderizado, (retanguloTexto.left + margem, y + margem))
        # Move o texto para a linha de baixo
        y += fontHeight + 2

        # Remove o texto do string original
        texto = texto[i:]

def jogo():
    global jogando
    jogando = True

def informacaozinha():
    global informacao
    informacao = True

def sairzinho():
    global Jogar
    Jogar = False

# sorteia a palavra que será usada
def sorteia_palavra():
    with open("palavras.txt", encoding="utf-8 ") as arquivo: # Lê o arquivo na forma de "utf-8"
        palavras = arquivo.readlines() # Lê cada linha do arquivo e guarda elas em uma lista
        palavras = list(map(str.strip, palavras)) # Remove possiveis espaços em brancono inicio e no final da lista
        palavraSorteada = random.choice(palavras).upper() # padroniza a palavra sorteada para que todas as letras sejam minusculas

    return palavraSorteada

def normaliza(texto):
    normalizada = unicodedata.normalize('NFD', texto) # Usa a função unicodedata com a opção de normalização "Normalização Canônica Decomposta" para tirar o cedilha e oas acento das letras
    
    return normalizada.encode('ascii', 'ignore').decode('utf-8').casefold().upper() # Converte a string para uma string composta somente de caracteres ascii e ignora os que não podem ser decodificados para tabela ascii são ignorados e em seguida os caracteres ascii são convertidos para utf-8 novamente mas sem os caracteres especiais (ç e acentos)

def retorna_menu_inicial():
    retorna_padrao()

def sairzinho():
    global jogar
    jogar = False

def sorteia_velocidade():
    numeroSorteado = random.randint(1,4)

    return numeroSorteado

def sorteia_lado():
    listaSelecao = ["esquerda","direita"]

    ladoEscolhido = random.choice(listaSelecao)

    return ladoEscolhido

def retorna_padrao():
    global contadorEsperaTextoTela
    global contadorJogandoTextoTela
    global listaRetangulos
    global listaOpcoes
    global letrasPalavra
    global listaVerificacao
    global listaAsteroides
    global jogar
    global jogando
    global informacao
    global contando
    global obtemTempoComparacao
    global venceu
    global perdeu
    global contandoJogo
    global acertouErrado
    global bateu
    global palavraSorteada
    global palavraSorteadaNormalizada
    global largura
    global xRetanguloLetraAtual
    global xRetangulosConteiners
    global backup

    contadorEsperaTextoTela = ""

    contadorJogandoTextoTela = ""

    listaRetangulos = []

    listaOpcoes = []

    letrasPalavra = []

    listaVerificacao = []

    listaAsteroides = []

    jogar = True

    jogando = False

    informacao = False

    contando = True

    obtemTempoComparacao = True

    venceu = False

    perdeu = False

    contandoJogo = True

    acertouErrado = 0

    bateu = 0

    palavraSorteada = sorteia_palavra()

    palavraSorteadaNormalizada = normaliza(palavraSorteada)

    largura = (larguraFontePalavraSorteada + 10) * len(palavraSorteada)

    xRetanguloLetraAtual = int(400 - largura / 2)

    xRetangulosConteiners = 100

    backup = xRetanguloLetraAtual

    yAsteroide = 190

    for i in range(26):
        listaRetangulos.append(pygame.Rect(xRetangulosConteiners,100,larguraFonteAlfabeto,alturaFonteAlfabeto))
        xRetangulosConteiners += 65

    for i in range(26):
    
        listaOpcoes.append(alfabeto(listaAlfabeto[i],fonteAlfabeto,listaRetangulos[i],5,larguraFonteAlfabeto,alturaFonteAlfabeto))

    for i in range(len(palavraSorteada)):
        letrasPalavra.append(letra(palavraSorteada[i],fonteLetrasPalavraSorteada,xRetanguloLetraAtual,500,larguraFontePalavraSorteada,alturaFontePalavraSorteada))

        xRetanguloLetraAtual += (larguraFontePalavraSorteada + 10)

    for i in range(1,5):
        numeroSorteado = sorteia_velocidade()
        ladoEscolhido = sorteia_lado()
        if i % 2 == 0:
            listaAsteroides.append(asteroide(pygame.Rect(800,yAsteroide,100,100),numeroSorteado,ladoEscolhido))
            yAsteroide += 75
        else:
            listaAsteroides.append(asteroide(pygame.Rect(0,yAsteroide,100,100),numeroSorteado,ladoEscolhido))
            yAsteroide += 75

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    janela = pygame.display.set_mode((800,600))

    pygame.display.set_caption("Word Zapper")

    relogio = pygame.time.Clock()

    fonte_titulo = pygame.font.SysFont("arialblack", 30)
    fonte_texto = pygame.font.SysFont("arialblack",20)

    fonteAlfabeto = pygame.font.SysFont("arialblack",40)
    fonteLetrasPalavraSorteada = pygame.font.SysFont("arialblack",40)

    fonteContadorEspera = pygame.font.SysFont("arialblack",60)

    larguraFonteAlfabeto = fonteAlfabeto.size("Tg")[0]
    alturaFonteAlfabeto = fonteAlfabeto.size("Tg")[1]

    larguraFontePalavraSorteada = fonteLetrasPalavraSorteada.size("Tg")[0]
    alturaFontePalavraSorteada = fonteLetrasPalavraSorteada.size("Tg")[1]

    cenario = pygame.image.load(caminho_arquivo("cenario3.jpg"))
    cenario = pygame.transform.scale(cenario,(800,600))

    cenarioVenceu = pygame.image.load(caminho_arquivo("venceu.jpg"))
    cenarioVenceu = pygame.transform.scale(cenarioVenceu,(800,600))

    cenarioPerdeu = pygame.image.load(caminho_arquivo("perdeu.jpg"))
    cenarioPerdeu = pygame.transform.scale(cenarioPerdeu,(800,600))

    naveEspera = pygame.image.load(caminho_arquivo("nave.png"))

    imagemWASD = pygame.image.load(caminho_arquivo("wasd.png"))

    imagemP = pygame.image.load(caminho_arquivo("p.png"))

    textoInfo = """Este programa foi feito usando por Matheus Marques Eiras estudante de bachalelado em Ciência da computação no Instituto Federal do Paraná campus Pinhais (IFPR - Pinhais)"""

    retanguloConteinerInformacao = pygame.Rect(50,400,700,150)

    botaoJogar = botao("jogar",250,150,300,50,jogo)
    botaoInformacoes = botao("Informações e comandos",250,250,300,50,informacaozinha)
    botaoSairMenuInicial = botao("Sair",250,350,300,50,sairzinho)

    jogarNovamente = botao("Jogar novamente?",100,350,250,50,retorna_menu_inicial)
    sairMenuFinal = botao("Sair",450,350,250,50,sairzinho)

    jogador = usuario(370,400,5)

    grupoTiros = pygame.sprite.Group()

    listaAlfabeto = list(string.ascii_uppercase)

    contadorEsperaTextoTela = ""

    contadorJogandoTextoTela = ""

    listaRetangulos = []

    listaOpcoes = []

    letrasPalavra = []

    listaVerificacao = []

    listaAsteroides = []

    jogar = True

    jogando = False
    
    informacao = False

    contando = True

    obtemTempoComparacao = True

    venceu = False

    perdeu = False

    contandoJogo = True

    acertouErrado = 0

    bateu = 0

    palavraSorteada = sorteia_palavra()

    palavraSorteadaNormalizada = normaliza(palavraSorteada)

    largura = (larguraFontePalavraSorteada + 10) * len(palavraSorteada)

    xRetanguloLetraAtual = int(400 - largura / 2)

    xRetangulosConteiners = 100

    backup = xRetanguloLetraAtual

    yAsteroide = 190

    for i in range(26):
        listaRetangulos.append(pygame.Rect(xRetangulosConteiners,100,larguraFonteAlfabeto,alturaFonteAlfabeto))
        xRetangulosConteiners += 65

    for i in range(26):
    
        listaOpcoes.append(alfabeto(listaAlfabeto[i],fonteAlfabeto,listaRetangulos[i],5,larguraFonteAlfabeto,alturaFonteAlfabeto))

    for i in range(len(palavraSorteada)):
        letrasPalavra.append(letra(palavraSorteada[i],fonteLetrasPalavraSorteada,xRetanguloLetraAtual,500,larguraFontePalavraSorteada,alturaFontePalavraSorteada))

        xRetanguloLetraAtual += (larguraFontePalavraSorteada + 10)

    for i in range(1,5):
        numeroSorteado = sorteia_velocidade()
        ladoEscolhido = sorteia_lado()
        if i % 2 == 0:
            listaAsteroides.append(asteroide(pygame.Rect(800,yAsteroide,100,100),numeroSorteado,ladoEscolhido))
            yAsteroide += 75
        else:
            listaAsteroides.append(asteroide(pygame.Rect(0,yAsteroide,100,100),numeroSorteado,ladoEscolhido))
            yAsteroide += 75

    while jogar:
        relogio.tick(100)

        janela.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                jogar = False
                exit()
            
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[K_p]:
                    jogador.volta_comeco()
                    jogando = False
                    retorna_padrao()

        if jogando:
            if venceu:
                janela.fill((0,0,0))

                janela.blit(cenarioVenceu,(0,0))

                escreve_texto("Parabens você chegou ao seu destino",fonte_titulo,(255,255,255),100,250)
                escreve_texto("Jogar novamente?",fonte_texto,(255,255,255),325,300)

                jogarNovamente.desenha_botao()
                jogarNovamente.click()

                sairMenuFinal.desenha_botao()
                sairMenuFinal.click()
                
            elif perdeu:
                janela.fill((0,0,0))

                janela.blit(cenarioPerdeu,(0,0))

                escreve_texto("Você perdeu e nao conseguiu chegar ao seu destino",fonte_titulo,(255,255,255),100,250)
                escreve_texto("Jogar novamente?",fonte_texto,(255,255,255),325,300)

                jogarNovamente.desenha_botao()
                jogarNovamente.click()

                sairMenuFinal.desenha_botao()
                sairMenuFinal.click()
                
            else:
                if obtemTempoComparacao:
                    tempoMedido = pygame.time.get_ticks()
                    obtemTempoComparacao = False

                if contando:
                    tempo = pygame.time.get_ticks()
                    medida = tempo - tempoMedido

                    if medida > 4500:
                        for i in range(len(palavraSorteada)):
                            if palavraSorteada[i] != "-":
                                letrasPalavra[i].letra = "_"
                                listaVerificacao.append("_")
                            else:
                                letrasPalavra[i].letra = "-"
                                listaVerificacao.append("-")


                        contando = False
                    
                    janela.blit(cenario,(0,0))

                    calculo = ((medida // 1000) - 3) * -1

                    x = 375

                    if calculo < 0:
                        contadorEsperaTextoTela = "Já!"
                        x = 340
                    else:
                        contadorEsperaTextoTela = str(calculo)


                    escreve_texto(contadorEsperaTextoTela,fonteContadorEspera,(28,130,173),x,250)

                    for i in range(26):         
                        listaOpcoes[i].desenha_lista_movendo()

                    desenha_retangulo_conteiner_palavra()

                    for i in range(len(palavraSorteada)):
                        letrasPalavra[i].desenha_letras()
                    
                    janela.blit(naveEspera,(370,400))
                else:

                    if contandoJogo:
                        obtemTempoComparacaoJogo = pygame.time.get_ticks()
                        contandoJogo = False

                    obtemTempoComparacaoJogoAtual = pygame.time.get_ticks()

                    calculo = 180 - ((obtemTempoComparacaoJogoAtual - obtemTempoComparacaoJogo) // 1000) - acertouErrado - bateu

                    if calculo < 1:
                        perdeu = True

                    contadorJogandoTextoTela = str(calculo)

                    janela.blit(cenario,(0,0))

                    desenha_retangulo_conteiner_contador()
                    if calculo > 100:                        
                        x = 328
                    elif calculo < 10:
                        x = 370
                    else:
                        x = 350

                    escreve_texto(contadorJogandoTextoTela,fonteContadorEspera,(255,255,255),x,15)

                    for i in range(26):         
                        listaOpcoes[i].desenha_lista_movendo()

                    desenha_retangulo_conteiner_palavra()
                    
                    for i in range(len(palavraSorteada)):
                        letrasPalavra[i].desenha_letras()
                    
                    for i in range(4):
                        listaAsteroides[i].desenha_asteroide()
                        listaAsteroides[i].atualiza_posicao()

                    jogador.move()
                    jogador.tiro()

                    grupoTiros.draw(janela)

                    grupoTiros.update()

        elif informacao:
            titulo = escreve_texto("Informaçoes e comandos",fonte_titulo,(255,255,255),300,25)
            
            janela.blit(imagemWASD,(50,90))

            escreve_texto("Use W A S D para se mover",fonte_texto,(255,255,255),300,175)

            # pygame.draw.rect(janela,(255,0,0),(50,400,700,150))

            janela.blit(imagemP,(65,225))

            escreve_texto("Presione P para voltar ao menu prinpal",fonte_texto,(255,255,255),300,285)

            escreve_texto_envelopado(janela, textoInfo, fonte_texto, (0,0,0), retanguloConteinerInformacao, 25, (100,100,100), True)

        else:

            escreve_texto("Word Zapper",fonte_titulo,(255,255,255),300,50)
            
            botaoJogar.desenha_botao()
            botaoJogar.click()

            botaoInformacoes.desenha_botao()
            botaoInformacoes.click()

            botaoSairMenuInicial.desenha_botao()
            botaoSairMenuInicial.click()

        pygame.display.update()
    
    pygame.quit()