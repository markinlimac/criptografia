#-*- coding: utf8 -*-
from random import choice
import os

#Vetor da permutação inicial definida
PI = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

#Vetor da permutação inical feita na chave (permuted choice one)
CP_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

#Vetor da permutação aplicada depois de fazer shift para obter a proxima subchave (permuted choice one)
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

#Vetor da matriz expandida
E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

#SBOX
S_BOX = [
         
[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
],

[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
],

[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
],

[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
],  

[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
], 

[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
], 

[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
],
   
[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]
]

#Permutação feita depois de cada SBox
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

#Permutação final depois de ter feito todos os rounds (inverso da permutação inicial)
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

#Vetor que define quantos shifts vao ser feitos em cada round
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

def makePassword(tamanho, escolha): #Gera uma chave aleatória de 8bytes
    if escolha == 1: #Se for para criptografar a chave tem que ser criada
        caracters = '0123456789ABCDEFGHIJKLMNOPQRSTUWVXZabcdefghijlmnopqrstuwvxz$./'
        senha = ''
        for char in range(tamanho): #No range de 8bytes
                senha += choice(caracters) #Escolhe um caracter aleatoriamente e adiciona ao final da senha
        
        print('chave = {}'.format(senha))
        key = open('key.txt', 'w')
        key.write(senha) #Escreve a senha no arquivo "key.txt"
        key.close
    
    elif escolha == 2: #Caso seja para descriptografar a chave ja existe e esta armazenada no arquivo "key.txt" 
        arquivo = open('key.txt', 'r+')
        for line in arquivo:
            senha = line
        print('chave = {}'.format(senha))
    
    return senha

def getLastLine(datafile): #Pega o valor da ultima linha do arquivo
    datafile = open(datafile, 'r+')
    lines = datafile.readlines()
    last_line = lines [ len ( lines ) -1]
    datafile.close()
    return last_line

def correctText(last_line, datafile, entrada): #Caso a entrada nao seja multiplo de 8 (8bytes), o programa adiciona espaços no final
    datafile = open(datafile, 'r+')
    
    for line in datafile:
    
        tamanho = len(line)
    
        for i in range(tamanho):
          if len(entrada) != 8:
              entrada.append(line[i])
          else:
              entrada = '{}{}{}{}{}{}{}{}'.format(entrada[0],entrada[1],entrada[2],entrada[3],entrada[4],entrada[5],entrada[6],entrada[7]) 
              entrada_atualizada = open('entrada_atualizada.txt', 'a')
              entrada_atualizada.write(entrada)
              entrada_atualizada.close
              entrada = []
              entrada.append(line[i])

        if line == last_line:
          if(len(entrada) < 8):
            diferenca = 8 - len(entrada)
            for i in range(diferenca):
              entrada.append(' ')
            entrada = '{}{}{}{}{}{}{}{}'.format(entrada[0],entrada[1],entrada[2],entrada[3],entrada[4],entrada[5],entrada[6],entrada[7])
            entrada_atualizada = open('entrada_atualizada.txt', 'a')
            entrada_atualizada.write(entrada)
            entrada_atualizada.close
          elif(len(entrada) == 8):
            entrada = '{}{}{}{}{}{}{}{}'.format(entrada[0],entrada[1],entrada[2],entrada[3],entrada[4],entrada[5],entrada[6],entrada[7])
            entrada_atualizada = open('entrada_atualizada.txt', 'a')
            entrada_atualizada.write(entrada)
            entrada_atualizada.close

    datafile.close()

def string_to_bit_vetcor(text):#Converte uma string em uma lista de bits
    vetor = list()
    for char in text:
        valor_binario = binval(char, 8)#Retorna o valor em bytes(8 bits) de cada char
        vetor.extend([int(x) for x in list(valor_binario)]) #Adiciona cada bit ao final da lista
    return vetor

def bit_vector_to_string(vetor):#Retorna uma string a partir da lista de bits
    string = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in bytes]) for bytes in  nsplit(vetor,8)]])   
    return string

def binval(val, bitsize):#Retorna o numero binário de uma string do tamanho determinado 
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "binary value larger than the expected size"
    while len(binval) < bitsize:
        binval = "0"+binval #Adiciona a quantidade de 0 necessarias para obter o tamanho desejado
    return binval

def nsplit(s, n):#Quebra uma lista em varias sublistas de tamanho "n"
    return [s[k:k+n] for k in range(0, len(s), n)]

ENCRYPT=1
DECRYPT=0

class des():
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()
        
    def run(self, key, text, action=ENCRYPT):
        self.password = key
        self.text = text
        
        self.generatekeys() #Gera todas as chaves
        text_blocks = nsplit(self.text, 8) #Qeubra o texto em blocos de 8 bytes so 64 bits
        result = list()
        for block in text_blocks:#Cada bloco de texto passa por 16 rounds
            block = string_to_bit_vetcor(block)#Converte o bloco em um vetor de bits
            block = self.permut(block,PI)#Aplica a permutação inicial
            g, d = nsplit(block, 32) #Quebra o bloco em 2 blocos g(LEFT), d(RIGHT)
            tmp = None
            for i in range(16): #Executa os 16 rounds
                d_e = self.expand(d, E) #Expande o d(RIGHT) para ficar do tamanho da subchave(48bits)
                if action == ENCRYPT:
                    tmp = self.xor(self.keys[i], d_e)#Se for encriptação usa a primeira subchave
                else:
                    tmp = self.xor(self.keys[15-i], d_e)#Se for deecriptação começa pela ultima subchave
                tmp = self.substitute(tmp)#Aplicação das SBOXes
                tmp = self.permut(tmp, P)#Faz a permutação 
                tmp = self.xor(g, tmp)#Faz o xor entre g(LEFT) e tmp
                g = d
                d = tmp
            result += self.permut(d+g, PI_1) #Faz a ultima permutação e acrescenta o resultado na lista
        final_res = bit_vector_to_string(result)
        
        return final_res #Retorna a string final do dado cifrado ou decifrado
    
    def substitute(self, d_e):#Substitui os bytes usando a SBOX
        subblocks = nsplit(d_e, 6)#Divide o vetor de bit em sublistas de 6 bits
        result = list()
        for i in range(len(subblocks)): #No range de todas sublistas
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]),2)#Obtem a linha com o primeiro e ultimo bit
            column = int(''.join([str(x) for x in block[1:][:-1]]),2) #Coluna é os bits 2,3,4,5
            val = S_BOX[i][row][column] #Pega o valor de cada SBOX no round
            bin = binval(val, 4)#Converte o valor para binario
            result += [int(x) for x in bin]#Acrescenta o valor na lista de resultado
        return result
        
    def permut(self, block, table):#Permuta o bloco usando a tabela dada
        return [block[x-1] for x in table]
    
    def expand(self, block, table):#Permuta o bloco usando a tabela dada
        return [block[x-1] for x in table]
    
    def xor(self, t1, t2):#Aplica o xor e retorna a lista de resultado
        return [x^y for x,y in zip(t1,t2)]
    
    def generatekeys(self):#Geração de chaves
        self.keys = []
        key = string_to_bit_vetcor(self.password)
        key = self.permut(key, CP_1) #Aplica a permutação inicial na chave
        g, d = nsplit(key, 28) #Quebra a chave em 2 blocos (g->LEFT),(d->RIGHT)
        for i in range(16):#Aplica os 16 rounds
            g, d = self.shift(g, d, SHIFT[i]) #Aplica os shifts de acordo com o round em questão
            tmp = g + d #Merge them
            self.keys.append(self.permut(tmp, CP_2)) #Aplica a permutação para obter a subchave

    def shift(self, g, d, n): #Aplica os shifts nos valores da lista
        return g[n:] + g[:n], d[n:] + d[:n]
    
    
    def encrypt(self, key, text):
        return self.run(key, text, ENCRYPT)
    
    def decrypt(self, key, text):
        return self.run(key, text, DECRYPT)
    
if __name__ == '__main__':
    d = des()
    print('----------Data Encryption Standard--------------')
    escolha = int(input('deseja criptograr[1] ou descriptografar[2]: '))
    
    if escolha == 1:
        key = makePassword(8, escolha) #Gera uma chave aleatória de 8bytes
        path = os.path.abspath(os.path.dirname(__file__)) #Acha o caminho do diretorio em que o programa esta
        dir = os.listdir(path) #Acha o diretorio em que o programa esta
        for file in dir:
            if file == "cypher_text.txt": #Caso ja exista o arquivo "cypher_text.txt" o programa exclui para não dar nenhum problema 
                os.remove(file)
            if file == "entrada_atualizada.txt": #Caso ja exista o arquivo "entrada_atualizada.txt" o programa exclui para não dar nenhum problema
                os.remove(file)

        entrada = []
        datafile = "entrada1.txt"
        arq = open(datafile, "r+")
        correctText(getLastLine(datafile), datafile, entrada) #Caso a entrada nao seja multiplo de 8 (8bytes), o programa adiciona espaços no final
        datafile = "entrada_atualizada.txt"
        arq = open(datafile, "r+")
        text = arq.read()
        print('TEXTO: {}'.format(text))
        r = d.encrypt(key,text)
        arq = open("cypher_text.txt", "w")
        arq.write(r) #Escreve o texto cifrado no arquivo "cypher_text.txt" 
        arq.close
        print("TEXTO CIFRADO: {}".format(r))
    
    elif escolha == 2:
        key = makePassword(8, escolha)
        existe = os.path.exists('cypher_text.txt')
        if existe == True: #Caso ja exista o arquivo "cypher_text.txt" o programa ira ler para descriptografar            
            arq = open("cypher_text.txt", "r+")
            r = arq.read()
            print("TEXTO CIFRADO: {}".format(r))
            r2 = d.decrypt(key,r)
            arq = open("plain_text.txt", "w")
            arq.write(r2) #Escreve o texto descifrado no arquivo "plain_text.txt" 
            arq.close
            print("TEXTO DESCRIPTOGRAFADO: {}".format(r2))
        elif existe == False: #Caso nãp exista o arquivo "cypher_text.txt" o programa ira identificar que não há dados para serem descriptografados
            print('Não existe nenhum dado criptografado')
    
    else:
        print("Escolha invalida")
