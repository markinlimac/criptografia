from random import randint
from math import gcd as bltin_gcd


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
    while not bltin_gcd(rand, ordem) == 1:
        rand = randint(1, ordem-1)

    return rand


def generate(Gx, Gy, ordem, p, a):
    print('\n\n\n\n\n\n-------------------- GERANDO ASSINATURA DIGITAL -------------------- ')

    PointG = (Gx, Gy)

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

        # # Passo 3: Calcule t = K^-1 mod ordem
        t  = modular_inverse(k, ordem)


        # Passo 4: Calcule Hash da mensagem
        message = input("\nDigite a mensagem para a qual deseja criar a assinatura digital:  ")
        print(message)



        

    
    