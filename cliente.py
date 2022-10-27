import socket
import os

class Conexao():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8082
        self.buffer = 1024

def conectar(): 
    server = Conexao()
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Conectando \nHost: %s   Porta: %s" % (server.host, server.port)) 
    server.sock.connect((server.host, server.port)) 
    try: 
        nome = input('\nPara começar, \ninforme o seu nome: ')
        server.sock.sendall('{}'.format(nome).encode('utf-8'))
        print("\nMENU")
        print("-----------------------------------")
        print("\t1 - Singleplayer")
        print("\t2 - VS Player")
        print("\t3 - VS IA")
        print("\t4 - Sair")
        print("-----------------------------------")
        opcao = int(input("Escolha uma opção:"))
        if opcao == 1:
            server.sock.sendall('singleplayer'.encode('utf-8'))
            server.sock.recv(server.buffer) 
            gameSingleplayer(server)
        elif opcao == 2:
            server.sock.sendall('vsplayer'.encode('utf-8'))
            server.sock.recv(server.buffer) 
            gameMultiplayer(server)
        elif opcao == 3:
            server.sock.sendall('vsia'.encode('utf-8'))
            server.sock.recv(server.buffer)
            gameSinglePlayerIA(server)
        elif opcao == 4:
            server.sock.sendall('sair'.encode('utf-8'))
            server.sock.recv(server.buffer)
            print("Saindo...")
            server.sock.close()
            exit()
        else:
            exit()


        print ("Finalizando conexão com o servidor...") 
        server.sock.close() 

    except Exception as e: 
        print ("Erro na execução: %s" %str(e)) 

def gameSingleplayer(server):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniciando partida Singleplayer\n\n")

    ## aguardando servidor gerar o numero
    server.sock.sendall('iniciar'.encode('utf-8'))

    while True:
        jogada = []
        index = 1
        while len(jogada) < 3:
            try:
                validation = int(input("Informe {}º digito do seu oponente: ".format(index)))
                if validation not in (0,1,2,3,4,5,6,7,8,9):
                    print("Digito não aceito")
                elif len(jogada) != 0 or (len(jogada) == 0 and validation != 0):
                    jogada.append(validation)
                    index += 1
                else:
                    print("O primeiro número não pode ser 0")


            except ValueError:
                print('O número não pode ser vazio')
        
        server.sock.sendall('{}-{}-{}'.format(jogada[0], jogada[1],jogada[2]).encode('utf-8'))
        resposta = server.sock.recv(server.buffer)
        
        print("{}\n===========================\n".format(resposta.decode('utf-8')))
        if(resposta.decode('utf-8') == 'vitoria'):
            print("Você ganhou!")
            print("Deseja continuar?")
            continuar = int(input("1 - Sim || 2 - Não ->"))
            server.sock.sendall('{}'.format(continuar).encode('utf-8'))
            if continuar == 1:
                server.sock.recv(server.buffer)
                gameSingleplayer(server)
            break
            


def gameSinglePlayerIA(server):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniciando partida Singleplayer\n\n")

    ## aguardando servidor gerar o numero
    server.sock.sendall('iniciar'.encode('utf-8'))

    numero = []
    index = 0
    while len(numero) < 3:
        try:
            validation = int(input("Informe {}º digito: ".format(index)))
            if validation not in (0,1,2,3,4,5,6,7,8,9):
                print("Digito não aceito")
            elif len(numero) != 0 or (len(numero) == 0 and validation != 0):
                numero.append(validation)
                index += 1
            else:
                print("O primeiro número não pode ser 0")
        except ValueError:
            print('O número não pode ser vazio')
    
    server.sock.sendall('{}-{}-{}'.format(numero[0], numero[1],numero[2]).encode('utf-8'))
    print("Aguardando o servidor informar o numero...")
    resposta = server.sock.recv(server.buffer)
    print("\n===========================\nIniciando partida")
    while True:
        jogada = []
        index = 0
        while len(jogada) < 3:
            try:
                validation = int(input("Informe {}º digito do seu oponente: ".format(index)))
                if validation not in (0,1,2,3,4,5,6,7,8,9):
                    print("Digito não aceito")
                elif len(jogada) != 0 or (len(jogada) == 0 and validation != 0):
                    jogada.append(validation)
                    index += 1
                else:
                    print("O primeiro número não pode ser 0")


            except ValueError:
                print('O número não pode ser vazio')
        
        server.sock.sendall('{}-{}-{}'.format(jogada[0], jogada[1],jogada[2]).encode('utf-8'))
        print("Aguardando jogada da IA...")
        data = server.sock.recv(server.buffer)
        resposta = data.decode('utf-8').split('-')



        print("A IA jogou: {}-{}-{}".format(resposta[0], resposta[1], resposta[2]))
        print("{} T  {} M".format(resposta[3], resposta[4]))
        print("Sua jogada: {}-{}-{}".format(jogada[0], jogada[1], jogada[2]))
        print("{} T  {} M".format(resposta[5], resposta[6]))


        print("\n===========================\n")
        if(resposta[6] == '3'):
            print("Você ganhou!")
            break
        elif resposta[4] == '3':
            print("Você perdeu!")
            break


def gameMultiplayer(server):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniciando partida Multiplayer\n\n")
    print("Aguarde sua vez de jogar...")
    ## aguardando servidor gerar o numero
    server.sock.sendall('iniciar'.encode('utf-8'))

    numero = []
    index = 1
    while len(numero) < 3:
        try:
            validation = int(input("Informe {}º digito: ".format(index)))
            if validation not in (0,1,2,3,4,5,6,7,8,9):
                print("Digito não aceito")
            elif len(numero) != 0 or (len(numero) == 0 and validation != 0):
                numero.append(validation)
                index += 1
            else:
                print("O primeiro número não pode ser 0")
        except ValueError:
            print('O número não pode ser vazio')
    
    server.sock.sendall('{}-{}-{}'.format(numero[0], numero[1],numero[2]).encode('utf-8'))
    print("\n===========================\nIniciando partida")
    while True:
        print("Aguarde a sua vez...")
        resposta = server.sock.recv(server.buffer)
        jogada = []
        index = 1
        while len(jogada) < 3:
            try:
                validation = int(input("Informe {}º digito do seu oponente: ".format(index)))
                if validation not in (0,1,2,3,4,5,6,7,8,9):
                    print("Digito não aceito")
                elif len(jogada) != 0 or (len(jogada) == 0 and validation != 0):
                    jogada.append(validation)
                    index += 1
                else:
                    print("O primeiro número não pode ser 0")


            except ValueError:
                print('O número não pode ser vazio')
        
        server.sock.sendall('{}-{}-{}'.format(jogada[0], jogada[1],jogada[2]).encode('utf-8'))
        print("Aguardando jogada do outro jogador...")
        data = server.sock.recv(server.buffer)
        resposta = data.decode('utf-8').split('-')



        print("O outro player jogou: {}-{}-{}".format(resposta[0], resposta[1], resposta[2]))
        print("{} T  {} M".format(resposta[3], resposta[4]))
        print("Sua jogada: {}-{}-{}".format(jogada[0], jogada[1], jogada[2]))
        print("{} T  {} M".format(resposta[5], resposta[6]))


        print("\n===========================\n")
        if(resposta[6] == '3'):
            print("Você ganhou!")
            break
        elif resposta[4] == '3':
            print("Você perdeu!")
            break
        else:
            server.sock.sendall('continuar'.encode('utf-8'))

   
conectar()