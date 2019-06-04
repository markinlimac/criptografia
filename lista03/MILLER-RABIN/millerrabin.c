#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int encontrarKQ(int *k , int *q ,int numero){
  int i ,j;
  int valorTeste,condicao;
  
  valorTeste = (numero - 1);
  
  for (i = 0 ; i < numero ; i++){
    for ( j = 1 ; j< numero ; j+=2){
        condicao = pow(2,i)*j;
        if (valorTeste == condicao){
          *k = i;
          *q = j;
          return 1;
      }
    }
  }
  return 0;
}

int congruenciaLinear(int numero, int semente){
  int valor;
  int randon_number;
  
  valor = 16807 * semente + 17;
  randon_number = valor % numero;
  
  if (randon_number == numero){
    randon_number = randon_number - 1;
  
  }else if(randon_number == 0){
    randon_number = 17;
  }
  return randon_number;
}

long long int exep(int a, int b , int c){
int i;
long long int saida;
saida =a;
  for( i = 1 ; i<b; i++){
    saida*=a;
    saida = saida % c;
  }
  return saida;
}

int teste(int semente, int numero){
  int *k,*q, valorK=0 , valorQ=0, i,t,x;
  long long int aux;
  
  k = &valorK;
  q = &valorQ;
  t = encontrarKQ(k,q,numero);
  aux = exep(semente,*q, numero);
  x = aux % numero;
  
  if (x == 1 || x == (numero-1)){
    return 1;
  }
  for (i = 0 ; i <=*k-1; i++){
    aux = exep(x,2,numero);
    x =  aux % numero;
    if (x == 1){
      return -1;
    }
    if (x == (numero-1)){
      return 1;
    }
  }
  return -1;
}

int main(){
  int auxiliar, i, semente;
  int quantidade, numero;
  double probabilidade, primo = 1;
  
  printf("Digite o numero que quer testar: ");
  scanf("%d",&numero);
  printf("Digite a quantidade de vezes que ira executar o teste: ");
  scanf("%d",&quantidade);

  i = 0;
  
  while (i != quantidade){
    if ( i == 0){
      semente = congruenciaLinear(numero,7);
    }else{
      semente = congruenciaLinear(numero,semente);
    }
    auxiliar = teste(semente,numero);
    if (auxiliar == 1){
      primo = primo * 0.25;
    }else{
      primo = -1;
      break;
    }
    i++;
  }
  if (primo == -1){
    printf("Numero Composto!\n");
  }else{
    probabilidade = 100 - primo;
    printf("Numero com probabilidade de ser primo = %lf%% \n",probabilidade);
  }
  return 0;
}