import pygame
import sys
from constantes import *
from controladorJuego import ControladorJuego
import config

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
    global imagenTitulo
    if config.modoDeJuego == "Clasico":
         config.modoDeJuego = "El Tigre"
         imagenTitulo = imagenTituloTigre
         pygame.mixer.music.stop()
         pygame.mixer.music.load('Recursos/Audio/El Gato Callejero Main.mp3')
         pygame.mixer.music.play(-1)
    else:
         config.modoDeJuego = "Clasico"
         imagenTitulo = imagenTituloClasico
         pygame.mixer.music.stop()
         pygame.mixer.music.load('Recursos/Audio/PacmanMenu.mp3')
         pygame.mixer.music.play(-1)

opcionesMenu[1] = f"Modo de Juego: {config.modoDeJuego}"

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


pausado = False

def menuPrincipal():
    juego = ControladorJuego()
    global opcionSeleccionada, pausado
    jugando = True

    while jugando:
        menu()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pausado = not pausado  # Cambia el estado de pausa
                    if pausado:
                        resultado = menuPausa()
                        if resultado == "menu_inicial":
                            return  # Reinicia desde menuPrincipal
                    else:
                        pygame.mixer.music.unpause()
                
                # Navegación en el menú principal
                elif evento.key == pygame.K_s:
                    opcionSeleccionada = (opcionSeleccionada + 1) % len(opcionesMenu)
                elif evento.key == pygame.K_w:
                    opcionSeleccionada = (opcionSeleccionada - 1) % len(opcionesMenu)
                elif evento.key == pygame.K_RETURN:
                    if opcionSeleccionada == 0:  # Jugar
                        pygame.mixer.music.stop()
                        juego.iniciarJuego()
                        while True:
                            # for evento in pygame.event.get():
                            #     if evento.type == pygame.QUIT:
                            #         pygame.quit()
                            #         sys.exit()
                            #     elif config.pausado == True:
                            #         config.pausado = True
                            #         resultado = menuPausa()
                            #         if resultado == "menu_inicial":
                            #             return
                            juego.actualizar()

                    elif opcionSeleccionada == 1:
                        cambiarModoDeJuego()
                        opcionesMenu[1] = f"Modo de Juego: {config.modoDeJuego}"
                    elif opcionSeleccionada == 2:
                        silenciar()
                    elif opcionSeleccionada == 3:
                        pygame.quit()
                        sys.exit()

# def menuPausa():
#     opcionesPausa = ["Continuar", "Menu Inicial", "Guardar y Salir"]
#     seleccionPausa = 0

#     while True:
#         pantalla.fill(NEGRO)
#         for i, opcion in enumerate(opcionesPausa):
#             color = AMARILLO if i == seleccionPausa else BLANCO
#             textoSuperficie = fuente.render(opcion, True, color)
#             textoRect = textoSuperficie.get_rect(center=(pantalla.get_width() // 2, 200 + i * 50))
#             pantalla.blit(textoSuperficie, textoRect)

#         pygame.display.flip()

#         for evento in pygame.event.get():
#             if evento.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif evento.type == pygame.KEYDOWN:
#                 if evento.key == pygame.K_w:
#                     seleccionPausa = (seleccionPausa - 1) % len(opcionesPausa)
#                 elif evento.key == pygame.K_s:
#                     seleccionPausa = (seleccionPausa + 1) % len(opcionesPausa)
#                 elif evento.key == pygame.K_RETURN:
#                     if seleccionPausa == 0:  # Continuar
#                         return
#                     elif seleccionPausa == 1:  # Menú inicial
#                         menuPrincipal()
#                     elif seleccionPausa == 2:  # Salir
#                         pygame.quit()
#                         sys.exit()
#                 elif evento.key == pygame.K_ESCAPE:
#                     return

if __name__ == "__main__":
    menuPrincipal()
