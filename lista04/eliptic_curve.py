pontoInfinito = (0,0)
import random

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

def extend_euclids_function(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return x0

def makeSum(pontoP, x, y, p, a):
    pontoQ = (x, y)
    Xp, Yp = pontoP
    
    if pontoP == pontoInfinito:
        resultado = pontoQ
    elif pontoQ == pontoInfinito:
        resultado = pontoP
    elif Xp == x and (Yp == (-y) % p):
        resultado = pontoInfinito
    else:
        if pontoP != pontoQ:
            lambd = ((y - Yp)*extend_euclids_function((x - Xp), p))%p
            x3 = int((lambd**2 - Xp - x)%p)
            y3 = int((lambd*(Xp - x3) - Yp)%p)
        elif pontoP == pontoQ:
            lambd = ((3*(Xp**2) + a)*extend_euclids_function((2*Yp), p))%p
            x3 = int((lambd**2 - Xp - x)%p)
            y3 = int((lambd*(Xp - x3) - Yp)%p)         
        resultado = (x3, y3)
    
    return resultado

def getOrder(x, y, p, a):
    ordem = 1
    ponto = (x,y)
    while ponto != pontoInfinito:
        ponto = makeSum(ponto, x, y, p, a)
        ordem += 1
    return ordem
    
def checkRoot(a, b): #checa se realmente a curva é uma curva nao-singular, se nao possui raizes multiplas 
    if (4*(a**3) + 27*(b**2)) != 0:
        root = True
    else:
        root = False
    
    return root
        
def calcRoot(a, b, p):
    contador = 0
    listOrdem = []
    listPonto = []
    
    for x in range(p):
        for y in range(p):
            if (y**2)%p == (x**3 + a*x + b)%p:
                contador += 1
                ponto = (x,y)
                ordem = getOrder(x, y, p, a)
                listOrdem.append(ordem)
                listPonto.append(ponto)
                print('Ponto ({}, {}) Ordem: {}'.format(x,y,ordem))
    
    lista = [value for value in list(zip(listOrdem, listPonto))]            
    lista.sort()
    ordem, pontox, pontoy = str(lista[-1]).split(',')
    print("\nPonto de maior ordem ({},{}) possui ordem igual a {}".format(pontox.split('(')[1], pontoy.split(')')[0], ordem.split('(')[1]))            
    print("Numero total de pontos:",contador) #todos os pontos mais o ponto no infinito
        
    
def menu():
    print("------------CURVA ELIPTICA------------")
    a = int(input("Digite o valor de a: "))
    b = int(input("Digite o valor de b: "))
    root = checkRoot(a, b)
    while root == False:
        print("\nEssa curva possui raízes multiplas\n")
        a = int(input("Digite o valor de a: "))
        b = int(input("Digite o valor de b: "))
        root = checkRoot(a, b)
    p = int(input("Digite o valor de p: "))
    prime = checkIsPrime(p)
    while prime == False:
        print("\nP nao é primo\n")
        p = int(input("Digite o valor de p: "))
        prime = checkIsPrime(p)
    print("")
    
    return a, b, p 
    
if __name__ == "__main__":
    a, b, p = menu()
    calcRoot(a, b, p)