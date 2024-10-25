import pygame
import sys
from pacman import ejecutar_Juego
# Iniciar programa

pygame.init()

# Definicion de colores

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)

# Pantalla

pantalla = pygame.display.set_mode((900, 950))
pygame.display.set_caption("Pacman Menu")

fuente = pygame.font.SysFont("Impact regular", 55)

opcionesMenu = ["Jugar", "Modo de Juego: Clasico", "Salir"]
opcionSeleccionada = 0
modoDeJuego = "Clasico"

imagenTituloClasico = pygame.image.load('Recursos/Menus/PacmanTitulo.png')
imagenTituloTigre = pygame.image.load('Recursos/Menus/PacmanMondeVil.png')
imagenTitulo = imagenTituloClasico

# Musica

pygame.mixer.music.load('Recursos/Audio/PacmanMenu.mp3') 
pygame.mixer.music.play(-1)  # -1 para que la musica se reproduzca en bucle

def cambiarModoDeJuego():
    global modoDeJuego, imagenTitulo
    if modoDeJuego == "Clasico":
         modoDeJuego = "El Tigre"
         imagenTitulo = imagenTituloTigre
         pygame.mixer.music.stop()
         pygame.mixer.music.load('Recursos/Audio/El Gato Callejero Main.mp3')
         pygame.mixer.music.play(-1)
    else:
         modoDeJuego = "Clasico"
         imagenTitulo = imagenTituloClasico
         pygame.mixer.music.stop()
         pygame.mixer.music.load('Recursos/Audio/PacmanMenu.mp3')
         pygame.mixer.music.play(-1)

opcionesMenu[1] = f"Modo de Juego: {modoDeJuego}"

def menu():
    pantalla.fill(NEGRO)

    tituloRect = imagenTitulo.get_rect(center=(pantalla.get_width() // 2, 200))
    pantalla.blit(imagenTitulo, tituloRect)

    for i, opcion in enumerate(opcionesMenu):
        color = AMARILLO if i == opcionSeleccionada else BLANCO
        textoSuperficie = fuente.render(opcion, True, color)

        textoRect = textoSuperficie.get_rect(center=(pantalla.get_width() // 2, 450 + i * 100))
        pantalla.blit(textoSuperficie, textoRect)

    
    pygame.display.flip()

def menuPrincipal():
    global opcionSeleccionada, modoDeJuego
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
                         
                         #iniciarJuego(modoDeJuego)  # Llamada al juego con el modo seleccionado
                         pantalla.fill(NEGRO)
                         ejecutar_Juego()
                         pygame.display.flip()

                     elif opcionSeleccionada == 1:  # Cambiar modo de juego
                         cambiarModoDeJuego()
                         opcionesMenu[1] = f"Modo de Juego: {modoDeJuego}"
                     elif opcionSeleccionada == 2:  # Salir
                         pygame.quit()
                         sys.exit()

        pygame.time.wait(100)

if __name__ == "__main__":
    menuPrincipal()