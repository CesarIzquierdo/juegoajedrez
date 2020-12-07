import socket
import pickle
import time

#La variable s es nuestro socket TCP / IP. AF_INET hace referencia a la familia o dominio, significa ipv4,
#en contraposición a ipv6 con AF_INET6. SOCK_STREAM significa que será un socket TCP, que es nuestro tipo de socket.
#TCP significa que estará orientado a la conexión, en lugar de sin conexión. AQUI NO SABIA QUE ERA DE FORMA CLARA ASIQ UE PUSE LA DEFINICION
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 5555
        #se usa como localhost para indicar que tiene conexion a internet
        self.addr = (self.host, self.port)
        self.board = self.connect()
        self.board = pickle.loads(self.board)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(4096*8)

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=False):
        """
        :parametro dato: str
        :return: str
        """
        #esto inicia el contador de los movimientos de los jugadores y lo muestra en el juego
        start_time = time.time()
        while time.time() - start_time < 5:
            try:
                if pick:
                    self.client.send(pickle.dumps(data))
                else:
                    self.client.send(str.encode(data))
                reply = self.client.recv(4096*8)
                try:
                    reply = pickle.loads(reply)
                    break
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)


        return reply


