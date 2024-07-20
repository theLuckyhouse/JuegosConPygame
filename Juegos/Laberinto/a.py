#* Importamos librerias
import pygame
import sys

#* Cosntantes 
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#!Ajuste Generales 
pygame.init() ## Inicializar Pygame
pygame.mixer.init() ##incializar Musica
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberinto")
victory = False

# Definir el jugador
sizePlayer = 20 ## Tamaño
player = pygame.Rect(50, 50, sizePlayer, sizePlayer) ## Forma

# trofeo
trofeo = pygame.Rect(700, 500, 20, 20)


#* Paredes del laberinto (coordenadas de las figuras)
walls = [
    pygame.Rect(0, 10, 800, 20),
    pygame.Rect(0, 580, 800, 20),
    pygame.Rect(0, 10, 20, 600),
    pygame.Rect(780, 10, 20, 600),
]

# Configuracion
clock = pygame.time.Clock()
speedPlayer = 2
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#* FUNCIONES
def moverPlayer(keys, player):
    if keys[pygame.K_LEFT]:
        player.x -= speedPlayer
    if keys[pygame.K_RIGHT]:
        player.x += speedPlayer
    if keys[pygame.K_UP]:
        player.y -= speedPlayer
    if keys[pygame.K_DOWN]:
        player.y += speedPlayer
        
    global victory
    if player.colliderect(trofeo):
        victory = True

def detectarColision(player, walls):
    for wall in walls:
        if player.colliderect(wall): ## colliderect funcion para reconocer colisiones
            player.x = 50
            player.y = 50
            return True
    return False
#--------------------------------------------------------------------------------------------------------------

while True:
    
    # Configurar el frame rate
    clock.tick(30)
    
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Mover al jugador
    moverPlayer(keys, player)

    # Comprobar colisiones y evitar el movimiento a través de las paredes
    if detectarColision(player, walls):
        if keys[pygame.K_LEFT]:
            player.x += speedPlayer
        if keys[pygame.K_RIGHT]:
            player.x -= speedPlayer
        if keys[pygame.K_UP]:
            player.y += speedPlayer
        if keys[pygame.K_DOWN]:
            player.y -= speedPlayer

    # Dibujar en la pantalla
    ventana.fill(WHITE)
    pygame.draw.rect(ventana, RED, player)
    pygame.draw.ellipse(ventana, BLACK, trofeo)

    for wall in walls:
        pygame.draw.rect(ventana, BLACK, wall)

        # Mostrar mensaje de victoria si se ha ganado
    if victory:
        Fuente = pygame.font.Font(None, 36)
        texto = Fuente.render("¡Has ganado!", True, BLACK)
        textRect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        ventana.blit(texto, textRect)
        
    # Actualizar la pantalla
    pygame.display.flip()