import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# ------------------------
# CONFIG
# ------------------------

ANCHO = 1000
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Star Wars Game")

clock = pygame.time.Clock()

# ------------------------
# COLORES
# ------------------------

BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
AMARILLO = (255, 255, 100)
VERDE = (0, 255, 0)

# ------------------------
# FUENTES
# ------------------------

fuente = pygame.font.SysFont("Arial", 30)
fuente_titulo = pygame.font.SysFont("Arial", 70)

# ------------------------
# SONIDOS
# ------------------------

laser_sound = pygame.mixer.Sound("sounds/laser.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")

pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)

# ------------------------
# IMAGENES
# ------------------------

background = pygame.image.load(
    "sprites/background.jpg"
)

player_img = pygame.image.load(
    "sprites/player.png"
).convert_alpha()

enemy_img = pygame.image.load(
    "sprites/enemy.png"
).convert_alpha()

boss_img = pygame.image.load(
    "sprites/boss.jpg"
).convert()

# Sacar fondo blanco
player_img.set_colorkey((255, 255, 255))
enemy_img.set_colorkey((255, 255, 255))
boss_img.set_colorkey((255, 255, 255))

# Escalar imágenes
background = pygame.transform.scale(
    background,
    (ANCHO, ALTO)
)

player_img = pygame.transform.scale(
    player_img,
    (80, 80)
)

enemy_img = pygame.transform.scale(
    enemy_img,
    (70, 70)
)

boss_img = pygame.transform.scale(
    boss_img,
    (220, 220)
)

# ------------------------
# JUGADOR
# ------------------------

nave = pygame.Rect(100, 300, 80, 80)

velocidad = 6

vidas = 3
puntaje = 0
highscore = 0
nivel = 1

estado_juego = "menu"

# ------------------------
# DISPAROS
# ------------------------

disparos = []
disparos_enemigos = []
disparos_boss = []

ultimo_disparo = 0
cooldown_disparo = 180

# ------------------------
# EXPLOSIONES
# ------------------------

explosiones = []

# ------------------------
# POWERUPS
# ------------------------

powerups = []

rapid_fire = False
rapid_fire_timer = 0

double_shot = False
double_shot_timer = 0

# ------------------------
# BOSS
# ------------------------

boss_activo = False

boss = pygame.Rect(700, 180, 220, 220)

boss_vida = 40

boss_direccion = 1

warning_activo = False
warning_timer = 0

# ------------------------
# ENEMIGOS
# ------------------------

enemigos = []

velocidad_enemigos = 4

def crear_enemigo():

    enemigo = pygame.Rect(
        random.randint(1000, 1400),
        random.randint(50, 550),
        70,
        70
    )

    enemigos.append(enemigo)

for i in range(5):
    crear_enemigo()

# ------------------------
# ESTRELLAS
# ------------------------

estrellas = []

for i in range(100):

    estrella = [
        random.randint(0, ANCHO),
        random.randint(0, ALTO),
        random.randint(1, 3)
    ]

    estrellas.append(estrella)

# ------------------------
# MENU
# ------------------------

def mostrar_menu():

    pantalla.blit(background, (0, 0))

    titulo = fuente_titulo.render(
        "STAR WARS GAME",
        True,
        BLANCO
    )

    jugar = fuente.render(
        "PRESIONA ENTER PARA JUGAR",
        True,
        BLANCO
    )

    salir = fuente.render(
        "ESC PARA SALIR",
        True,
        BLANCO
    )

    pantalla.blit(titulo, (180, 180))
    pantalla.blit(jugar, (300, 320))
    pantalla.blit(salir, (390, 380))

    pygame.display.update()

# ------------------------
# LOOP PRINCIPAL
# ------------------------

while True:

    # ------------------------
    # MENU
    # ------------------------

    if estado_juego == "menu":

        mostrar_menu()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    estado_juego = "jugando"

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        clock.tick(60)

        continue

    # ------------------------
    # EVENTOS
    # ------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ------------------------
    # MOVIMIENTO
    # ------------------------

    teclas = pygame.key.get_pressed()

    # Disparo automático manteniendo SPACE
    tiempo_actual = pygame.time.get_ticks()

    if teclas[pygame.K_SPACE]:

        cooldown_actual = 80 if rapid_fire else cooldown_disparo

        if tiempo_actual - ultimo_disparo > cooldown_actual:

            laser_sound.play()

            disparo = pygame.Rect(
                nave.x + 70,
                nave.y + 35,
                25,
                6
            )

            disparos.append(disparo)

            # Doble disparo
            if double_shot:

                disparo2 = pygame.Rect(
                    nave.x + 70,
                    nave.y + 55,
                    25,
                    6
                )

                disparos.append(disparo2)

            ultimo_disparo = tiempo_actual

    if teclas[pygame.K_w]:
        nave.y -= velocidad

    if teclas[pygame.K_s]:
        nave.y += velocidad

    if teclas[pygame.K_a]:
        nave.x -= velocidad

    if teclas[pygame.K_d]:
        nave.x += velocidad

    nave.x = max(0, min(ANCHO - nave.width, nave.x))
    nave.y = max(0, min(ALTO - nave.height, nave.y))

    # ------------------------
    # FONDO
    # ------------------------

    pantalla.blit(background, (0, 0))

    # Estrellas
    for estrella in estrellas:

        estrella[0] -= estrella[2]

        if estrella[0] < 0:
            estrella[0] = ANCHO
            estrella[1] = random.randint(0, ALTO)

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (estrella[0], estrella[1]),
            estrella[2]
        )

    # ------------------------
    # PLAYER
    # ------------------------

    pantalla.blit(player_img, (nave.x, nave.y))

    # ------------------------
    # DISPAROS JUGADOR
    # ------------------------

    for disparo in disparos[:]:

        disparo.x += 15

        pygame.draw.rect(
            pantalla,
            ROJO,
            disparo,
            border_radius=5
        )

        if disparo.x > ANCHO:
            disparos.remove(disparo)

        # Colision enemigos
        for enemigo in enemigos[:]:

            if disparo.colliderect(enemigo):

                explosion_sound.play()

                explosiones.append([
                    enemigo.centerx,
                    enemigo.centery,
                    30
                ])

                enemigos.remove(enemigo)

                if disparo in disparos:
                    disparos.remove(disparo)

                puntaje += 1

                # Activar boss
                if (
                    puntaje >= 15
                    and nivel == 1
                    and not boss_activo
                    and not warning_activo
                ):

                    warning_activo = True
                    warning_timer = pygame.time.get_ticks()

                # Powerup
                if random.randint(1, 5) == 1:

                    tipo = random.choice([
                        "vida",
                        "rapid",
                        "double"
                    ])

                    powerup = {
                        "rect": pygame.Rect(
                            enemigo.x,
                            enemigo.y,
                            30,
                            30
                        ),
                        "tipo": tipo
                    }

                    powerups.append(powerup)

                # Dificultad progresiva
                if puntaje % 5 == 0:
                    velocidad_enemigos += 0.5

                if not boss_activo and not warning_activo:
                    crear_enemigo()

    # ------------------------
    # ENEMIGOS
    # ------------------------

    for enemigo in enemigos[:]:

        enemigo.x -= velocidad_enemigos

        pantalla.blit(enemy_img, (enemigo.x, enemigo.y))

        # Disparo enemigo
        if random.randint(1, 120) == 1:

            disparo_enemigo = pygame.Rect(
                enemigo.x,
                enemigo.y + 30,
                20,
                5
            )

            disparos_enemigos.append(disparo_enemigo)

        # Escapa pantalla
        if enemigo.x < -100:

            enemigos.remove(enemigo)

            vidas -= 1

            if not boss_activo and not warning_activo:
                crear_enemigo()

        # Colision jugador
        if enemigo.colliderect(nave):

            explosion_sound.play()

            enemigos.remove(enemigo)

            vidas -= 1

            if not boss_activo and not warning_activo:
                crear_enemigo()

    # ------------------------
    # DISPAROS ENEMIGOS
    # ------------------------

    for disparo in disparos_enemigos[:]:

        disparo.x -= 10

        pygame.draw.rect(
            pantalla,
            AMARILLO,
            disparo,
            border_radius=5
        )

        if disparo.x < 0:
            disparos_enemigos.remove(disparo)

        if disparo.colliderect(nave):

            explosion_sound.play()

            vidas -= 1

            if disparo in disparos_enemigos:
                disparos_enemigos.remove(disparo)

    # ------------------------
    # WARNING BOSS
    # ------------------------

    if warning_activo:

        texto_warning = fuente_titulo.render(
            "WARNING BOSS INCOMING",
            True,
            ROJO
        )

        tela_warning = pygame.Surface((ANCHO, ALTO))
        tela_warning.set_alpha(80)
        tela_warning.fill((255, 0, 0))

        pantalla.blit(tela_warning, (0, 0))

        pantalla.blit(texto_warning, (80, 250))

        # Esperar 3 segundos
        if pygame.time.get_ticks() - warning_timer > 3000:

            warning_activo = False
            boss_activo = True

            enemigos.clear()

    # ------------------------
    # BOSS
    # ------------------------

    if boss_activo:

        pantalla.blit(boss_img, (boss.x, boss.y))

        # Movimiento horizontal
        boss.x += 4 * boss_direccion

        if boss.x <= 500:
            boss_direccion = 1

        if boss.x >= 750:
            boss_direccion = -1

        # Disparo boss
        if random.randint(1, 20) == 1:

            disparo = pygame.Rect(
                boss.x,
                boss.y + 100,
                35,
                10
            )

            disparos_boss.append(disparo)

        # Colision boss
        for disparo in disparos[:]:

            if disparo.colliderect(boss):

                if disparo in disparos:
                    disparos.remove(disparo)

                boss_vida -= 1

                explosion_sound.play()

        # Boss derrotado
        if boss_vida <= 0:

            boss_activo = False

            puntaje += 20

            boss_vida = 40

            nivel = 2

            for i in range(7):
                crear_enemigo()

    # ------------------------
    # DISPAROS BOSS
    # ------------------------

    for disparo in disparos_boss[:]:

        disparo.x -= 14

        pygame.draw.rect(
            pantalla,
            VERDE,
            disparo,
            border_radius=5
        )

        if disparo.x < 0:
            disparos_boss.remove(disparo)

        if disparo.colliderect(nave):

            vidas -= 1

            explosion_sound.play()

            if disparo in disparos_boss:
                disparos_boss.remove(disparo)

    # ------------------------
    # POWERUPS
    # ------------------------

    for powerup in powerups[:]:

        powerup["rect"].x -= 4

        color = BLANCO

        if powerup["tipo"] == "vida":
            color = VERDE

        elif powerup["tipo"] == "rapid":
            color = (255, 255, 0)

        elif powerup["tipo"] == "double":
            color = ROJO

        pygame.draw.rect(
            pantalla,
            color,
            powerup["rect"],
            border_radius=8
        )

        # Agarrar powerup
        if powerup["rect"].colliderect(nave):

            if powerup["tipo"] == "vida":
                vidas += 1

            elif powerup["tipo"] == "rapid":
                rapid_fire = True
                rapid_fire_timer = pygame.time.get_ticks()

            elif powerup["tipo"] == "double":
                double_shot = True
                double_shot_timer = pygame.time.get_ticks()

            powerups.remove(powerup)

        elif powerup["rect"].x < -50:
            powerups.remove(powerup)

    # ------------------------
    # EXPLOSIONES
    # ------------------------

    for explosion in explosiones[:]:

        pygame.draw.circle(
            pantalla,
            AMARILLO,
            (explosion[0], explosion[1]),
            explosion[2]
        )

        explosion[2] -= 2

        if explosion[2] <= 0:
            explosiones.remove(explosion)

    # ------------------------
    # TIMERS POWERUPS
    # ------------------------

    tiempo_actual = pygame.time.get_ticks()

    if rapid_fire:

        if tiempo_actual - rapid_fire_timer > 5000:
            rapid_fire = False

    if double_shot:

        if tiempo_actual - double_shot_timer > 5000:
            double_shot = False

    # ------------------------
    # HIGHSCORE
    # ------------------------

    if puntaje > highscore:
        highscore = puntaje

    # ------------------------
    # HUD
    # ------------------------

    texto_puntos = fuente.render(
        f"Puntaje: {puntaje}",
        True,
        BLANCO
    )

    texto_vidas = fuente.render(
        f"Vidas: {vidas}",
        True,
        BLANCO
    )

    texto_nivel = fuente.render(
        f"Nivel: {nivel}",
        True,
        BLANCO
    )

    texto_record = fuente.render(
        f"Highscore: {highscore}",
        True,
        AMARILLO
    )

    pantalla.blit(texto_puntos, (20, 20))
    pantalla.blit(texto_vidas, (20, 60))
    pantalla.blit(texto_nivel, (20, 100))
    pantalla.blit(texto_record, (20, 140))

    # Vida boss
    if boss_activo:

        pygame.draw.rect(
            pantalla,
            (80, 80, 80),
            (250, 20, 500, 35),
            border_radius=10
        )

        pygame.draw.rect(
            pantalla,
            ROJO,
            (250, 20, boss_vida * 12, 35),
            border_radius=10
        )

        texto_boss = fuente.render(
            f"BOSS HP: {boss_vida}",
            True,
            BLANCO
        )

        pantalla.blit(texto_boss, (420, 60))

    # ------------------------
    # GAME OVER
    # ------------------------

    if vidas <= 0:

        game_over = fuente.render(
            "GAME OVER - PRESIONA R",
            True,
            ROJO
        )

        pantalla.blit(game_over, (250, 280))

        pygame.display.update()

        esperando = True

        while esperando:

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_r:

                        nave.x = 100
                        nave.y = 300

                        disparos.clear()
                        disparos_enemigos.clear()
                        disparos_boss.clear()

                        enemigos.clear()
                        explosiones.clear()
                        powerups.clear()

                        vidas = 3
                        puntaje = 0
                        nivel = 1

                        velocidad_enemigos = 4

                        rapid_fire = False
                        double_shot = False

                        boss_activo = False
                        boss_vida = 40

                        warning_activo = False

                        for i in range(5):
                            crear_enemigo()

                        estado_juego = "menu"

                        esperando = False

    # ------------------------
    # UPDATE
    # ------------------------

    pygame.display.update()

    clock.tick(60)
