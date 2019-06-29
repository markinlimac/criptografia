from random import randint
from math import gcd as bltin_gcd
from sha1 import sha1

import sys
sys.path.insert(0, '..')
import elipticAlgorithym


def modular_inverse(k, ordem):

    for number in range(ordem):
        result = (k * number) % ordem
        if result == 1: 
            break

    return number


def extend_euclids_function(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return x0



def multiply_ponit(k, G, p, a):
    x, y = G
    
    for times in range(k):
        dividendo = (3*(x**2)+a) % p
        divisor = (2*y) % p    
        delta = (dividendo * extend_euclids_function(divisor, p)) % p

        # print(delta)

        x = ((delta**2) - x - x) % p
        y = (delta*(x-y) - y) % p
        resultado = (x, y)

    return resultado


def calculate_k(ordem):
    
    rand = 0
    while not bltin_gcd(rand, int(ordem)) == 1:
        rand = randint(1, ordem-1)

    return rand


def generate(PointG, ordem, p, a, questao):
    print('-------------------- GERANDO ASSINATURA DIGITAL -------------------- ')

    # PointG = (Gx, Gy)

    d = 149                                         # Chave Privada
    PointQ = multiply_ponit(d, PointG, p, a)        # Chave Publica

    repeat = True
    while repeat == True:
        repeat = False

        # Passo 1: Calcula K
        k = calculate_k(ordem)

        # Passo 2: P = (x, y) = kG and r = x mod ordem
        P = multiply_ponit(k, PointG, p, a)
        r = P[0] % ordem

        if r==0:
            repeat = True
            continue

        # Passo 3: Calcule t = K^-1 mod ordem
        t  = modular_inverse(k, ordem)

        # Passo 4: Calcule Hash da mensagem
        if questao == 'questao_a':
            message = input("\nDigite a mensagem para a qual deseja criar a assinatura digital:  ")
        elif questao == 'questao_b':
            with open('message.txt') as file:
                message = file.read()
                # print("\n\nMensagem: ", message)
        
        e = sha1(message)

        # Passo 5: Calcula S
        s = t*(int(e, 16) + d*r)

        # Passo 6: A assinatura é o par R e S
        
        if questao == 'questao_b':
            with open('digital_signature.txt', 'w') as f:
                print("r= ", r, file=f)
                print("s= ", s, file=f)

                print("\n\nA assinatura digital da mensagem")
                print("\n\t\"" + message + "\"\n")
                print("\n\t\tencontra-se no arquivo 'digital_signature.txt'.")
                
                return


        return r, s, message


def get_global_params():

    a = int(input("Insira o valor A: "))
    b = int(input("Insira o valor B: "))
    root = elipticAlgorithym.checkRoot(a, b)

    while root == False:
        print("\nEssa curva possui raízes multiplas\n")
        a = int(input("Digite o valor de a: "))
        b = int(input("Digite o valor de b: "))
        root = elipticAlgorithym.checkRoot(a, b)
    
    
    p = int(input("Insira o valor P: "))
    prime = elipticAlgorithym.checkIsPrime(p)
    while prime == False:
        print("\nP nao é primo\n")
        p = int(input("Digite o valor de p: "))
        prime = elipticAlgorithym.checkIsPrime(p)


    points = elipticAlgorithym.calcRoot(a, b, p)
    orders = [elipticAlgorithym.getOrder(point, a, p) for point in points]

    temp_list = list(zip(orders, points))
    value_list = [value for value in temp_list]
    value_list.sort()

    order, pointx, pointy = str(value_list[-1]).split(',')
    point = (pointx.split('(')[1], pointy.split(')')[0])
    print("\nÉ recomendado usar o ponto G: ({},{})".format(point[0], point[1]))
    pointG = eval(input("\tInsira o ponto no formato (x,y): "))

    order = order[1:]

    return pointG, order, p, a



def check_message_file_is_not_empty():
    input("\nPrimeiramente, insira a mensagem para a qual deseja gerar a assinatura digital no arquivo 'message.py'.\n\n"
            "\t\tPara continuar pressione enter.\n\n")

    empty = True

    while empty:

        with open('message.txt') as file:
            first = file.read(1)
            if not first:
                input("\nO arquivo continua vazio!"
                        "\n\tInsira a mensagem e pressione enter.\n\n")

            else:
                empty = False
    
    return
