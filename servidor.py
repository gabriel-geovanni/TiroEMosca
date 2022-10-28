
import random
import socket
import os


class Jogador:
    def __init__(self, nome, client, address):
        self.nome = nome
        self.client = client
        self.address = address
        self.vitorias = 0
        self.numero = []

class Computador:
    def __init__(self):
        self.vitorias = 0
        self.numero = []

class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8082
        self.buffer = 1024

def init():
    server = Server()

    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Iniciando servidor Tiro e Mosca\nHost: %s  Porta: %s" % (server.host, server.port))
    server.sock.bind((server.host, server.port))
    server.sock.listen(3)

    jogadores = []
    
    i=0

    print ('\nAguardando jogador{} se conectar... '.format(i+1))
    client, address = server.sock.accept() 
    data = client.recv(server.buffer) 
    nomePlayer1 = data.decode('utf-8')
    print("Jogador1 se conectou.\nNome: {}\n".format(nomePlayer1))
    jogadores.append(Jogador(nomePlayer1, client, address))
    print ('\nAguardando tipo do jogo... ')
    data = jogadores[0].client.recv(server.buffer) 
    tipo = data.decode('utf-8')
    print("Tipo do jogo: {}\n".format(tipo))
    while len(jogadores) < 2:
        print("Tipo do jogo1: {}\n".format(tipo))
        if tipo == 'vsplayer': 
            
            print("Tipo do jogo2: {}\n".format(tipo))
            print ('Aguardando jogador2 se conectar... ')
            client, address = server.sock.accept() 
            data = client.recv(server.buffer) 
            jogador = data.decode('utf-8').split('-')
            jogadores.append(Jogador(jogador[0], client, address))
            tipo2 = jogadores[1].client.recv(server.buffer)
            print("Jogador2 se conectou.\nNome: {}\n".format(jogador[0]))
            while len(jogadores) == 2 and tipo2.decode('utf-8') == 'vsplayer':
                retorno = gameMultiplayer(jogadores, server)
                if retorno == 0:
                    jogadores.clear()

        elif tipo == 'singleplayer': 
            print ('\nSINGLEPLAYER SELECT... ')
            retorno = gameSinglePlayer(jogadores, server)
            if retorno == 0:
                jogadores.clear()
        elif tipo == 'vsia': 
            print ('\nSINGLEPLAYER VS IA SELECT... ')
            retorno = gameSinglePlayerVsIA(jogadores, server)
            if retorno == 0:
                jogadores.clear()
        else:
            break


             
def gameSinglePlayer(jogadores, server):
    os.system('cls' if os.name == 'nt' else'clear')
    jogadores[0].client.send('start'.encode('utf-8'))
    
    print("\nIniciando partida...")
    data = jogadores[0].client.recv(server.buffer)
    comando = data.decode('utf-8')
    if comando == 'iniciar':
        numero = gerarNumero([])
        print("NUMERO IA ==> {} {} {}".format(numero[0], numero[1], numero[2]))
        while True:
            data1 = jogadores[0].client.recv(server.buffer)
            jogada = data1.decode('utf-8').split('-')
            print(jogada)
            tiroJogador = 0
            moscaJogador = 0
            for i in range(3):
                    if int(jogada[i]) == numero[i]:
                        moscaJogador += 1
                    else:
                        for j in range(3):
                            if int(jogada[i]) == numero[j]:
                                tiroJogador += 1
            
            print("Resultado jogador: ", tiroJogador, "T", moscaJogador, "M\n")
            if moscaJogador == 3:
                print("JOGADOR VENCEU!!!")
                jogadores[0].client.send("vitoria".encode('utf-8'))
                data = jogadores[0].client.recv(server.buffer)
                if data.decode('utf-8') == '1':
                    jogadores[0].vitorias += 1
                    gameSinglePlayer(jogadores, server)
                break
            else:
                jogadores[0].client.send((str(tiroJogador) + "T" + str(moscaJogador) + "M").encode('utf-8'))
                moscaJogador = 0
                tiroJogador = 0
                jogada = []   

    return 0
             
def gameSinglePlayerVsIA(jogadores, server):
    os.system('cls' if os.name == 'nt' else'clear')
    jogadores[0].client.send('start'.encode('utf-8'))
    
    print("\nIniciando partida...")
    jogadores[0].client.recv(server.buffer)
    data = jogadores[0].client.recv(server.buffer)
    numJogador = data.decode('utf-8').split('-')
    numeroIA = gerarNumero([])
    print("NUMERO JOGADOR ==> {} {} {}".format(numJogador[0], numJogador[1], numJogador[2]))
    print("NUMERO IA ==> {} {} {}".format(numeroIA[0], numeroIA[1], numeroIA[2]))
    jogadores[0].client.send("start".encode('utf-8'))

    numerosExcluidos  = []
    while True:
        data1 = jogadores[0].client.recv(server.buffer)
        jogada = data1.decode('utf-8').split('-')
        print(jogada)
        tiroJogador = 0
        moscaJogador = 0
        tiroIA =0
        moscaIA = 0
        for i in range(3):
                if int(jogada[i]) == numeroIA[i]:
                    moscaJogador += 1
                else:
                    for j in range(3):
                        if int(jogada[i]) == numeroIA[j]:
                            tiroJogador += 1
        


        jogadaIA = gerarNumero(numerosExcluidos)
        for i in range(3):
            if jogadaIA[i] == numJogador[i]:
                moscaIA += 1
            else:
                for j in range(3):
                    if jogadaIA[i] == numJogador[j]:
                        tiroIA += 1
        
        if moscaIA == 0 and tiroIA == 0:
            numerosExcluidos.append(jogadaIA[0])
            numerosExcluidos.append(jogadaIA[1])
            numerosExcluidos.append(jogadaIA[2])


        jogadores[0].client.send("{}-{}-{}-{}-{}-{}-{}".format(jogadaIA[0], jogadaIA[1], jogadaIA[2],tiroIA, moscaIA, tiroJogador, moscaJogador).encode('utf-8'))
        if moscaJogador == 3 and moscaIA == 3:
            print("EMPATE!!!")
            break

        print("Resultado jogador: ", tiroJogador, "T", moscaJogador, "M")
        print("Resultado IA: ", tiroIA, "T", moscaIA, "M\n")
        if moscaJogador == 3:
            print("JOGADOR VENCEU!!!")
            break
        else:
            moscaJogador = 0
            tiroJogador = 0
            jogada = []   


        if moscaIA == 3:
            print("IA VENCEU!!!")
            break
        else:
            moscaIA= 0
            tiroIA = 0
            jogadaIA = []   
    
    return 0
             
def gameMultiplayer(jogadores, server):
    os.system('cls' if os.name == 'nt' else'clear')
    jogadores[0].client.send('start'.encode('utf-8'))
    
    print("\nIniciando partida...")
    jogadores[0].client.recv(server.buffer)
    data = jogadores[0].client.recv(server.buffer)
    numJogador = data.decode('utf-8').split('-')

    jogadores[1].client.send('start'.encode('utf-8'))
    jogadores[1].client.recv(server.buffer)
    data = jogadores[1].client.recv(server.buffer)
    numJogador2 = data.decode('utf-8').split('-')

    print("NUMERO JOGADOR ==> {} {} {}".format(numJogador[0], numJogador[1], numJogador[2]))
    print("NUMERO JOGADOR 2 ==> {} {} {}".format(numJogador2[0], numJogador2[1], numJogador2[2]))
    i = 0
    while True:
        if i > 0:
            jogadores[0].client.recv(server.buffer)
        jogadores[0].client.send("start".encode('utf-8'))
        data1 = jogadores[0].client.recv(server.buffer)
        jogada = data1.decode('utf-8').split('-')
        if i > 0:
            jogadores[1].client.recv(server.buffer)
        jogadores[1].client.send("start".encode('utf-8'))
        data2 = jogadores[1].client.recv(server.buffer)
        jogada2 = data2.decode('utf-8').split('-')
        print(jogada)
        tiroJogador = 0
        moscaJogador = 0
        tiroJogador2 =0
        moscaJogador2 = 0
        for i in range(3):
            if jogada[i] == numJogador2[i]:
                moscaJogador += 1
            else:
                for j in range(3):
                    if jogada[i] == numJogador2[j]:
                        tiroJogador += 1

        for i in range(3):
            if jogada2[i] == numJogador[i]:
                moscaJogador2 += 1
            else:
                for j in range(3):
                    if jogada2[i] == numJogador[j]:
                        tiroJogador2 += 1
        

        jogadores[0].client.send("{}-{}-{}-{}-{}-{}-{}".format(jogada2[0], jogada2[1], jogada2[2],tiroJogador2, moscaJogador2, tiroJogador, moscaJogador).encode('utf-8'))
        jogadores[1].client.send("{}-{}-{}-{}-{}-{}-{}".format(jogada[0], jogada[1], jogada[2],tiroJogador, moscaJogador, tiroJogador2, moscaJogador2).encode('utf-8'))
        if moscaJogador == 3 and moscaJogador2 == 3:
            print("EMPATE!!!")
            break

        print("Resultado jogador: ", tiroJogador, "T", moscaJogador, "M")
        print("Resultado jogador 2: ", tiroJogador2, "T", moscaJogador2, "M\n")
        if moscaJogador == 3:
            print("JOGADOR 1 VENCEU!!!")
            break
        else:
            moscaJogador = 0
            tiroJogador = 0
            jogada = []   


        if moscaJogador2 == 3:
            print("JOGADOR 2 VENCEU!!!")
            break
        else:
            moscaJogador2= 0
            tiroJogador2 = 0
            jogada2 = []   
        i += 1
    
    return 0


def gerarNumero(numerosExcluidosIA):
    exist = 0
    rangeList = [0,1,2,3,4,5,6,7,8,9]
    
    print("Numeros excluido:", numerosExcluidosIA)
    for i in range(len(numerosExcluidosIA)):
        rangeList.remove(numerosExcluidosIA[i])
    
    while exist == 0:
        number = random.sample(rangeList, 3)
        exist = 1

        if number[0] == number[1] or number[0] == number[2] or number[1] == number[2] or number[0] == 0:
            exist = 0

    return number


init()