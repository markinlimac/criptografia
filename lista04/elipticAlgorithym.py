import random

pontoInfinito = (0, 0)

def extend_euclids_function(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return x0

def makeSum(pointP, pointQ, a, p):
    Xp, Yp = pointP
    Xq, Yq = pointQ

    if pointP == pontoInfinito:
        result = pointQ
    elif pointQ == pontoInfinito:
        result = pointP
    elif Xp == Xq and (Yp == (-Yq) % p):
        result = pontoInfinito
    else:
        lambd = 0
        if pointP != pointQ:
            lambd = (((Yq-Yp) % p)*extend_euclids_function(((Xq-Xp) % p), p)) % p
            x3 = ((lambd**2) - Xp - Xq) % p
            y3 = (lambd*(Xp-x3) - Yp) % p
        elif pointP == pointQ:
            lambd = (((3*(Xp**2)+a) % p)*extend_euclids_function(((2*Yp) % p), p)) % p
            x3 = ((lambd**2) - Xp - Xq) % p
            y3 = (lambd*(Xp-x3) - Yp) % p
        result = (x3, y3)

    return result

def checkRoot(a, b): #checa se realmente a curva é uma curva nao-singular, se nao possui raizes multiplas 
    if (4*(a**3) + 27*(b**2)) != 0:
        root = True
    else:
        root = False
    
    return root
    
def checkIsPrime(num): #executa o algoritimo de millerrabin com 100 rounds, para saber se o numero eh primo ou nao

    if num == 2:
        return True

    if num % 2 == 0:
        return False

    r, s = 0, num - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(100):
        a = random.randrange(2, num - 1)
        x = pow(a, s, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
    return True

def getOrder(point, a, p):
    order = 1
    x, y = point
    while point != pontoInfinito:
        point = makeSum(point, (x, y), a, p)
        order += 1
    return order

def calcRoot(a, b, p):
    listOrder = []
    listPoint = []
    
    for x in range(p):
        for y in range(p):
            if (y**2)%p == (x**3 + a*x + b)%p:
                point = (x,y)
                order = getOrder(point, a, p)
                listOrder.append(order)
                listPoint.append(point)
    
    return listPoint

def makeMultiply(k, point, a, p):
    result = pontoInfinito
    pointAux = point

    for i in range(k.bit_length()): #quantidade de bits que contem k
        if (k >> i) & 1:
            result = makeSum(result, pointAux, a, p)
        pointAux = makeSum(pointAux, pointAux, a, p)
    return result

def encryption(g, pointP, public_key, a, p):
    k = int(input("\nInsira um valor inteiro aleatorio: "))

    c1 = makeMultiply(k, g, a, p)
    c2 = makeSum(pointP, makeMultiply(k, public_key, a, p), a, p)
    return (c1, c2)

def decryption(cripto, private_key, a, p):
    aux = makeMultiply(private_key, cripto[0], a, p)
    decript = makeSum(cripto[1], (aux[0],(-aux[1]) % p), a, p)
    return decript

if __name__ == '__main__':
    print("------------CRIPTOGRAFIA DE CURVA ELIPTICA------------")
    a = int(input("Insira o valor A: "))
    b = int(input("Insira o valor B: "))
    root = checkRoot(a, b)
    while root == False:
        print("\nEssa curva possui raízes multiplas\n")
        a = int(input("Digite o valor de a: "))
        b = int(input("Digite o valor de b: "))
        root = checkRoot(a, b)
    p = int(input("Insira o valor P: "))
    prime = checkIsPrime(p)
    while prime == False:
        print("\nP nao é primo\n")
        p = int(input("Digite o valor de p: "))
        prime = checkIsPrime(p)

    points = calcRoot(a, b, p)
    orders = [getOrder(point, a, p) for point in points]
    list = [value for value in list(zip(orders, points))]
    list.sort()
    order, pointx, pointy = str(list[-1]).split(',')
    point = (pointx.split('(')[1], pointy.split(')')[0])
    print("\nÉ recomendado usar o ponto G: ({},{})".format(point[0], point[1]))
    g = eval(input("\tInsira o ponto no formato (x,y): "))

    print("\nEscolha o ponto a ser cifrado, use alguns dos pontos abaixo")
    for point in points:
        print(point)
    pointP = eval(input("\tInsira o ponto no formato (x,y): "))

    public_key = eval(input("\nInsira a chave publica do destinatario para cifracao no formato (x,y): "))
    cripto = encryption(g, pointP, public_key, a, p)
    print("\nPontos C1 e C2 criptografados: ", cripto)

    pointC1 = eval(input("\nInsira o ponto C1 no formato (x,y): "))
    pointC2 = eval(input("Insira o ponto C2 no formato (x,y): "))
    cripto = (pointC1, pointC2)
    private_key = int(input("\nInsira a chave privada para decifrar: "))
    pointP = decryption(cripto, private_key, a, p)
    print("\nPonto P descriptografado: ", pointP)