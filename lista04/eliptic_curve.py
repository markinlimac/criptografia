#achar o ponto no infinito 
#somar varias vezes todos os pontos ate chegar no ponto no infinito e fazer um contador para que conte quantas vezes foi somado (ordem do ponto)
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

def getInfinitPoint(x, y, xanterior, yanterior, p, a):
    y = y-(p/2) 
    yanterior = yanterior-(p/2)
    x3 = xanterior + x
    y3 = yanterior + y
    return x3, int(y3)

# def getInfinitPoint(x, y, xanterior, yanterior, p, a):
#     if xanterior != x:
#         lambd = ((y - yanterior)/(x - xanterior))%p
#         x3 = (lambd**2 - xanterior - x)%p
#         y3 = (lambd*(xanterior - x3) - yanterior)%p
#     elif xanterior == x and yanterior != 0:
#         lambd = (3*(xanterior**2) + a)/(2*yanterior)
#         x3 = (lambd**2 - 2*xanterior)%p
#         y3 = (lambd*(xanterior - x3) - yanterior)%p        
# 
#     return x3, y3
    
def checkRoot(a, b): #checa se realmente a curva é uma curva nao-singular, se nao possui raizes multiplas 
    if (4*(a**3) + 27*(b**2)) != 0:
        root = True
    else:
        root = False
    
    return root
        
def calcRoot(a, b, p):
    contador = 0
    
    for x in range(p):
        for y in range(p):
            if (y**2)%p == (x**3 + a*x + b)%p:
                contador += 1
                if contador == 1:
                    xanterior = x
                    yanterior = y
                if contador == 2:
                    x3,y3 = getInfinitPoint(x, y, xanterior, yanterior, p, a) #calcular o ponto no infinito a partir de pontos simetricos 
                print(x,y)
        
    print("Ponto no infinito: {} {}".format(x3, y3))
    print("\nNumero total de pontos:",contador+1) #todos os pontos mais o ponto no infinito
        
    
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