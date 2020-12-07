
import subprocess
import sys
import get_pip

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "installar", package])

#aqui intenta conectar con pygame para que este juego se pueda ejecutar y lo instala desde la clase get_pip
try:
    print("[JUEGO] Intentando importar pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame no esta instalado")

    try:
        print("[JUEGO] Intentando instalar pygame a través de pip")
        import pip
        install("pygame")
        print("[JUEGO] Se instaló Pygame")
    except:
        print("[EXCEPCIÓN] Pip no instalado en el sistema")
        print("[JUEGO] Intentando instalar pip")
        get_pip.main()
        print("[GAME] Pip fue instalado")
        try:
            print("[GAME] Intentando instalar pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame ha sido instalado")
        except:
            print("[ERROR 1] Pygame no se pudo instalar")


import pygame
import os
import time
from client import Network
import pickle
pygame.font.init()
#pone la imagen del menu
board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
chessbg = pygame.image.load(os.path.join("img", "ajedrez.png"))
rect = (113,113,525,525)

turn = "w"

# intanta conectar con el servidor e instanciar la imagen en un menu incicial
def menu_screen(win, name):
    global bo, chessbg
    run = True
    offline = False

    while run:
        win.blit(chessbg, (0,0))
        small_font = pygame.font.SysFont("comicsans", 50)
        
        if offline:
            off = small_font.render("Servidor fuera de linea, por favor intenta despues...", 1, (255, 0, 0))
            win.blit(off, (width / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    bo = connect()
                    run = False
                    main()
                    break
                except:
                    print("Servidor desconectado")
                    offline = True


    
def redraw_gameWindow(win, bo, p1, p2, color, ready):
    win.blit(board, (0, 0))
    bo.draw(win, color)

    formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1%60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2%60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("comicsans", 30)
    try:
        txt = font.render(bo.p1Name + "\ Tiempo: " + str(formatTime2), 1, (255, 255, 255))
        txt2 = font.render(bo.p2Name + "\ Tiempo: " + str(formatTime1), 1, (255,255,255))
    except Exception as e:
        print(e)
    win.blit(txt, (520,10))
    win.blit(txt2, (520, 700))

    txt = font.render("presiona Q para rendirte :)", 1, (255, 255, 255))
    win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("modo espectador", 1, (255, 0, 0))
        win.blit(txt3, (width/2-txt3.get_width()/2, 10))

    if not ready:
        show = "esperando jugador"
        if color == "s":
            show = "esperando jugador"
        font = pygame.font.SysFont("comicsans", 80)
        txt = font.render(show, 1, (255, 0, 0))
        win.blit(txt, (width/2 - txt.get_width()/2, 300))

    if not color == "s":
        font = pygame.font.SysFont("comicsans", 30)
        if color == "w":
            txt3 = font.render("Eres el blanco", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font.render("eres el negro", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 10))

        if bo.turn == color:
            txt3 = font.render("tu turno", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))
        else:
            txt3 = font.render("tu turno", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))

    pygame.display.update()


#El módulo de fuentes permite representar fuentes TrueType en un nuevo objeto Surface. Acepta cualquier carácter
#UCS-2 ('u0001' a 'uFFFF'). Este módulo es opcional y requiere SDL_ttf como dependencia. Debe probar que el módulo
#pygame.fontpygame para cargar y representar fuentes está disponible e inicializado antes de intentar usar el módulo.

def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text,1, (255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False


def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2]/8))
            j = int(divY / (rect[3]/8))
            return i, j

    return -1, -1


def connect():
    global n
    n = Network()
    return n.board


def main():
    global turn, bo, name

    color = bo.start_user
    count = 0

    bo = n.send("update_moves")
    bo = n.send("nombre " + name)
    clock = pygame.time.Clock()
    run = True

    while run:
        if not color == "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
        except Exception as e:
            print(e)
            end_screen(win, "el otro jugador salio")
            run = False
            break

        if not color == "s":
            if p1Time <= 0:
                bo = n.send("ganador b")
            elif p2Time <= 0:
                bo = n.send("ganador w")

            if bo.check_mate("b"):
                bo = n.send("ganador b")
            elif bo.check_mate("w"):
                bo = n.send("ganador w")

        if bo.winner == "w":
            end_screen(win, "El jugador blanco ha ganado!")
            run = False
        elif bo.winner == "b":
            end_screen(win, "El jugador negro ha ganado!")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            #Este módulo contiene funciones para manejar el teclado. El módulo pygame.eventpygame para interactuar con los
            #eventos y la cola de colas obtiene los eventos pygame.KEYDOWN y pygame.KEYUP cuando se presionan y sueltan los
            #botones del teclado. Ambos eventos tienen atributos clave y mod. clave: un ID entero que representa cada tecla del teclado
             #mod: una máscara de bits de todas las teclas modificadoras que estaban presionadas cuando ocurrió el evento
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and color != "s":
                    # quit game
                    if color == "w":
                        bo = n.send("ganador b")
                    else:
                        bo = n.send("ganador w")

                if event.key == pygame.K_RIGHT:
                    bo = n.send("forward")

                if event.key == pygame.K_LEFT:
                    bo = n.send("back")

            #Cuando se establece el modo de visualización, la cola de eventos comenzará a recibir eventos del mouse. Los botones del
            #mouse generan eventos pygame.MOUSEBUTTONDOWN y pygame.MOUSEBUTTONUP cuando se presionan y sueltan. Estos eventos contienen
            #un atributo de botón que representa qué botón se presionó. La rueda del mouse generará eventos pygame.MOUSEBUTTONDOWN y
            #pygame.MOUSEBUTTONUP cuando se mueva. El botón se establecerá en 4 cuando se suba la rueda y en el botón 5 cuando se baje
            #la rueda. Siempre que se mueve el mouse, se genera un evento pygame.MOUSEMOTION. El movimiento del
            #mouse se divide en eventos de movimiento pequeños y precisos. A medida que el mouse se mueve, muchos eventos
            #de movimiento se colocarán en la cola. Los eventos de movimiento del mouse que no se limpian correctamente
            #de la cola de eventos son la razón principal por la que la cola de eventos se llena.

            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    bo = n.send("update moves")
                    i, j = click(pos)
                    bo = n.send("selecionar " + str(i) + " " + str(j) + " " + color)
    
    n.disconnect()
    bo = 0
    menu_screen(win)


name = input("Por favor ingrese su nombre: ")
width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("JUEGO DE AJEDREZ")
menu_screen(win, name)
