# Este Archivo contiene las constantes que se utilizan en el juego para no estar repitiendo codigo y poder configurar ciertas cosas de manera mas rapidas y sencilla.

ANCHOCASILLA = 16
ALTOCASILLA = 16
FILA = 36
COLUMNA = 28
ANCHOPANTALLA = COLUMNA*ANCHOCASILLA
ALTOPANTALLA = FILA*ALTOCASILLA
TAMANNOPANTALLA = (ANCHOPANTALLA, ALTOPANTALLA)

NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
ROSADO = (255,100,150)
CYAN = (100,255,255)
NARANJA = (230,190,40)
VERDE = (0, 255, 0)

DETENER = 0
ARRIBA = 1
ABAJO = -1
IZQUIERDA = 2
DERECHA = -2
PORTAL = 3

PACMAN = 0
BOLITA = 1
BOLITAGRANDE = 2
FANTASMA = 3
BLINKY = 4
PINKY = 5
INKY = 6
CLYDE = 7
FRUTA = 8

DISPERCION = 0
PERSEGUIR = 1
ASUSTADO = 2
SPAWN = 3

PUNTAJETXT = 0
NIVELTXT = 1
INICIOTXT = 2
PAUSATXT = 3
GAMEOVERTXT = 4