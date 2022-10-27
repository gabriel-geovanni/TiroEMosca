import random

def computador(numerosExcluidosIA):
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

class game():
    tiroJogador = 0
    moscaJogador = 0
    tiroIA = 0
    moscaIA = 0
    jogador = []
    numeroIA = []
    end = 0
    jogada = []
    jogadaIA = []
    numerosExcluidosIA = []
    vencedor = []
    numeroIA = computador(numerosExcluidosIA)
    print(numeroIA)
    rangeList = [0,1,2,3,4,5,6,7,8,9]
    index = 1
    while len(jogador) < 3:
        try:
            validation = int(input("Informe {}º digito: ".format(index)))
            if validation not in (0,1,2,3,4,5,6,7,8,9):
                print("Numero nao aceito")
            elif len(jogador) != 0 or (len(jogador) == 0 and validation != 0):
                jogador.append(validation)
                index += 1
            else:
                print("O primeiro número não pode ser 0")
        except ValueError:
            print('O número não pode ser vazio')        

    index = 1
    while(end == 0):
        try:
            while len(jogada) < 3:
                validation = int(input("Informe o digito {}º do openente: ".format(index)))
                if validation not in (0,1,2,3,4,5,6,7,8,9):
                    print("Número não aceito")
                elif len(jogada) != 0 or (len(jogada) == 0 and validation != 0):
                    jogada.append(validation)
                    index += 1
                else:
                    print("O primeiro número não pode ser 0")

            for i in range(3):
                if jogada[i] == numeroIA[i]:
                    moscaJogador += 1
                else:
                    for j in range(3):
                        if jogada[i] == numeroIA[j]:
                            tiroJogador += 1

      
        except ValueError:
            print('O número não pode ser vazio') 

        print("Resultado jogador: ", tiroJogador, "T", moscaJogador, "M\n")
        if moscaJogador == 3:
            print("JOGADOR VENCEU!!!")
            break
        else:
            index = 1
            moscaJogador = 0
            tiroJogador = 0
            jogada = []       


        jogadaIA = computador(numerosExcluidosIA)
        numeroDeMoscaDaRodadaIA = 0
        for i in range(3):
            if jogadaIA[i] == jogador[i]:
                moscaIA += 1
            else:
                for j in range(3):
                    if jogadaIA[i] == jogador[j]:
                        tiroIA += 1              
        
        print("Resultado IA: ", tiroIA, "T", moscaIA, "M\n")
        if moscaIA == 3:
            print("IA VENCEU!!!")
            break
        else:
            if tiroIA == 0 and moscaIA == 0:
                for i in range(3):
                    numerosExcluidosIA.append(jogadaIA[i])
            moscaIA = 0
            tiroIA = 0
            jogadaIA = []       





