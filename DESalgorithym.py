# -*- coding: utf-8 -*-
#autor: Marco Antônio de Lima Costa
#algoritimo: Algoritimo de criptografia DES (Data Encryption Standard)
import numpy as np
from random import choice
import os

def makePassword(tamanho, escolha):
    if escolha == 1: 
        caracters = '0123456789ABCDEFGHIJKLMNOPQRSTUWVXZabcdefghijlmnopqrstuwvxz$./'
        senha = ''
        for char in range(tamanho):
                senha += choice(caracters)
        
        print('chave = {}'.format(senha))
        key = open('key.txt', 'w')
        key.write(senha)
        key.close
    
    elif escolha == 2:
        arquivo = open('key.txt', 'r+')
        for line in arquivo:
            senha = line
        print('chave = {}'.format(senha))            
    return makePasswordBlock(senha)

def makePasswordBlock(senha):
    password_bit = np.zeros((8,8)) #cria uma matriz 8x8
    linha = 0
    for letra in senha: #pega letra por letra na senha
        char_byte = bin(ord(letra))[2:].zfill(8)

        for coluna in range(8):
          password_bit[linha][coluna] = char_byte[coluna] #adiciona cada bit da letra em uma casa na matriz 8x8
        linha += 1

    input_key = np.zeros((8,7))
    for i in range(8):
        for j in range(7):
            if j%8 != 0:
                input_key[i][j] = password_bit[i][j]
            else:
                continue
    #print(input_key)
    return makePCO(input_key)

def makePCO(input_key):
    chave_permutada = np.zeros((8,7))
    matriz_definida = [[57, 49, 41, 33, 25, 17, 9], [1, 58, 50, 42, 34, 26, 18], [10, 2, 59, 51, 43, 35, 27], [19, 11, 3, 60, 52, 44, 36], [63, 55, 47, 39, 31, 23, 15], [7, 62, 54, 46, 38, 30, 22], [14, 6, 61, 53, 45, 37, 29], [21, 13, 5, 28, 20, 12, 4]]

    for i in range(8):
        for j in range(7):
            linha = (matriz_definida[i][j]-1)/8 #localizando numero da matriz definida no bloco de bit (linha)
            if linha == 0 or linha < 1:
              linha = 0
            elif linha == 1 or linha < 2:
              linha = 1
            elif linha == 2 or linha < 3:
              linha = 2
            elif linha == 3 or linha < 4:
              linha = 3
            elif linha == 4 or linha < 5:
              linha = 4
            elif linha == 5 or linha < 6:
              linha = 5
            elif linha == 6 or linha < 7:
              linha = 6
            elif linha == 7 or linha < 8:
              linha = 7

            coluna = (matriz_definida[i][j]%8)-1 #localizando numero da matriz definida no bloco de bit (coluna)

            chave_permutada[i][j] = input_key[linha][coluna]
    #print(chave_permutada)
    return crashPermutedKey(chave_permutada)

def crashPermutedKey(chave_permutada):
    c_block = np.zeros((4,7))
    d_block = np.zeros((4,7))

    for i in range(4):
        for j in range(7):
            c_block[i][j] = chave_permutada[i][j]
            d_block[i][j] = chave_permutada[i+4][j]

    return (c_block, d_block)

def getLastLine(datafile): #Pega o valor da ultima linha do arquivo
    datafile = open(datafile, 'r+')
    lines = datafile.readlines()
    last_line = lines [ len ( lines ) -1]
    datafile.close()
    return last_line

def makeBlock(last_line, datafile, entrada, c_block, d_block, escolha): #quebra texto em blocos de 64 bits
    datafile = open(datafile, 'r+')
    
    for line in datafile:

        tamanho = len(line)

        for i in range(tamanho):
          if len(entrada) != 8:
            entrada.append(line[i])
          else:
            #print(entrada)
            makeBitBlock(entrada, c_block, d_block, escolha)
            entrada = []
            entrada.append(line[i])

        if line == last_line:
          if(len(entrada) < 8):
            diferenca = 8 - len(entrada)
            for i in range(diferenca):
              entrada.append(' ')
            makeBitBlock(entrada, c_block, d_block, escolha)
          elif(len(entrada) == 8):
            makeBitBlock(entrada, c_block, d_block, escolha)

    datafile.close()

def makeBitBlock(bloco, c_block, d_block, escolha): #transforma bloco de texto em um bloco de 64 bits
    bloco_bit = np.zeros((8,8)) #cria uma matriz 8x8
    linha = 0
    for letra in bloco: #pega letra por letra no bloco de texto
        for i in range(len(letra)):
            char_byte = bin(ord(letra[i]))[2:].zfill(8) #por causa do python, letra esta como string de tamanho 0, exatamente porque é so uma letra. Dai coverte apenas a letra que esta na posiçao 0 da string letra
        for coluna in range(8):
          bloco_bit[linha][coluna] = char_byte[coluna] #adiciona cada bit da letra em uma casa na matriz 8x8
        linha += 1
    #print(bloco_bit)
    initialPermutation(bloco_bit, c_block, d_block, escolha)

def initialPermutation(bloco_bit, c_block, d_block, escolha):
    matriz_permutada = np.zeros((8,8))
    matriz_definida = [[58, 50, 42, 34, 26, 18, 10, 2], [60, 52, 44, 36, 28, 20, 12, 4], [62, 54, 46, 38, 30, 22, 14, 6], [64, 56, 48, 40, 32, 24, 16, 8], [57, 49, 41, 33, 25, 17, 9, 1], [59, 51, 43, 35, 27, 19, 11, 3], [61, 53, 45, 37, 29, 21, 13, 5], [63, 55, 47, 39, 31, 23, 15, 7]]

    for i in range(8):
        for j in range(8):
            linha = (matriz_definida[i][j]-1)/8 #localizando numero da matriz definida no bloco de bit (linha)
            if linha == 0 or linha < 1:
              linha = 0
            elif linha == 1 or linha < 2:
              linha = 1
            elif linha == 2 or linha < 3:
              linha = 2
            elif linha == 3 or linha < 4:
              linha = 3
            elif linha == 4 or linha < 5:
              linha = 4
            elif linha == 5 or linha < 6:
              linha = 5
            elif linha == 6 or linha < 7:
              linha = 6
            elif linha == 7 or linha < 8:
              linha = 7

            coluna = (matriz_definida[i][j]%8)-1 #localizando numero da matriz definida no bloco de bit (coluna)

            matriz_permutada[i][j] = bloco_bit[linha][coluna]
    #print(matriz_permutada)
    crashBlock(matriz_permutada, c_block, d_block, escolha)

def crashBlock(matriz_permutada, c_block, d_block, escolha):
    left_block = np.zeros((8,4))
    right_block = np.zeros((8,4))

    for i in range(8):
        for j in range(4):
            left_block[i][j] = matriz_permutada[i][j]
            right_block[i][j] = matriz_permutada[i][j+4]
    
    if escolha == 1:
        roundFunction(left_block, right_block, c_block, d_block)
    elif escolha == 2:
        roundDecryptFunction(left_block, right_block, c_block, d_block)
        
def roundFunction(left_block, right_block, c_block, d_block):

    for round in range(1,17):
        right_expandido = expansion(right_block)
        leftShift(c_block, d_block, round)
        matriz_pct = makePCT(c_block, d_block)
        first_xor = makeXor(right_expandido, matriz_pct)
        sBoxes = sBox(first_xor)
        matriz_permutada = makePermutation(sBoxes)
        second_xor = make2Xor(matriz_permutada, left_block)
        left_block = right_block
        right_block = second_xor
    
    gravarCriptografado(left_block, right_block)

def roundDecryptFunction(left_block, right_block, c_block, d_block):
    armazenamento = np.zeros((6,16*8))
    armazenamento2 = np.zeros((6,8))
    for round in range(1,17):
        leftShift(c_block, d_block, round)
        for i in range(6):
            for j in range(8):
                armazenamento[i][j*round] = (makePCT(c_block, d_block))[i][j]
    
    for round in range(16,0,-1):
        right_expandido = expansion(left_block)
        for i in range(6):
            for j in range(8):
                armazenamento2[i][j]= armazenamento[i][j*round]
        first_xor = makeXor(right_expandido, armazenamento2)
        sBoxes = sBox(first_xor)
        matriz_permutada = makePermutation(sBoxes)
        second_xor = make2Xor(matriz_permutada, right_block)
        right_block = left_block 
        left_block = second_xor
    
    gravarDescriptografado(left_block, right_block)

def gravarDescriptografado(left_block, right_block):
    bits_criptografados = np.zeros((8,8))
    cypher = open('plain_text.txt', 'a')
    
    for i in range(8):
        for j in range(4):
            bits_criptografados[i][j] = left_block[i][j]
            bits_criptografados[i][j+4] = right_block[i][j]
    
    inverseInitialPermutation(bits_criptografados)
    
    for i in range(8):
        byte = '{}{}{}{}{}{}{}{}'.format(int(bits_criptografados[i][0]),int(bits_criptografados[i][1]),int(bits_criptografados[i][2]),int(bits_criptografados[i][3]),int(bits_criptografados[i][4]),int(bits_criptografados[i][5]),int(bits_criptografados[i][6]),int(bits_criptografados[i][7]))
        byte = int(byte, 2)
        byte = chr(byte)
        cypher.write(byte)
    
    cypher.close
    cypher = open('plain_text.txt', 'r+')
    print("TEXTO DESCRIPTOGRAFADO: {}".format(cypher.read()))    
    cypher.close
    
def gravarCriptografado(left_block, right_block):
    bits_criptografados = np.zeros((8,8))
    cypher = open('cypher_text.txt', 'a')
    
    for i in range(8):
        for j in range(4):
            bits_criptografados[i][j] = left_block[i][j]
            bits_criptografados[i][j+4] = right_block[i][j]

    inverseInitialPermutation(bits_criptografados)

    for i in range(8):
        byte = '{}{}{}{}{}{}{}{}'.format(int(bits_criptografados[i][0]),int(bits_criptografados[i][1]),int(bits_criptografados[i][2]),int(bits_criptografados[i][3]),int(bits_criptografados[i][4]),int(bits_criptografados[i][5]),int(bits_criptografados[i][6]),int(bits_criptografados[i][7]))
        byte = int(byte, 2)
        byte = chr(byte)
        cypher.write(byte)
    
    cypher.close
    cypher = open('cypher_text.txt', 'r+')
    print("TEXTO CRIPTOGRAFADO: {}".format(cypher.read()))
    cypher.close
    
def inverseInitialPermutation(bits_criptografados):
    matriz_permutada = np.zeros((8,8))
    matriz_definida = [[40, 8, 48, 16, 56, 24, 64, 32], [39, 7, 47, 15, 55, 23, 63, 31], [38, 6, 46, 14, 54, 22, 62, 30], [37, 5, 47, 13, 53, 21, 61, 29], [36, 4, 44, 12, 52, 20, 60, 28], [35, 3, 43, 11, 51, 19, 59, 27], [34, 2, 42, 10, 50, 18, 58, 26], [33, 1, 41, 9, 49, 17, 57, 25]]

    for i in range(8):
        for j in range(8):
            linha = (matriz_definida[i][j]-1)/8 #localizando numero da matriz definida no bloco de bit (linha)
            if linha == 0 or linha < 1:
              linha = 0
            elif linha == 1 or linha < 2:
              linha = 1
            elif linha == 2 or linha < 3:
              linha = 2
            elif linha == 3 or linha < 4:
              linha = 3
            elif linha == 4 or linha < 5:
              linha = 4
            elif linha == 5 or linha < 6:
              linha = 5
            elif linha == 6 or linha < 7:
              linha = 6
            elif linha == 7 or linha < 8:
              linha = 7

            coluna = (matriz_definida[i][j]%8)-1 #localizando numero da matriz definida no bloco de bit (coluna)

            matriz_permutada[i][j] = bits_criptografados[linha][coluna]
            bits_criptografados[i][j] = matriz_permutada[i][j]

def make2Xor(matriz_permutada, left_block):
    second_xor = np.zeros((8,4))
    matriz_permutada = np.resize(matriz_permutada,(8,4))
    
    for i in range(8):
        for j in range(4):
            second_xor[i][j] = int(left_block[i][j])^int(matriz_permutada[i][j])
    
    return second_xor
        
def makePermutation(sBoxes):
    matriz_permutada = np.zeros((4,8))
    matriz_definida = [[16, 7, 20, 21, 29, 12, 28, 17], [1, 15, 23, 26, 5, 18, 31, 10], [2, 8, 24, 14, 32, 27, 3, 9], [19, 13, 30, 6, 22, 11, 4, 25]]
    
    for i in range(4):
        for j in range(8):
            linha = (matriz_definida[i][j]-1)/4 #localizando numero da matriz definida no bloco de bit (linha)
            if linha == 0 or linha < 1:
              linha = 0
            elif linha == 1 or linha < 2:
              linha = 1
            elif linha == 2 or linha < 3:
              linha = 2
            elif linha == 3 or linha < 4:
              linha = 3
            elif linha == 4 or linha < 5:
              linha = 4
            elif linha == 5 or linha < 6:
              linha = 5
            elif linha == 6 or linha < 7:
              linha = 6
            elif linha == 7 or linha < 8:
              linha = 7

            coluna = (matriz_definida[i][j]%4)-1 #localizando numero da matriz definida no bloco de bit (coluna)
            if coluna == -1:
                coluna = 3
            matriz_permutada[i][j] = sBoxes[linha][coluna]
    
    return matriz_permutada                     
        
def sBox(first_xor):
    sBoxes = np.zeros((8,4))
    linha = np.zeros((8,2))
    coluna = np.zeros((8,4))
    
    for i in range(8):
        linha[i][0] = first_xor[i][0]
        linha[i][1] = first_xor[i][5]
        coluna[i][0] = first_xor[i][1]
        coluna[i][1] = first_xor[i][2]
        coluna[i][2] = first_xor[i][3]
        coluna[i][3] = first_xor[i][4]
    
    s1 = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]
    s2 = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]
    s3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]
    s4 = [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]
    s5 = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]
    s6 = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]
    s7 = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]
    s8 = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

    for i in range(8):
        if linha[i][0] == 0 and linha[i][1] == 0:
            linhaa = 0
        elif linha[i][0] == 0 and linha[i][1] == 1:
            linhaa = 1
        elif linha[i][0] == 1 and linha[i][1] == 0:
            linhaa = 2
        elif linha[i][0] == 1 and linha[i][1] == 1:
            linhaa = 3
        
        if coluna[i][0] == 0 and coluna[i][1] == 0 and coluna[i][2] == 0 and coluna[i][3] == 0:
            colunaa = 0
        elif coluna[i][0] == 0 and coluna[i][1] == 0 and coluna[i][2] == 0 and coluna[i][3] == 1:
            colunaa = 1
        elif coluna[i][0] == 0 and coluna[i][1] == 0 and coluna[i][2] == 1 and coluna[i][3] == 0:
            colunaa = 2
        elif coluna[i][0] == 0 and coluna[i][1] == 0 and coluna[i][2] == 1 and coluna[i][3] == 1:
            colunaa = 3
        elif coluna[i][0] == 0 and coluna[i][1] == 1 and coluna[i][2] == 0 and coluna[i][3] == 0:
            colunaa = 4
        elif coluna[i][0] == 0 and coluna[i][1] == 1 and coluna[i][2] == 0 and coluna[i][3] == 1:
            colunaa = 5
        elif coluna[i][0] == 0 and coluna[i][1] == 1 and coluna[i][2] == 1 and coluna[i][3] == 0:
            colunaa = 6
        elif coluna[i][0] == 0 and coluna[i][1] == 1 and coluna[i][2] == 1 and coluna[i][3] == 1:
            colunaa = 7
        elif coluna[i][0] == 1 and coluna[i][1] == 0 and coluna[i][2] == 0 and coluna[i][3] == 0:
            colunaa = 8
        elif coluna[i][0] == 1 and coluna[i][1] == 0 and coluna[i][2] == 0 and coluna[i][3] == 1:
            colunaa = 9
        elif coluna[i][0] == 1 and coluna[i][1] == 0 and coluna[i][2] == 1 and coluna[i][3] == 0:
            colunaa = 10
        elif coluna[i][0] == 1 and coluna[i][1] == 0 and coluna[i][2] == 1 and coluna[i][3] == 1:
            colunaa = 11
        elif coluna[i][0] == 1 and coluna[i][1] == 1 and coluna[i][2] == 0 and coluna[i][3] == 0:
            colunaa = 12
        elif coluna[i][0] == 1 and coluna[i][1] == 1 and coluna[i][2] == 0 and coluna[i][3] == 1:
            colunaa = 13
        elif coluna[i][0] == 1 and coluna[i][1] == 1 and coluna[i][2] == 1 and coluna[i][3] == 0:
            colunaa = 14
        elif coluna[i][0] == 1 and coluna[i][1] == 1 and coluna[i][2] == 1 and coluna[i][3] == 1:
            colunaa = 15
        
        if i == 0:
            column = 0
            for letra in bin(s1[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1  
        elif i == 1:
            column = 0
            for letra in bin(s2[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1
        elif i == 2:
            column = 0
            for letra in bin(s3[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1
        elif i == 3:
            column = 0
            for letra in bin(s4[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1
        elif i == 4:
            column = 0
            for letra in bin(s5[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1
        elif i == 5:
            column = 0
            for letra in bin(s6[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1
        elif i == 6:
            column = 0
            for letra in bin(s7[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1
        elif i == 7:
            column = 0
            for letra in bin(s8[linhaa][colunaa])[2:].zfill(4):
                sBoxes[i][column] = letra
                column = column + 1
                
    return sBoxes
        
def makeXor(right_expandido, matriz_pct):
    first_xor = np.zeros((8,6))
    matriz_pct_nova = np.resize(matriz_pct,(8,6))
                
    for i in range(8):
        for j in range(6):
            first_xor[i][j] = int(right_expandido[i][j])^int(matriz_pct_nova[i][j])
    
    return first_xor        

def makePCT(c_block, d_block):
    matriz_definida = [[14, 17, 11, 24, 1, 5, 3, 28], [15, 6, 21, 10, 23, 19, 12, 4], [26, 8, 16, 7, 27, 20, 13, 2], [41, 52, 31, 37, 47, 55, 30, 40], [51, 45, 33, 48, 44, 49, 39, 56], [34, 53, 46, 42, 50, 36, 29, 32]]
    matriz_pct = np.zeros((8,7))
    
    for i in range(4):
        for j in range(7):
            matriz_pct[i][j] = c_block[i][j]
            matriz_pct[i+4][j] = d_block[i][j]

    #print(matriz_pct)
    matriz_pct2 = np.zeros((6,8))
    
    for i in range(6):
        for j in range(8):
            linha = (matriz_definida[i][j])/8 #localizando numero da matriz definida no bloco de bit (linha)
            if linha == 0 or linha < 1:
              linha = 0
            elif linha == 1 or linha < 2:
              linha = 1
            elif linha == 2 or linha < 3:
              linha = 2
            elif linha == 3 or linha < 4:
              linha = 3
            elif linha == 4 or linha < 5:
              linha = 4
            elif linha == 5 or linha < 6:
              linha = 5
            elif linha == 6 or linha < 7:
              linha = 6
            elif linha == 7 or linha < 8:
              linha = 7

            coluna = (matriz_definida[i][j]%7)-1 #localizando numero da matriz definida no bloco de bit (coluna)
            if coluna == -1:
                coluna = 6
            matriz_pct2[i][j] = matriz_pct[linha][coluna]
    
    return matriz_pct2

def leftShift(c_block, d_block, round):
    #print(round)
    c_anterior = c_block
    d_anterior = d_block
    a = c_anterior[0][0]
    b = c_anterior[0][1]
    c = d_anterior[0][0]
    d = d_anterior[0][1]
    if round == 1 or round == 2 or round == 9 or round == 16:
        for i in range(4):
            for j in range(7):
                if j == 6:
                    if i == 3:
                        c_block[i][j] = a
                        d_block[i][j] = c
                    else:
                        c_block[i][j] = c_block[i+1][0]
                        d_block[i][j] = d_block[i+1][0]
                else:
                    c_block[i][j] = c_block[i][j+1]
                    d_block[i][j] = d_block[i][j+1]
    
    else:
        for i in range(4):
            for j in range(7):
                if j == 5:
                    if i == 3:
                        c_block[i][j] = a
                        d_block[i][j] = c
                    else:
                        c_block[i][j] = c_anterior[i+1][0]
                        d_block[i][j] = d_anterior[i+1][0]
                elif j == 6:
                    if i == 3:
                        c_block[i][j] = b
                        d_block[i][j] = d
                    else:
                        c_block[i][j] = c_anterior[i+1][1]
                        d_block[i][j] = d_anterior[i+1][1]
                else:
                    c_block[i][j] = c_anterior[i][j+2]
                    d_block[i][j] = d_anterior[i][j+2]
    
def expansion(right_block):
    right_expandido = np.zeros((8,6))

    for i in range(8):
        for j in range(6):
            if j == 0:
                linha = i-1
                if linha == -1:
                    linha = 7
                coluna = 3
            elif j == 5:
                linha = i+1
                if linha == 8:
                    linha = 0
                coluna = 0
            else:
                linha = i
                coluna = j-1

            right_expandido[i][j] = right_block[linha][coluna]
    return right_expandido

print('----------Data Encryption Standard--------------')
print('deseja: criptograr[1] ou descriptografar[2]')
escolha = int(input())
if escolha == 1:
    path = os.path.abspath(os.path.dirname(__file__))
    dir = os.listdir(path)
    for file in dir:
        if file == "cypher_text.txt":
            os.remove(file)

    entrada = []
    c_block, d_block = makePassword(8, escolha)
    datafile = "entrada1.txt"
    arq = open(datafile, "r+")
    print('TEXTO: {}'.format(arq.read()))
    makeBlock(getLastLine(datafile), datafile, entrada, c_block, d_block, escolha)
    print("Sucesso!")
elif escolha == 2:
    path = os.path.abspath(os.path.dirname(__file__))
    dir = os.listdir(path)
    for file in dir:
        if file == "plain_text.txt":
            os.remove(file)
    
    entrada = []
    c_block, d_block = makePassword(8, escolha)
    datafile = "cypher_text.txt"
    arq = open(datafile, "r+")
    print('TEXTO CRIPTOGRAFADO: {}'.format(arq.read()))
    makeBlock(getLastLine(datafile), datafile, entrada, c_block, d_block, escolha)
    print("Sucesso!")
else:
    print("Escolha invalida")
#gravar senha em arquivo de texto, para poder deografar posteriormente