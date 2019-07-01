import os
from digital_signature import generate, get_global_params, check_message_file_is_not_empty, authenticate, check_has_files



def questao_a(pointG, order, p, a):
    os.system('cls' if os.name == 'nt' else 'clear')

    message = generate(pointG, order, p, a, 'questao_a')


    # # Printa resultado
    # with open('signature_pair.txt') as file:
    #     r = file.readline().split(" ", 1)[1].rsplit(" ", 1)[0]
    #     s = file.readline().split(" ", 1)[1].rsplit(" ", 1)[0]

    # print("\n\n\tR: ", r)
    # print("\tS: ", s)
    # print("\tMensagem: ", message)

    input("\nPessione enter para continuar...")





def questao_b(pointG, order, p, a):
    os.system('cls' if os.name == 'nt' else 'clear')
    check_message_file_is_not_empty()

    generate(pointG, order, p, a, 'questao_b')

    input("\nPessione enter para continuar...")





def questao_c(pointG, order, p, a):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    has_files = check_has_files()

    if has_files:
        authenticate(pointG, order, p, a)

    input("\nPessione enter para continuar...")



def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n\nPara utilizar o ECDSA, primeiro devemos definir alguns parametros globais utilizando curvas elipticas.\n")
    
    # pointG, order, p, a = get_global_params()

    print("\n\nOs valores foram setados:")

    pointG = (3, 4)
    order = 12
    p = 7
    a = 10

    print("\torder:", order)
    print("\tGx:", pointG[0])
    print("\tGy:", pointG[1])    
    print("\tp:", p)
    print("\ta:", a)

    input("\nPessione enter para continuar...")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\nCom os parametros settados, há três operações disponíveis: \n")
        
        print("a - Algoritmo ECDSA.")
        print("b - Algoritmo ECDSA, com arquivo de mensagem e gerando arquivo com assinatura.")
        print("c - Verificar se a assinatura gerada é valida.")
        print("\nCaso deseje sair, insira outro caracter.")

        entrada = input("\n\t\tDigite a opção escolhida:\t")
        
        if entrada == 'a':
            questao_a(pointG, order, p, a)
        elif entrada == 'b':
            questao_b(pointG, order, p, a)
        elif entrada == 'c':
            questao_c(pointG, order, p, a)
        else:
            print('\n\n\t\tAdeus!\n\n')
            break

        print('\n\n\n')
        
    exit()
    


if __name__ == "__main__":
    menu()