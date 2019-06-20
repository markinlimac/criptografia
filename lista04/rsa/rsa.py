# -*- coding: utf-8 -*-

'''
Algoritimo RSA
Autor: Marco Antônio de Lima Costa

Na parte que pede o caminho do arquivo, basta dar o comando "show" e o 
programa ira listar os caminhos de todos arquivos que estão no mesmo diretório
 
'''
#implementar para que o ascii sempre tenha o tamanho de 3, acrescentando 0 para poder voltar para char
import random
import os
import math

def inverseMultiplicative(e, fi): #algoritimo de euclides estendido para achar d que eh inverso multiplicativo de e
    modulo0 = fi
    y = 0
    x = 1

    if (fi == 1) : #resto da divisão de qualquer coisa por 1 é sempre 0
        return 0

    while (e > 1) :
        if (fi == 0):
          return("Esse numero nao possui inverso multiplicativo")
        quociente = e // fi

        moduloAntigo = fi

        fi = e % moduloAntigo #resto vira modulo nas proximas iterações
        e = moduloAntigo #dividendo vira o que antes era modulo
        moduloAntigo = y

        # Update x and y
        y = x - quociente * y
        x = moduloAntigo


    # Make x positive
    if (x < 0) :
        x = x + modulo0

    return x
    
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
    
def checkPublicKey(e, fi): #calcula MDC de fi de n e da chave publica "e"
    if e <= 1 or e >= fi:
        return 2
         
    while fi:
        e, fi = fi, e % fi
    return e

def funcaoTotiente(p, q): #calcula MMC de p-1 e q-1
    if(p > q):
        maior = p
        menor = q
        for x in range(1, menor+1):
            max = maior * x
            if max % menor == 0  and max % maior == 0:
                break
    elif(q > p):
        maior = q
        menor = p
        for x in range(1, menor+1):
            max = maior * x
            if max % menor == 0  and max % maior == 0:
                break
    return max
    
def getN(p, q):
    n = p*q
    return n

def getData(caminho):
    arq = open(caminho, "r+")
    text = arq.read()
    print('TEXTO: {}'.format(text))
    return text

def charToAscii(plainText):
    ascii = [0]*len(plainText)
    
    for i in range(len(plainText)):
        ascii[i] = ord(plainText[i])    
    return ascii

def makeMod(n, num, block):
        
    c = (block**num)%n
    return c

def saveArquive(cypherText, resposta):
    if resposta == 1:
        text = ""
        for char in cypherText:
            text = text + chr(char)
        print("TEXTO CIFRADO: {}".format(text))
        arq = open("cypher_text.txt", "w") 
        arq.write(text) #escreve o texto cifrado no arquivo cypher_text.txt 
        arq.close
    elif resposta == 2:
        text = ""
        for char in cypherText:
            text = text + chr(char)
        print("TEXTO DESCRIPTOGRAFADO: {}".format(text))
        arq = open("plain_text.txt", "w") 
        arq.write(text) #escreve o texto cifrado no arquivo cypher_text.txt 
        arq.close

def encrypt(n, e, caminho, resposta):
    plainText = getData(caminho)
    cypherText = [0]*len(plainText)
    ascii = charToAscii(plainText)

    i = 0
    for char in ascii:
        c = makeMod(n, e, char)
        cypherText[i] = c
        i = i + 1
    saveArquive(cypherText, resposta)

# def decrypt(n, d, caminho, resposta):
#     cypherText = getData(caminho)
#     digit = len(str(n))
#     makeBlock(cypherText, digit-1, n, d, resposta)

def menu(n, e, p, q, d):
    print("\n========MENU========")
    print("(1) Criptografar\n(2) Descriptografar\n(0) Sair")
    resposta = int(input("\nO que deseja fazer: "))
    
    while resposta < 0 or resposta > 2:
        print("Entrada invalida!")
        resposta = int(input("\nO que deseja fazer: "))
    
    if resposta == 0:
        print("\nOBRIGADO POR UTILIZAR ESSE PROGRAMA!\n")
        return 0
        
    if resposta == 1:
        caminho = input("Digite o caminho do arquivo que deseja criptografar: ")
        while caminho == 'show':
            path = os.path.abspath(os.path.dirname(__file__))
            dir = os.listdir(path)
            for file in dir:
                print("{}/{}".format(path,file))
            caminho = input("\nDigite o caminho do arquivo que deseja criptografar: ")
        else:
            encrypt(n, e, caminho, resposta)
            
    elif resposta == 2:
        caminho = input("Digite o caminho do arquivo que deseja descriptografar: ")
        while caminho == 'show':
            path = os.path.abspath(os.path.dirname(__file__))
            dir = os.listdir(path)
            for file in dir:
                print("{}/{}".format(path,file))
            caminho = input("\nDigite o caminho do arquivo que deseja descriptografar: ")
        else:
            encrypt(n, d, caminho, resposta)
    
def main():
    print("----------------------------RSA----------------------------")
    
    p = int(input('Digite o valor de p: '))
    while checkIsPrime(p) == False:
        p = int(input('Digite um valor de p que seja primo: '))
    
    q = int(input('Digite o valor de q: '))
    while checkIsPrime(q) == False:
        q = int(input('Digite um valor de q que seja primo: '))
    
    e = int(input('Digite o valor da chave publica "e": '))
        
    n = getN(p, q)
    fi = funcaoTotiente(p-1, q-1)
    mdc = checkPublicKey(e, fi)
    while mdc != 1:
        print("\nERRO! CHAVE PUBLICA INVALIDA")
        e = int(input('Digite novamente o valor da chave publica "e": '))
        mdc = checkPublicKey(e, fi)
    
    d = inverseMultiplicative(e, fi)
    
    men = menu(n, e, p, q, d)
    while men != 0:
        men = menu(n, e, p, q, d)
    
if __name__ == "__main__":
    main()