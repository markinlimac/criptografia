# -*- coding: utf-8 -*-
#autor: Marco Antônio de Lima Costa
#algoritimo: Algoritimo de criptografia DES (Data Encryption Standard)
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
          entrada.append('')
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
    print(bloco_bit) #chamar permutação inicial

#def initialPermutation():

entrada = []
makeBlock(getLastLine(), entrada)
