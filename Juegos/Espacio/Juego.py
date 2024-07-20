#* Importamos librerías
import pygame
import random

#! Constantes
WIDTH = 800  ## Ancho
HEIGHT = 600  ## Alto
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
aparicionEnemy = 60  ## Frecuencia de aparición de enemigos

#! Funciones de Inicio
pygame.init()  ## Activa la librería
pygame.mixer.init()  ## Activación de sonido

#* VARIABLES
ventana = pygame.display.set_mode((WIDTH, HEIGHT))  ## Definimos la ventana
pygame.display.set_caption("StarWars")  ## Nombre del Juego
reloj = pygame.time.Clock()  ## Reloj
enemigos = []
bullets = []
score = 0
gameOver = False  ## Estado del juego

#! Ajustes Generales

#* Jugador
playerImagen = pygame.image.load("./asset/nave.png")  ## Cargamos una imagen (Personaje)
playerImagen.set_colorkey(BLACK)  ## Quita el Fondo
playerImagen = pygame.transform.scale(playerImagen, (50, 50))  ## Redimensionar imagen
playerPosicion = playerImagen.get_rect()  ## Posición de la imagen
playerPosicion.centerx = WIDTH // 2  ## Posición de aparición (Ancho)
playerPosicion.bottom = HEIGHT - 10  ## Posición de aparición (Alto)

#* Fondo
imagenFondo = pygame.image.load("./asset/Blue Nebula 8 - 1024x1024.png").convert()  ## Carga de la imagen de fondo

#* Enemigo
enemyImage = pygame.image.load("./asset/meteor.png").convert()
enemyImage = pygame.transform.scale(enemyImage, (50, 50))  ## Redimensionar imagen
enemyImage.set_colorkey(BLACK)  ## Quita el Fondo

#* Bala
bulletImage = pygame.image.load("./asset/laser1.png").convert()
bulletImage.set_colorkey(BLACK)  ## Quita el Fondo
bulletImage = pygame.transform.scale(bulletImage, (10, 20))

#* Sonido
balasSonido = pygame.mixer.Sound("./asset/laser5.ogg") ## Sonido de balas
explosionSonido = pygame.mixer.Sound("./asset/explosion.wav") ## Sonido de explosión
pygame.mixer.music.load("./Musica/POP.mp3") ## Música de fondo
pygame.mixer.music.set_volume(0.2) ## Volumen de la música

#! Funciones

#* Player
def actualizarPlayer():
    playerVelocidad = 0
    
    teclaPush = pygame.key.get_pressed()
    if teclaPush[pygame.K_LEFT]:
        playerVelocidad = -5
    if teclaPush[pygame.K_RIGHT]:
        playerVelocidad = 5
    
    # Limite de desplazamiento 
    playerPosicion.x += playerVelocidad
    if playerPosicion.right > WIDTH:
        playerPosicion.right = WIDTH
    if playerPosicion.left < 0:
        playerPosicion.left = 0

#* Enemigos
def generarEnemigos():
    if random.randint(1, aparicionEnemy) == 1:  ## Probabilidad de generar un nuevo enemigo
        x = random.randrange(WIDTH - enemyImage.get_width())  ## x aleatoria dentro del ancho de la pantalla
        y = random.randrange(-100, -40)  ## y aleatoria fuera de la pantalla
        speedx = random.randrange(-5, 5)  ## Velocidad horizontal aleatoria
        speedy = random.randrange(1, 10)  ## Velocidad de caída
        enemigos.append([x, y, speedx, speedy])  ## [x, y, velocidadX, velocidadY]

def actualizarEnemigos():
    for enemigo in enemigos[:]:
        enemigo[0] += enemigo[2]  ## Actualiza x (Horizontalmente)
        enemigo[1] += enemigo[3]  ## Actualiza y (Verticalmente)

        # Reiniciar la posición del enemigo
        if enemigo[1] > HEIGHT + 10 or enemigo[0] < -25 or enemigo[0] > WIDTH + 22:
            enemigo[0] = random.randrange(WIDTH - enemyImage.get_width())
            enemigo[1] = random.randrange(-100, -40)
            enemigo[3] = random.randrange(1, 4)  ## Velocidad aleatoria

def dibujarEnemigos(ventana):
    for enemigo in enemigos:
        ventana.blit(enemyImage, (enemigo[0], enemigo[1]))

def colisionJugadorMeteoros():
    for enemigo in enemigos:
        enemigo_rect = pygame.Rect(enemigo[0], enemigo[1], enemyImage.get_width(), enemyImage.get_height())  ## Rectángulo del enemigo
        if playerPosicion.colliderect(enemigo_rect):
            return True  ## Colisión detectada
    return False  ## Sin colisión

#* Disparos
def dispararBala():
    bulletRect = pygame.Rect(playerPosicion.centerx - bulletImage.get_width() // 2, playerPosicion.top - bulletImage.get_height(), bulletImage.get_width(), bulletImage.get_height())
    bullets.append(bulletRect)
    balasSonido.play()

def actualizarBalas():
    for bullet in bullets[:]:
        bullet.y -= 10  ## Mover la bala hacia arriba
        
        #! Eliminar la bala si sale de la pantalla
        if bullet.bottom < 0:
            bullets.remove(bullet)

def colisionBalasEnemigos():
    global enemigos, bullets, score
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet.x, bullet.y, bulletImage.get_width(), bulletImage.get_height())
        for enemigo in enemigos[:]:
            enemigo_rect = pygame.Rect(enemigo[0], enemigo[1], enemyImage.get_width(), enemyImage.get_height())
            if bullet_rect.colliderect(enemigo_rect):
                enemigos.remove(enemigo)
                bullets.remove(bullet)
                score += 10  ## Incrementar el puntaje en 10
                explosionSonido.play()
                break

def dibujarBalas(ventana):
    for bullet in bullets:
        ventana.blit(bulletImage, bullet.topleft)

#* Dibujar Texto
def dibujarTexto(ventana, texto, tamaño, x, y):
    fuente = pygame.font.SysFont(None, tamaño)
    textos = fuente.render(texto, True, WHITE) ## Texto y color
    textoPosicion = textos.get_rect() ## Tamaño de texto
    textoPosicion.midtop = (x, y)
    ventana.blit(textos, textoPosicion)

#* Pantalla de Game Over
def mostrarGameOver(ventana):
    ventana.fill(BLACK)  ## Fondo negro
    dibujarTexto(ventana, "GAME OVER", 60, WIDTH // 2, HEIGHT // 2 - 30)
    dibujarTexto(ventana, f"Puntaje Final: {score}", 40, WIDTH // 2, HEIGHT // 2 + 30)
    dibujarTexto(ventana, "Presiona R para Reiniciar o Q para Salir", 30, WIDTH // 2, HEIGHT // 2 + 90)
    pygame.display.flip()

#* Reiniciar el Juego
def reiniciarJuego():
    #! Reiniciamos variables
    global enemigos, bullets, score, playerPosicion, gameOver
    enemigos = []
    bullets = []
    score = 0
    playerPosicion = playerImagen.get_rect()  ## Posición de la imagen
    playerPosicion.centerx = WIDTH // 2  ## Posición de aparición (Ancho)
    playerPosicion.bottom = HEIGHT - 10  ## Posición de aparición (Alto)
    gameOver = False

#! Bucle principal 
running = True
pygame.mixer.music.play(loops=-1)

while running:
    if gameOver:
        mostrarGameOver(ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reiniciarJuego()
                elif event.key == pygame.K_q:
                    running = False
    else:
        reloj.tick(60)  ## FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dispararBala()

        actualizarPlayer()
        generarEnemigos()
        actualizarEnemigos()
        actualizarBalas()
        colisionBalasEnemigos()
        
        #* Colisiones 
        if colisionJugadorMeteoros():
            gameOver = True  ## Termina el juego si hay una colisión

        #* Dibujos 
        ventana.blit(imagenFondo, (0, 0))  ## Dibujar imagen de fondo
        ventana.blit(playerImagen, playerPosicion)  ## Dibujar jugador
        dibujarEnemigos(ventana)
        dibujarBalas(ventana) 
        
        dibujarTexto(ventana, str(score), 25, WIDTH // 2, 10)
        
        pygame.display.flip()

pygame.quit()
