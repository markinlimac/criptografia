import sys
sys.path.insert(0, '..')
import elipticAlgorithym


def questao_a():
    print('Entrou em A')

    print("\nAgora, vamos gerar as chaves publicas e privadas: \n")
    publicA, publicB, secretA, secretB, ordem, Gx, Gy = elipticAlgorithym.menu()

    print("\n\nChaves: \n")
    print("PrKA:", secretA)
    print("PrKB:", secretB)
    print("PuKA:", publicA)
    print("PuKB:", publicB)
    print("N:", ordem)
    print("Gx:", Gx)
    print("Gy:", Gy)





def questao_b():
    print('Entrou em B')

    temp = input("\nPrimeiramente, insira a mensagem para a qual deseja gerar a assinatura digital no arquivo 'message.py'.\n\n"
                    "\t\tPara continuar pressione enter.\n\n")
    




def questao_c():
    print('Entrou em C')




def menu():
    while True:
        print("\n\nPara o ECDSA, há três operações disponíveis: \n")
        
        print("a - Algoritmo ECDSA.")
        print("b - Algoritmo ECDSA, com arquivo de mensagem e gerando arquivo com assinatura.")
        print("c - Verificar se a assinatura gerada é valida.")
        print("\nCaso deseje sair, insira outro caracter.")

        entrada = input("\n\t\tDigite a opção escolhida:\t")
        
        if entrada == 'a':
            questao_a()
        elif entrada == 'b':
            print('Entrou em B')
        elif entrada == 'c':
            print('Entrou em C')
        else:
            print('\n\n\t\tAdeus!\n\n')
            break;

        print('\n\n\n')
        
    exit()
    


if __name__ == "__main__":
    menu()