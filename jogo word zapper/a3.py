import string
import pygame
from pygame.locals import *
from sys import exit
import os
from pathlib import Path
from pygame.sprite import Sprite

class Usuario:
    def __init__(self, posicao_inicial_x, posicao_inicial_y, velocidade):
        self.nave = pygame.image.load(caminho_arquivo("nave.png"))
        self.rect = pygame.Rect(posicao_inicial_x, posicao_inicial_y, self.nave.get_width(), self.nave.get_height())
        self.rect.topleft = posicao_inicial_x, posicao_inicial_y
        self.velocidade = velocidade

        self.tiro_disparado = False

    def move(self):
        janela.blit(self.nave, self.rect)

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
            if self.rect.y >= 560:
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
            tiro = Disparo(self.rect.center[0], self.rect.top)
            grupoTiros.add(tiro)

            self.tiro_disparado = True
        elif not pygame.key.get_pressed()[K_SPACE]:
            self.tiro_disparado = False


class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load(caminho_arquivo("tiro.png"))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 10

        if pygame.sprite.spritecollide(self, letras, True):
            self.kill()

        if self.rect.y < 0:
            self.kill()


class Botao:
    def __init__(self, texto, x, y, largura, altura, funcao):
        self.clicou = False

        self.retanguloConteiner = pygame.Rect(x, y, largura, altura)
        self.corBotao = (100, 100, 100)

        self.texto = fonte_texto.render(texto, True, (255, 255, 255))
        self.retanguloTamnhoTexto = self.texto.get_rect(center=(self.retanguloConteiner.centerx, self.retanguloConteiner.centery))

        self.funcao = funcao

    def desenha_botao(self):
        pygame.draw.rect(janela, self.corBotao, self.retanguloConteiner, border_radius=10)
        janela.blit(self.texto, self.retanguloTamnhoTexto)

    def click(self):
        mouse = pygame.mouse.get_pos()

        if self.retanguloConteiner.collidepoint(mouse):
            self.corBotao = (55, 55, 55)

            if pygame.mouse.get_pressed()[0]:
                self.clicou = True
            else:
                if self.clicou == True:
                    self.clicou = False
                    self.funcao()
        else:
            self.corBotao = (100, 100, 100)


class Letras(Sprite):
    def __init__(self, x, y, width, height, color, letter, font_size, font_color, velocidade):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

        self.font = pygame.font.Font(None, font_size)
        self.letter_surface = self.font.render(letter, True, font_color)

        self.image = self.letter_surface
        self.rect = self.image.get_rect(center=self.rect.center)

        self.velocidade = velocidade

        self.contador = 0

    def update(self):
        self.rect.x -= self.velocidade

        if self.rect.x < 0:
            self.kill()

            nova_letra = Letras(1700, 100, larguraFonte, alturaFonte, (0, 0, 0), listaAlfabeto[self.contador], 40, (255, 255, 255), 5)
            self.contador += 1
            letras.add(nova_letra)

            if self.contador > 26:
                self.contador = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def caminho_arquivo(nome):
    caminho = os.getcwd()
    caminhoAbsoluto = os.path.join(caminho, "jogo word zapper/imagens/", nome)
    caminhoAbsoluto = Path(caminhoAbsoluto)
    return caminhoAbsoluto


def escreve_texto(texto, fonte, corTexto, posicaoX, posicaoY):
    textoEscrito = fonte.render(texto, True, corTexto)
    janela.blit(textoEscrito, (posicaoX, posicaoY))


def jogo():
    global jogando
    jogando = True


def teste():
    print("teste")


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    janela = pygame.display.set_mode((800, 600))

    pygame.display.set_caption("Word Zapper")

    relogio = pygame.time.Clock()

    fonte_titulo = pygame.font.SysFont("arialblack", 30)
    fonte_texto = pygame.font.SysFont("arialblack", 20)

    fonte_alfabeto = pygame.font.SysFont("arialblack", 40)

    larguraFonte = fonte_alfabeto.size("Tg")[0]
    alturaFonte = fonte_alfabeto.size("Tg")[1]

    cenario = pygame.image.load(caminho_arquivo("cenario3.jpg"))
    cenario = pygame.transform.scale(cenario, (800, 600))

    botaoJogar = Botao("jogar", 250, 150, 300, 50, jogo)
    botaoInformacoes = Botao("Informações e comandos", 250, 250, 300, 50, teste)
    botaoSairMenuInicial = Botao("Sair", 250, 350, 300, 50, teste)

    grupoTiros = pygame.sprite.Group()

    listaAlfabeto = list(string.ascii_uppercase)

    listaRetangulos = []

    listaLetrasTela = []

    xRetangulosConteiners = 800

    letras = pygame.sprite.Group()

    for i in range(26):
        letra = Letras(xRetangulosConteiners, 100, larguraFonte, alturaFonte, (0, 0, 0), listaAlfabeto[i], 40,
                       (255, 255, 255), 5)
        letras.add(letra)
        xRetangulosConteiners += 65

    jogador = Usuario(380, 400, 5)

    jogar = True

    jogando = False

    while jogar:
        relogio.tick(100)

        janela.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                jogar = False
                exit()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[K_p]:
                    jogador.volta_comeco()
                    jogando = False

        if jogando:
            janela.blit(cenario, (0, 0))

            jogador.move()
            jogador.tiro()

            grupoTiros.draw(janela)
            letras.draw(janela)

            letras.update()
            grupoTiros.update()

        else:
            escreve_texto("Word Zapper", fonte_titulo, (255, 255, 255), 300, 50)

            botaoJogar.desenha_botao()
            botaoJogar.click()

            botaoInformacoes.desenha_botao()
            botaoInformacoes.click()

            botaoSairMenuInicial.desenha_botao()
            botaoSairMenuInicial.click()

        pygame.display.update()

    pygame.quit()
