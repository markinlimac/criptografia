# -*- coding: utf-8 -*-
#assume-se que o maximo divisor comum de entrada e modulo é 1, ou seja são primos entre si

def inversoMultiplicativo(entrada, modulo) :
    modulo0 = modulo
    y = 0
    x = 1

    if (modulo == 1) : #resto da divisão de qualquer coisa por 1 é sempre 0
        return 0

    while (entrada > 1) :
        if (modulo == 0):
          return("Esse numero nao possui inverso multiplicativo")
        quociente = entrada // modulo

        moduloAntigo = modulo

        modulo = entrada % moduloAntigo #resto vira modulo nas proximas iterações
        entrada = moduloAntigo #dividendo vira o que antes era modulo
        moduloAntigo = y

        # Update x and y
        y = x - quociente * y
        x = moduloAntigo


    # Make x positive
    if (x < 0) :
        x = x + modulo0

    return x

datafile = open("entradas2.txt", 'r+')
for line in datafile:
    entrada = line
    entrada, separador, modulo = entrada.split(' ')

    print("O inverso multiplicativo de {} mod {} eh: {}".format(int(entrada), int(modulo), inversoMultiplicativo(int(entrada), int(modulo))))
