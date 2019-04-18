# -*- coding: utf-8 -*-
import numpy as np

def getLastLine(): #Pega o valor da ultima linha do arquivo
  datafile = open("entrada1.txt", 'r+')
  lines = datafile.readlines()
  last_line = lines [ len ( lines ) -1]
  datafile.close()
  return last_line

def makeBlock(last_line, entrada): #quebra texto em blocos de 64 bits
  datafile = open("entrada1.txt", 'r+')

  for line in datafile:

    tamanho = len(line)

    for i in range(tamanho):
      if len(entrada) != 8:
        entrada.append(line[i])
      else:
        print(entrada)
        makeBitBlock(entrada)
        entrada = []
        entrada.append(line[i])

    if line == last_line:
      if(len(entrada) < 8):
        diferenca = 8 - len(entrada)
        for i in range(diferenca):
          entrada.append(' ')
        print(entrada)
        makeBitBlock(entrada)
      elif(len(entrada) == 8):
        print(entrada)
        makeBitBlock(entrada)

  datafile.close()

def makeBitBlock(bloco): #transforma bloco de texto em um bloco de 64 bits
    bloco_bit = np.zeros((8,8)) #cria uma matriz 8x8
    linha = 0
    for letra in bloco: #pega letra por letra no bloco de texto
        for i in range(len(letra)):
            char_byte = bin(ord(letra[i]))[2:].zfill(8) #por causa do python, letra esta como string de tamanho 0, exatamente porque é so uma letra. Dai coverte apenas a letra que esta na posiçao 0 da string letra

        for coluna in range(8):
          bloco_bit[linha][coluna] = char_byte[coluna] #adiciona cada bit da letra em uma casa na matriz 8x8
        linha += 1
    #print(bloco_bit)
    initialPermutation(bloco_bit)

def initialPermutation(bloco_bit):
    matriz_permutada = np.zeros((8,8))
    matriz_definida = [[58, 50, 42, 34, 26, 18, 10, 2],
                       [60, 52, 44, 36, 28, 20, 12, 4],
                       [62, 54, 46, 38, 30, 22, 14, 6],
                       [64, 56, 48, 40, 32, 24, 16, 8],
                       [57, 49, 41, 33, 25, 17, 9, 1],
                       [59, 51, 43, 35, 27, 19, 11, 3],
                       [61, 53, 45, 37, 29, 21, 13, 5],
                       [63, 55, 47, 39, 31, 23, 15, 7]]

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
    print(matriz_permutada)

entrada = []
makeBlock(getLastLine(), entrada)
