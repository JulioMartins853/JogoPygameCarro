import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("sons/motor.mp3")  
pygame.mixer.music.set_volume(0.3)
som_batida = pygame.mixer.Sound("sons/batida.mp3")
som_batida.set_volume(0.6)

largura = 640
altura = 480
relogio = pygame.time.Clock()
velocidade_jogo = 5

janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Corrida")
fonte = pygame.font.SysFont('arial', 40, True, True)

fundo = pygame.image.load("img/pista1.png").convert()
fundo_y1 = 0
fundo_y2 = -altura  

carro = pygame.image.load("img/carro1.png").convert_alpha()
carro = pygame.transform.scale(carro, (80, 100))

inimigo = pygame.image.load("img/cone1.png").convert_alpha()
inimigo = pygame.transform.scale(inimigo, (80, 100))

limite_esquerdo = 160
limite_direito = 400

def reiniciar_jogo():
    global x, y, x_inimigo, y_inimigo, pontos, velocidade_jogo, fundo_y1, fundo_y2, game_over
    x = largura / 2 - 50
    y = 350
    x_inimigo = randint(limite_esquerdo, limite_direito)
    y_inimigo = -120
    pontos = 0
    velocidade_jogo = 5
    fundo_y1 = 0
    fundo_y2 = -altura
    game_over = False
    pygame.mixer.music.play(-1)  

reiniciar_jogo()

rodando = True
while rodando:
    relogio.tick(60)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()
        
        if evento.type == KEYDOWN and evento.key == K_SPACE and game_over:
            reiniciar_jogo()

    if not game_over:
        
        fundo_y1 += velocidade_jogo
        fundo_y2 += velocidade_jogo
        if fundo_y1 >= altura:
            fundo_y1 = -altura
        if fundo_y2 >= altura:
            fundo_y2 = -altura

        
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT]:
            x -= 6
        if teclas[K_RIGHT]:
            x += 6
        
        if x < limite_esquerdo:
            x = limite_esquerdo
        if x > limite_direito:
            x = limite_direito

        
        y_inimigo += velocidade_jogo
        if y_inimigo > altura:
            y_inimigo = -120
            x_inimigo = randint(limite_esquerdo, limite_direito)
            pontos += 1
            velocidade_jogo += 0.3

        
        ret_jogador = pygame.Rect(x + 10, y + 10, 60, 80)
        ret_inimigo = pygame.Rect(x_inimigo + 10, y_inimigo + 20, 60, 70)
        if ret_jogador.colliderect(ret_inimigo):
            game_over = True
            pygame.mixer.music.stop()  
            som_batida.play()          
    
    
    janela.blit(fundo, (0, fundo_y1))
    janela.blit(fundo, (0, fundo_y2))
    janela.blit(carro, (x, y))
    janela.blit(inimigo, (x_inimigo, y_inimigo))

    
    texto = fonte.render(f"Km: {int(pontos)}", True, (255, 255, 255))
    janela.blit(texto, (450, 30))

    if game_over:
        mensagem = fonte.render("GAME OVER!", True, (255, 0, 0))
        msg2 = fonte.render("Pressione ESPAÇO", True, (255, 255, 255))
        janela.blit(mensagem, (160, 180))
        janela.blit(msg2, (120, 240))

    pygame.display.update()
