import pygame
import sys
from constantes import *
from controladorJuego import ControladorJuego

pygame.init()

# Definicion de colores

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)

# Pantalla

pantalla = pygame.display.set_mode(TAMANNOPANTALLA, 0, 32)
pygame.display.set_caption("Pacman Menu")

fuente = pygame.font.Font('Recursos/Fuentes/PressStart2P-Regular.ttf', 20)

opcionesMenu = ["Jugar", "Modo de Juego: Clasico", "Silenciar musica: no","Salir"]
opcionSeleccionada = 0
MODODEJUEGO = "Clasico"
musica_Activada = True

imagenTituloClasico = pygame.image.load('Recursos/Menus/PacmanTitulo.png')
imagenTituloClasico = pygame.transform.scale(imagenTituloClasico, (400, 150))
imagenTituloTigre = pygame.image.load('Recursos/Menus/PacmanMondeVil.png')
imagenTituloTigre = pygame.transform.scale(imagenTituloTigre, (400, 150))
imagenTitulo = imagenTituloClasico

# Musica

pygame.mixer.music.load('Recursos/Audio/PacmanMenu.mp3') 
pygame.mixer.music.play(-1)  # -1 para que la musica se reproduzca en bucle

def cambiarModoDeJuego():
    global MODODEJUEGO, imagenTitulo
    if MODODEJUEGO == "Clasico":
         MODODEJUEGO = "El Tigre"
         imagenTitulo = imagenTituloTigre
         pygame.mixer.music.stop()
         pygame.mixer.music.load('Recursos/Audio/El Gato Callejero Main.mp3')
         pygame.mixer.music.play(-1)
    else:
         MODODEJUEGO = "Clasico"
         imagenTitulo = imagenTituloClasico
         pygame.mixer.music.stop()
         pygame.mixer.music.load('Recursos/Audio/PacmanMenu.mp3')
         pygame.mixer.music.play(-1)

opcionesMenu[1] = f"Modo de Juego: {MODODEJUEGO}"

def silenciar():
    global musica_Activada
    if musica_Activada:
        pygame.mixer.music.pause()
        opcionesMenu[2] = "Silenciar musica: si" 
    else:
        pygame.mixer.music.unpause()
        opcionesMenu[2] = "Silenciar musica: no"
    musica_Activada = not musica_Activada    


def menu():
    pantalla.fill(NEGRO)

    tituloRect = imagenTitulo.get_rect(center=(pantalla.get_width() // 2, 120))
    pantalla.blit(imagenTitulo, tituloRect)

    for i, opcion in enumerate(opcionesMenu):
        color = AMARILLO if i == opcionSeleccionada else BLANCO
        textoSuperficie = fuente.render(opcion, True, color)

        textoRect = textoSuperficie.get_rect(center=(pantalla.get_width() // 2, 300 + i * 50))
        pantalla.blit(textoSuperficie, textoRect)

    
    pygame.display.flip()

def menuPrincipal():
    juego = ControladorJuego()
    global opcionSeleccionada, MODODEJUEGO
    jugando = True

    while jugando:
        menu()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    opcionSeleccionada = (opcionSeleccionada + 1) % len(opcionesMenu)
                elif evento.key == pygame.K_w:
                    opcionSeleccionada = (opcionSeleccionada - 1) % len(opcionesMenu)

                elif evento.key == pygame.K_RETURN:
                     if opcionSeleccionada == 0:  # Jugar
                        pygame.mixer.music.stop()
                        juego.iniciarJuego()
                        while True:
                            juego.actualizar()

                     elif opcionSeleccionada == 1:  # Cambiar modo de juego
                         cambiarModoDeJuego()
                         opcionesMenu[1] = f"Modo de Juego: {MODODEJUEGO}"
                     elif opcionSeleccionada == 2: #silenciar musica
                         silenciar()
                     elif opcionSeleccionada == 3:  # Salir
                         pygame.quit()
                         sys.exit()

        pygame.time.wait(100)

if __name__ == "__main__":
    menuPrincipal()