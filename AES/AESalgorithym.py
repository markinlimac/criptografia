#!/usr/bin/python

import os
import sys
import math

class AES(object):    
    keySize = dict(SIZE_128=16)

    # Rijndael S-box
    sbox =  [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16]

    def getSBoxValue(self,num):
        return self.sbox[num]

    def rotate(self, word):
        return word[1:] + word[:1]

    # Rijndael Rcon
    Rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
            0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97,
            0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72,
            0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
            0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
            0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
            0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
            0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61,
            0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
            0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
            0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,
            0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
            0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
            0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
            0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c,
            0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
            0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4,
            0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
            0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
            0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
            0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
            0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2,
            0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74,
            0xe8, 0xcb ]

    def getRconValue(self, num):
        return self.Rcon[num]

    def core(self, word, iteration):

        word = self.rotate(word) #rotaciona a palavra(t) de 32 bits em 8 bits a esquerda
        
        for i in range(4):
            word[i] = self.getSBoxValue(word[i]) # aplica a substituicao de S-Box em todas as 4 partes da palavra de 32 bits
        word[0] = word[0] ^ self.getRconValue(iteration) #aplica XOR na saida da operacao rcon com a primeira letra da esquerda
        return word

    def expandKey(self, key, size, expandedKeySize): #expansao de Rijndael

        currentSize = 0
        rconIteration = 1
        expandedKey = [0] * expandedKeySize #expandedKey vai ser um vetor de 0 do tamanho da chaveexpandida definida na parte da encriptacao

        for j in range(size):
            expandedKey[j] = key[j] #coloca o valor da chave dentro da chave expandida
        currentSize += size

        while currentSize < expandedKeySize:
            t = expandedKey[currentSize-4:currentSize] #coloca os ultimos 4 bytes na variavel temporaria t

            if currentSize % size == 0:
                t = self.core(t, rconIteration) #a cada 16 bytes eh aplicado a programacao principal para t
                rconIteration += 1 #incrementa a rconIteration

            for m in range(4):
                expandedKey[currentSize] = expandedKey[currentSize - size] ^ t[m] #aplica XOR no bloco de 4 bytes com o bloco de 16 bytes e isso vira os proximos 4 bytes na chave expandida
                currentSize += 1

        return expandedKey

    def addRoundKey(self, state, roundKey):

        for i in range(16):
            state[i] ^= roundKey[i] #aplica XOR no bloco com a chave de round
        return state #novo bloco depois do XOR

    def createRoundKey(self, expandedKey, roundKeyPointer): #cria uma chave a cada round a partir da chave expandida

        roundKey = [0] * 16 #array de 16 posicoes preenchidos com 0
        for i in range(4):
            for j in range(4):
                roundKey[j*4+i] = expandedKey[roundKeyPointer + i*4 + j]
        return roundKey

    def galois_multiplication(self, a, b): #multiplicacao galois de 8 bits entre a e b 

        p = 0
        for counter in range(8):
            if b & 1: p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            # keep a 8 bit
            a &= 0xFF
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p

    def subBytes(self, state, isInv): #substitui todos os valores do bloco pelo valor no SBox, usando o valor do bloco como indice para o SBox
        if isInv: getter = self.getSBoxInvert #pega o valor na SBox invertida
        else: getter = self.getSBoxValue #pega o valor na SBox 
        for i in range(16): state[i] = getter(state[i])
        return state

    def shiftRows(self, state, isInv):
        
        for i in range(4):
            state = self.shiftRow(state, i*4, i, isInv) #chama shiftRow para cada linha iterada
        return state

    def shiftRow(self, state, statePointer, nbr, isInv):
        
        for i in range(nbr): #cada iteracao desloca 1 bit a esquerda
            if isInv:
                state[statePointer:statePointer+4] = state[statePointer+3:statePointer+4] + state[statePointer:statePointer+3]
            else:
                state[statePointer:statePointer+4] = state[statePointer+1:statePointer+4] + state[statePointer:statePointer+1]
        return state

    def mixColumns(self, state, isInv): #multiplicacao galois da matriz 4x4
    
        for i in range(4):
            column = state[i:i+16:4] #constroi uma coluna cortando as 4 linhas 
            column = self.mixColumn(column, isInv) #aplica mixColumn na coluna
            state[i:i+16:4] = column # put the values back into the state

        return state

    def mixColumn(self, column, isInv): #multiplicacao galois em uma coluna da matriz 4x4
        if isInv: mult = [14, 9, 13, 11]
        else: mult = [2, 1, 1, 3]
        cpy = list(column)
        g = self.galois_multiplication

        column[0] = g(cpy[0], mult[0]) ^ g(cpy[3], mult[1]) ^ g(cpy[2], mult[2]) ^ g(cpy[1], mult[3])
        column[1] = g(cpy[1], mult[0]) ^ g(cpy[0], mult[1]) ^ g(cpy[3], mult[2]) ^ g(cpy[2], mult[3])
        column[2] = g(cpy[2], mult[0]) ^ g(cpy[1], mult[1]) ^ g(cpy[0], mult[2]) ^ g(cpy[3], mult[3])
        column[3] = g(cpy[3], mult[0]) ^ g(cpy[2], mult[1]) ^ g(cpy[1], mult[2]) ^ g(cpy[0], mult[3])
        return column

    def aes_round(self, state, roundKey): #aplica 4 operacoes em cada rodada
        state = self.subBytes(state, False) #substituicao de bytes
        state = self.shiftRows(state, False) #shiftRows
        state = self.mixColumns(state, False) #mistura as colunas
        state = self.addRoundKey(state, roundKey) #adiciona a chave de round
        return state

    # applies the 4 operations of the inverse round in sequence
    def aes_invRound(self, state, roundKey):
        state = self.shiftRows(state, True)
        state = self.subBytes(state, True)
        state = self.addRoundKey(state, roundKey)
        state = self.mixColumns(state, True)
        return state

    def aes_main(self, state, expandedKey, nbrRounds):
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 0))
        i = 1
        while i < nbrRounds:
            state = self.aes_round(state, self.createRoundKey(expandedKey, 16*i))
            i += 1
        state = self.subBytes(state, False)
        state = self.shiftRows(state, False)
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 16*nbrRounds))
        return state

    # Perform the initial operations, the standard round, and the final
    # operations of the inverse aes, creating a round key for each round
    def aes_invMain(self, state, expandedKey, nbrRounds):
        state = self.addRoundKey(state,
                                 self.createRoundKey(expandedKey, 16*nbrRounds))
        i = nbrRounds - 1
        while i > 0:
            state = self.aes_invRound(state,
                                      self.createRoundKey(expandedKey, 16*i))
            i -= 1
        state = self.shiftRows(state, True)
        state = self.subBytes(state, True)
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 0))
        return state

    def encrypt(self, iput, key, size):
        
        output = [0] * 16
        nbrRounds = 0 #numero de rounds
        block = [0] * 16 #o bloco de 128 bits que serao encriptados

        if size == self.keySize["SIZE_128"]: nbrRounds = 10 #se o tamanho da chave for 128 bits, serao 10 rounds
        else: return None

        expandedKeySize = 16*(nbrRounds+1) #tamanho da chave expandida

        for i in range(4): #iteracao das colunas do bloco
            for j in range(4): #iteracao das linhas do bloco
                block[(i+(j*4))] = iput[(i*4)+j]

        expandedKey = self.expandKey(key, size, expandedKeySize) #expande a chave em 176 bytes

        block = self.aes_main(block, expandedKey, nbrRounds) #encripta o bloco usando a chave expandida

        for k in range(4):
            for l in range(4):
                output[(k*4)+l] = block[(k+(l*4))] #desmapeia o bloco novamente na saida
        return output

    def decrypt(self, iput, key, size):
        
        output = [0] * 16
        nbrRounds = 0 #numero de rounds
        block = [0] * 16 #o bloco de 128 bits que serao encriptados

        if size == self.keySize["SIZE_128"]: nbrRounds = 10 #se o tamanho da chave for 128 bits, serao 10 rounds
        else: return None

        expandedKeySize = 16*(nbrRounds+1) #tamanho da chave expandida

        for i in range(4): #iteracao das colunas do bloco
            for j in range(4): #iteracao das linhas do bloco
                block[(i+(j*4))] = iput[(i*4)+j]

        expandedKey = self.expandKey(key, size, expandedKeySize) #expande a chave em 176 bytes

        block = self.aes_invMain(block, expandedKey, nbrRounds) #decripta o bloco usando a chave expandida

        for k in range(4):
            for l in range(4):
                output[(k*4)+l] = block[(k+(l*4))] #desmapeia o bloco novamente na saida
        return output


class AESModeOfOperation(object):
    aes = AES()

    modeOfOperation = dict(CFB=1)

    # converte a 16 character string into a number array de acordo com a tabela ascii
    def convertString(self, string, start, end, mode):
        if end - start > 16:
            end = start + 16
        ar = []
        
        i = start
        j = 0
        while len(ar) < end - start: #enquanto o tamanho da string ar for menor que o tamanho do bloco
            ar.append(0) #o programa acrescenta 0
        while i < end:
            ar[j] = ord(string[i]) #o programa substitui o 0 pelo inteiro que representa o char
            j += 1
            i += 1
        return ar #retorna o bloco em forma de string de numeros inteiros representando cada char

    def encrypt(self, stringIn, mode, key, size, IV):

        plaintext = []
        iput = [0] * 16 #matriz de zeros com 16 colunas np.zeros((0,16))
        output = []
        ciphertext = [0] * 16
        cipherOut = []

        firstRound = True
        if stringIn != None:
            for j in range(int(math.ceil(float(len(stringIn))/16))): #divide o tamanho do plaintext por 16 e pega o menor numero positivo depois do resultado da divisao  
                start = j*16 # o inicio do bloco de 16 bytes
                end = j*16+16 # o fim do bloco de 16 bytes
                if  end > len(stringIn): #se o fim do bloco for maior que o proprio tamanho da string
                    end = len(stringIn) #o fim do bloco vai ser o final da string
                plaintext = self.convertString(stringIn, start, end, mode) #plaintext eh o bloco em forma de inteiros

                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size) #primeiro round encripta usando o iv
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size) #se nao for o primeiro round encripta usando o bloco
                    for i in range(16):
                        if len(plaintext)-1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output)-1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext)-1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]
                    for k in range(end-start):
                        cipherOut.append(ciphertext[k])
                    iput = ciphertext
        return mode, len(stringIn), cipherOut

    def decrypt(self, cipherIn, originalsize, mode, key, size, IV):

        ciphertext = []
        iput = []
        output = []
        plaintext = [0] * 16 #matriz de zeros com 16 colunas np.zeros((0,16))
        chrOut = []

        firstRound = True
        if cipherIn != None:
            for j in range(int(math.ceil(float(len(cipherIn))/16))): #divide o tamanho do plaintext por 16 e pega o menor numero positivo depois do resultado da divisao
                start = j*16 #o inicio do bloco de 16 bytes
                end = j*16+16 #o fim do bloco de 16 bytes
                if j*16+16 > len(cipherIn): #se o fim do bloco for maior que o proprio tamanho da string
                    end = len(cipherIn) #o fim do bloco vai ser o final da string
                ciphertext = cipherIn[start:end] #ciphertext vai ser uma string de inteiros representando o bloco de 16 bytes
                
                if mode == self.modeOfOperation["CFB"]:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size) #primeiro round encripta usando o iv
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size) #se nao for o primeiro round encripta usando o bloco
                    for i in range(16):
                        if len(output)-1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext)-1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output)-1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]
                    for k in range(end-start):
                        chrOut.append(chr(plaintext[k]))
                    iput = ciphertext
        return "".join(chrOut)

def encryptData(key, text, mode=AESModeOfOperation.modeOfOperation["CFB"]):
    
    key = map(ord, key) #transforma a chave em um array de inteiros
    keysize = len(key) #pega tamanho da chave
    iv = [ord(i) for i in os.urandom(16)] #cria um iv aleatorio
    moo = AESModeOfOperation()
    (mode, length, ciph) = moo.encrypt(text, mode, key, keysize, iv) #retorna o texto cifrado o modo e o tamanho do texto cifrado
    return ''.join(map(chr, iv)) + ''.join(map(chr, ciph)) #transforma o texto cifrado que esta em forma de inteiro em char e concatena para uma mesma string

def decryptData(key, data, mode=AESModeOfOperation.modeOfOperation["CFB"]):
    
    key = map(ord, key) #transforma a chave em um array de inteiros
    keysize = len(key) #pega tamanho da chave
    iv = map(ord, data[:16]) # iv eh os primeiros 16 bytes em forma de numeros inteiros
    data = map(ord, data[16:]) # text eh o restante de bytes em forma de numeros inteiros
    moo = AESModeOfOperation()
    decr = moo.decrypt(data, None, mode, key, keysize, iv) #retorna o texto descriptografado
    return decr

def generateRandomKey(keysize = 16):
    senha = os.urandom(keysize) 
    key = open('key.txt', 'w')
    key.write(senha) #Escreve a senha no arquivo "key.txt"
    key.close
    return senha
    
if __name__ == "__main__":
    moo = AESModeOfOperation()
    print('----------Advanced Encryption Standard--------------')
    escolha = int(input('deseja criptograr[1] ou descriptografar[2]: '))
    
    if escolha == 1:
        path = os.path.abspath(os.path.dirname(__file__)) #Acha o caminho do diretorio em que o programa esta
        dir = os.listdir(path) #Acha o diretorio em que o programa esta
        for file in dir:
            if file == "cypher_text.txt": #Caso ja exista o arquivo "cypher_text.txt" o programa exclui para nao dar nenhum problema 
                os.remove(file)
        
        entrada = []
        datafile = "entrada1.txt"
        arq = open(datafile, "r+")
        text = arq.read()
        print('TEXTO: {}'.format(text))
        key =  generateRandomKey(16)
        print ''
        print 'chave =', key
        print ''
        mode = AESModeOfOperation.modeOfOperation["CFB"]
        cipher = encryptData(key, text, mode) #chama o modo de encriptacao CFB
        arq = open("cypher_text.txt", "w") 
        arq.write(str(cipher)) #escreve o texto cifrado no arquivo cypher_text.txt 
        arq.close
        print("TEXTO CIFRADO: {}".format(cipher))
    
    elif escolha == 2:
        existe = os.path.exists('cypher_text.txt')
        if existe == True: #Caso ja exista o arquivo "cypher_text.txt" o programa ira ler para descriptografar            
            arq = open("cypher_text.txt", "r+")
            text = arq.read()
            print("TEXTO CIFRADO: {}".format(text))
            mode = AESModeOfOperation.modeOfOperation["CFB"]
            arquivo = open('key.txt', 'r+')
            key = arquivo.read()
            print ''
            print('chave = {}'.format(key))
            print ''
            decr = decryptData(key, text, mode) #chama o modo de decriptacao CFB
            arq = open("plain_text.txt", "w")
            arq.write(decr) #Escreve o texto descifrado no arquivo "plain_text.txt" 
            arq.close
            print("TEXTO DESCRIPTOGRAFADO: {}".format(decr))
        elif existe == False: #Caso nao exista o arquivo "cypher_text.txt" o programa ira identificar que nao ha dados para serem descriptografados
            print('Nao existe nenhum dado criptografado')
    
    else:
        print("Escolha invalida")