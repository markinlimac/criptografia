from random import randint
from math import gcd as bltin_gcd
from sha1 import sha1

import sys
sys.path.insert(0, '..')
import elipticAlgorithym



def hash_to_int(hash, order):
    number = 0

    for char in hash:
        number += ord(char)

    number = number % order
    return number
    


def modular_inverse(k, order):

    for number in range(order):
        result = (k * number) % order

        # print('Numero ' , number, ': ', result)

        if result == 1: 
            return number
    
    number = 1
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


def sum_points(pointP, pointQ, a, order):
    Xp, Yp = pointP
    Xq, Yq = pointQ

    if pointP != pointQ:
        dividendo = (Yq-Yp) % order
        divisor = (Xq-Xp) % order
        delta = (dividendo*extend_euclids_function(divisor, order)) % order
    elif pointP == pointQ:
        dividendo = (3*(Xp**2)+a) % order
        divisor = (2*Yp) % order
        delta = (dividendo*extend_euclids_function(divisor, order)) % order

    Xr = ((delta**2) - Xp - Xq) % order
    Yr = (delta*(Xp-Xr) - Yp) % order
    resultado = (Xr, Yr)

    return resultado



def calculate_k(order):
    
    rand = 0
    while not bltin_gcd(rand, int(order)) == 1:
        rand = randint(1, order-1)

    return rand



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



def check_has_files():
    try:
        with open('public_key.txt') as file:
            file.readline()
    except:
        print("\n\n\tArquivo 'public_key.txt' não existe, ele deve ser gerado pela opção B\n\n")
        return False


    try:
        with open('signature_pair.txt') as file:
            file.readline()

    except:
        print("\n\n\tArquivo 'signature_pair.txt' não existe, ele deve ser gerado pela opção B\n\n")
        return False

    return True





def generate(PointG, order, p, a, questao):
    print('-------------------- GERANDO ASSINATURA DIGITAL -------------------- ')

    # PointG = (Gx, Gy)

    d = randint(1, order-1)                         # Chave Privada
    PointQ = multiply_ponit(d, PointG, p, a)        # Chave Publica

    with open('public_key.txt', 'w') as f:
                print(PointQ, file=f)

    repeat = True
    while repeat == True:
        repeat = False

        # Passo 1: Calcula K
        k = calculate_k(order)


        # Passo 2: P = (x, y) = kG and r = x mod order
        P = multiply_ponit(k, PointG, p, a)
        r = P[0] % order

        if r==0:
            repeat = True
            continue


        # Passo 3: Calcule t = K^-1 mod order
        t  = modular_inverse(k, order)


        # Passo 4: Calcule e (hash da mensagem como inteiro)
        if questao == 'questao_a':
            message = input("\nDigite a mensagem para a qual deseja criar a assinatura digital:  ")
        elif questao == 'questao_b':
            with open('message.txt') as file:
                message = file.read()
                # print("\n\nMensagem: ", message)
        
        hash_160_bits = sha1(message)
        e = hash_to_int(hash_160_bits, order)
        # print('\n\n\nE: ', e, '\n\n')



        # Passo 5: Calcula S
        s = t*(e + d*r) % order

        if s==0:
            repeat = True
            continue


        # Passo 6: A assinatura é o par R e S
        with open('signature_pair.txt', 'w') as f:
            print("r=", r, file=f)
            print("s=", s, file=f)

            print("\n\nA assinatura digital da mensagem")
            print("\n\t\"" + message + "\"")
            print("\n\t\tencontra-se no arquivo 'signature_pair.txt'.\n\n\n")


    return message




def authenticate(pointG, order, p, a, message=False):
    print('-------------------- AUTENTICANDO -------------------- ')

    # Passo 1: Checar se R e S estão entre 1 e Order-1
    print('\n\nPasso 1: Checando se R e S possuem os valores aceitos.')

    with open('signature_pair.txt') as file:
        r = int(file.readline().split(" ", 1)[1].rsplit(" ", 1)[0])
        s = int(file.readline().split(" ", 1)[1].rsplit(" ", 1)[0])
    
    if not (1 <= r <= order-1) or not (1 <= s <= order-1):
        print('\n\n\tPar de assinatura inválido. \n\tAo menos um dos valores de R e S no arquivo "signature_pair.txt" está inválidos')
        return
        

    # Passo 2: Calcule e
    print('Passo 2: Calculando o valor de e.')

    if not message:
        with open('message.txt') as file:
            message = file.read()
    
    hash_160_bits = sha1(message)
    e = hash_to_int(hash_160_bits, order)


    # Passo 3: Calcule w
    print('Passo 3: Calculando o valor de w.')

    w = modular_inverse(s, order)


    # Passo 4: Caular u1 e u2
    print('Passo 4: Calculando o valor de u1 e u2.')

    u1 = e*w
    u2 = r*w

    # Passo 5: Calcule o ponto X
    print('Passo 5: Calculando o valor do ponto X.')

    with open('public_key.txt') as file:
            content = file.read()
            pointQ = (int(content[1]), int(content[4]))
    
    u1_times_G = multiply_ponit(u1, pointG, p, a)
    u2_times_Q = multiply_ponit(u2, pointQ, p, a)
    X = sum_points(u1_times_G, u2_times_Q, a, order)

    # Passo 6: Calcular V caso X não seja identidade
    print('Passo 6: Calculando o valor de v.')

    if X==(0,0):
        print("\n\n\t\tAssinatura Rejeitada!\n\n\n\n")
        return

    v = X[0] % order

    # Passo 7: Cheque se v = r
    print('Passo 7: Verificando se v é igual a r, caso seja, a mensagem é autentica.')

    if(v == r):
        print("\n\n\t\t Mensagem autenticada!\n\n\n\n")
    else:
        print("\n\n\t\t Autenticação Negada!\n\n\n\n")        
    

    return