
#! Importamos librerias 
import pygame 
import sys

#* Iniciarlizar pygame 
pygame.init() 

#* Variables 
ANCHO = 800
ALTO = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
ventana = pygame.display.set_mode((ANCHO,ALTO))
reloj = pygame.time.Clock()

#* Player 
playerSize= 20 ## Tamaño de player
playerx = 50 ## Coordenada x del personaje
playery = 50 ## Coordenada y del personaje

player = pygame.Rect(playerx,playery,playerSize,playerSize)
Speedplayer = 2 ## Velocidad del personaje

#* Lista que almacena los bloques/Paredes
paredes = [
    pygame.Rect(0,0,800,10),
    pygame.Rect(0,590,800,10),
    pygame.Rect(0,0,10,600),
    pygame.Rect(790,0,10,600),
]
#----------------------------------------------------------------------------------------------------

#! Funciones

"""
Esta funcion se encarga de revisar si
hay una colision entre el jugador 
y las paredes 
""" 
def revColision(player,paredes):
    for pared in paredes: 
        if player.colliderect(pared): ## Funcion colliderect detecta las colisiones
            return True 
    return False
#-----------------------------------------------------------------------------------------------------

#! Bucle Principal 

while True:
    
    reloj.tick(60) ## FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #* Teclado 
    teclas = pygame.key.get_pressed() ## asignamos la funcion de presionar tecla a una variable
    
    """"
    Movimientos:
    
    Podemos obtener la coordenada x y y del "player"
    utilizando ".x" o ".y"
    
    esos valores son tomados de la funcion de personaje 
    "pygame.Rect(playerx,playery,playerSize,playerSize)"
                    playerx y playery
    """
    
    if teclas [pygame.K_LEFT]:
        player.x -= Speedplayer     
    if teclas [pygame.K_RIGHT]:
        player.x += Speedplayer     
    if teclas [pygame.K_DOWN]:
        player.y += Speedplayer     
    if teclas [pygame.K_UP]:
        player.y -= Speedplayer     
    
    
    """
    
    En esta sección nos encargamos de asignar una acción cuando se detecta una colisión. 
    En el caso del ejemplo:

    1. Revisamos qué tecla estamos pulsando.
    2. Al detectar una colisión, se asigna un nuevo movimiento al jugador.
    
    El nuevo movimiento del jugador es la distancia que recorre originalmente 
    (por ejemplo, 2 píxeles) al pulsar la tecla, pero al detectar una colisión, 
    se realiza un movimiento con una operación contraria (por ejemplo, -2 píxeles).

    Ejemplo:
    Si al pulsar la tecla D aumentamos +2 píxeles, al detectar una colisión disminuiríamos -2 píxeles:
                                2 - 2 = 0

    Esto provocaría que nuestro jugador no se pudiera mover hacia esa dirección.
    """
    if revColision(player,paredes):
        if teclas [pygame.K_LEFT]:
            player.x += 4       
        if teclas [pygame.K_RIGHT]:
            player.x -= 4     
        if teclas [pygame.K_DOWN]:
            player.y -= 4     
        if teclas [pygame.K_UP]:
            player.y += 4     
    
        
    # *Pintar Pantalla
    ventana.fill(WHITE) ## Dibujamos la pantalla    
    pygame.draw.rect(ventana,BLACK,player)     
    
    #* Bucle de dibujado de paredes
    for pared in paredes:
        pygame.draw.rect(ventana,BLACK,pared)
            
    #* Dibuja todo lo que colocamos en la ventana
    pygame.display.flip() 