import pygame
import random
import math
from pygame import mixer

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

# agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# variables del Jugador
img_jugador = pygame.image.load("nave.png")
img_jugador = pygame.transform.scale(img_jugador,(100,100))
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.6)
    enemigo_y_cambio.append(50)

# variables de la bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 5
bala_visible = False


# puntaje
puntaje = 0
fuente = pygame.font.SysFont(None, 32)
texto_x = 10
texto_y = 10

# texto final de juego
fuente_final = pygame.font.SysFont(None, 40)


def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))


# funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# fucion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# fucion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 34, y + 10))


# funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego

# Inicializar lista de enemigos vivos
enemigos_vivos = [True] * cantidad_enemigos

se_ejecuta = True
while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    jugador_x += jugador_x_cambio
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            elif evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            elif evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                # Dispara una bala
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad_x": 0,
                    "velocidad_y": -5
                }
                balas.append(nueva_bala)

        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicación de las balas
    for bala in balas:
        bala["y"] += bala["velocidad_y"]

        # Si la bala sale de la pantalla, la eliminamos
        if bala["y"] < 0:
            balas.remove(bala)

    # Modificar ubicación de los enemigos y verificar colisiones
    for e in range(cantidad_enemigos):
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            se_ejecuta = False
            break

        # Solo mover y dibujar enemigos vivos
        if enemigos_vivos[e]:
            enemigo_x[e] += enemigo_x_cambio[e]
            if enemigo_x[e] <= 0:
                enemigo_x_cambio[e] = 1
                enemigo_y[e] += enemigo_y_cambio[e]
            elif enemigo_x[e] >= 736:
                enemigo_x_cambio[e] = -1
                enemigo_y[e] += enemigo_y_cambio[e]

            # Verificar colisiones con las balas
            for bala in balas:
                if enemigo_x[e] < bala["x"] < enemigo_x[e] + 64 and enemigo_y[e] < bala["y"] < enemigo_y[e] + 64:
                    sonido_colision = mixer.Sound("Golpe.mp3")
                    sonido_colision.play()
                    puntaje += 1
                    # Eliminar la bala
                    balas.remove(bala)
                    # Marcar al enemigo como muerto
                    enemigos_vivos[e] = False
                    break

            enemigo(enemigo_x[e], enemigo_y[e], e)

    # Dibujar balas
    for bala in balas:
        disparar_bala(bala["x"], bala["y"])

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)
     
    # Verificar si todos los enemigos han sido eliminados
    if all(not vivo for vivo in enemigos_vivos):
        texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
        pantalla.blit(texto_game_over, (300, 250))
        pygame.display.update()
        pygame.time.delay(2000)  # Esperar 2 segundos antes de salir del juego
        se_ejecuta = False
      
    pygame.display.update()









