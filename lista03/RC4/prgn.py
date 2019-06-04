import random
import os

MOD = 256


def KSA(key):

    key_length = len(key)
    S = range(MOD)  # [0,1,2, ... , 255]
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values
        
    return S


def PRGA(S):
    
    quantidade = int(input("Qaul a quantidade de bits que deseja gerar?: "))
    
    i = 0
    j = 0
    res = []
    for k in range(quantidade):
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % MOD]
        val = ("%02X" %  k)
        res.append(val)
    bitsream = ''.join(res)
    bitsream = bitsream.decode('hex')
    print(bitsream)


def get_keystream(key):
    
    S = KSA(key)
    PRGA(S)


def encrypt(key):
    
    key = [ord(c) for c in key]

    get_keystream(key)

def makePassword():
    keylength = random.randint(1,32)

    caracters = '0123456789ABCDEFGHIJKLMNOPQRSTUWVXZabcdefghijlmnopqrstuwvxz$./-'
    senha = ''
    for char in range(keylength*8): #No range de keylength
        senha += random.choice(caracters) #Escolhe um caracter aleatoriamente e adiciona ao final da senha
    
    return senha

def main():
    
    key = makePassword()
    ciphertext = encrypt(key)

if __name__ == '__main__':
    main()