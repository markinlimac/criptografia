#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os

MOD = 256


def KSA(key):
    ''' Key Scheduling Algorithm (from wikipedia):
        for i from 0 to 255
            S[i] := i
        endfor
        j := 0
        for i from 0 to 255
            j := (j + S[i] + key[i mod keylength]) mod 256
            swap values of S[i] and S[j]
        endfor
    '''
    key_length = len(key)
    # create the array "S"
    S = range(MOD)  # [0,1,2, ... , 255]
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values
        
    return S


def PRGA(S):
    ''' Psudo Random Generation Algorithm (from wikipedia):
        i := 0
        j := 0
        while GeneratingOutput:
            i := (i + 1) mod 256
            j := (j + S[i]) mod 256
            swap values of S[i] and S[j]
            K := S[(S[i] + S[j]) mod 256]
            output K
        endwhile
    '''
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K


def get_keystream(key):
    ''' Takes the encryption key to get the keystream using PRGA
        return object is a generator
    '''
    S = KSA(key)
    print(next(PRGA(S)))
    return PRGA(S)


def encrypt(key, plaintext):
    ''' :key -> encryption key used for encrypting, as hex string
        :plaintext -> string to encrpyt/decrypt
    '''
    key = [ord(c) for c in key]

    # Get the keystream
    keystream = get_keystream(key)

    res = []
    for c in plaintext:
        val = ("%02X" % (ord(c) ^ next(keystream)))  # XOR and taking hex
        res.append(val)
    '''
    arquivo = open('key.txt', 'r+')
    for line in arquivo:
        senha = line
    print('key = {}'.format(senha))
    '''
    return ''.join(res)


def decrypt(key, ciphertext):
    ''' :key -> encryption key used for encrypting, as hex string
        :ciphertext -> hex encoded ciphered text using RC4
    '''
    ciphertext = ciphertext.decode('hex')
    print 'ciphertext to func:', ciphertext  # optional, to see
    res = encrypt(key, ciphertext)
    return res.decode('hex')

def makePassword():
    keylength = random.randint(5,16)

    caracters = '0123456789ABCDEFGHIJKLMNOPQRSTUWVXZabcdefghijlmnopqrstuwvxz$./-'
    senha = ''
    for char in range(keylength*8): #No range de keylength
            senha += random.choice(caracters) #Escolhe um caracter aleatoriamente e adiciona ao final da senha
    
    print('chave = {}'.format(senha))
    key = open('key.txt', 'w')
    key.write(senha) #Escreve a senha no arquivo "key.txt"
    key.close
    
    return senha

def main():
    
    path = os.path.abspath(os.path.dirname(__file__)) #Acha o caminho do diretorio em que o programa esta
    dir = os.listdir(path) #Acha o diretorio em que o programa esta
    for file in dir:
        if file == "cypher_text.txt": #Caso ja exista o arquivo "cypher_text.txt" o programa exclui para não dar nenhum problema 
            os.remove(file)
            
    key = makePassword()  # plaintext
    datafile = "entrada3.txt"
    arq = open(datafile, "r+")
    plaintext = arq.read()
    # encrypt the plaintext, using key and RC4 algorithm
    ciphertext = encrypt(key, plaintext)
    print 'plaintext:', plaintext
    print 'ciphertext:', ciphertext
    arq = open("cypher_text.txt", "w")
    arq.write(ciphertext) #Escreve o texto cifrado no arquivo "cypher_text.txt" 
    arq.close
    # ..
    # Let's check the implementation
    # ..
    arquivo = open('cypher_text.txt', 'r+')
    for line in arquivo:
        ciphertext = line
    # change ciphertext to string again
    decrypted = decrypt(key, ciphertext)
    print 'decrypted:', decrypted

if __name__ == '__main__':
    main()