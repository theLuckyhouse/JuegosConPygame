#! Importamos librerias 
import pygame
import sys

# Iniciarlizar pygame 
pygame.init()

#Variables 
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO,ALTO))
WHITE = (255,255,255)
BLACK = (0,0,0)
reloj = pygame.time.Clock()

#Player 
playerSize= 20
playerx = 50
playery = 50
player = pygame.Rect(playerx,playery,playerSize,playerSize)
Speedplayer = 2

paredes = [
    pygame.Rect(0,0,800,10),
    pygame.Rect(0,590,800,10),
    pygame.Rect(0,0,10,600),
    pygame.Rect(790,0,10,600),
]

def revColision(player,paredes):
    for pared in paredes: 
        if player.colliderect(pared):
            return True 
    return False

while True:
    reloj.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Teclado     
    teclas = pygame.key.get_pressed()
    
    if teclas [pygame.K_LEFT]:
        player.x -= Speedplayer     
    if teclas [pygame.K_RIGHT]:
        player.x += Speedplayer     
    if teclas [pygame.K_DOWN]:
        player.y += Speedplayer     
    if teclas [pygame.K_UP]:
        player.y -= Speedplayer     
    
    #Cheko de colisiones 
    if revColision(player,paredes):
        if teclas [pygame.K_LEFT]:
            player.x += 4     
        if teclas [pygame.K_RIGHT]:
            player.x -= 4     
        if teclas [pygame.K_DOWN]:
            player.y -= 4     
        if teclas [pygame.K_UP]:
            player.y += 4     
    
        
    #Pintar Pantalla
    ventana.fill(WHITE)# Dibujamos la pantalla    
    pygame.draw.rect(ventana,BLACK,player)     
    
    for pared in paredes:
        pygame.draw.rect(ventana,BLACK,pared)
            
    #Pantalla
    pygame.display.flip()
    
    
    