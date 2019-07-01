import os
from digital_signature import generate, get_global_params, check_message_file_is_not_empty, authenticate, check_has_files



def questao_a(pointG, order, p, a):
    os.system('cls' if os.name == 'nt' else 'clear')

    message = generate(pointG, order, p, a, 'questao_a')

    input("\nPessione para realizar a AUTENTICAÇÃO!\n\n\n")

    authenticate(pointG, order, p, a, message)    

    input("\nPessione enter para continuar...")





def questao_b(pointG, order, p, a):
    os.system('cls' if os.name == 'nt' else 'clear')
    has_message = check_message_file_is_not_empty() 

    if has_message:
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
    
    pointG, order, p, a = get_global_params()

    input("\n\n\n\nPessione enter para continuar...")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\nCom os parametros settados, há três operações disponíveis: \n")
        
        print("a - Algoritmo ECDSA (Completo).")
        print("b - ECDSA utilizando arquivo de mensagem - Gerar.")
        print("c - Verificar se a assinatura gerada é valida - Autenticar.")
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