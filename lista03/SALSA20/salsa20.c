#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <limits.h>

int asciiInt (unsigned char caracter)
{
    static char binario[CHAR_BIT + 1] = {0};
    int r = 0;
    char *p;

    for (int i = CHAR_BIT - 1; i >= 0; i--) {
        binario[i] = (caracter % 2) + '0';
        caracter /= 2;
    }
    
    p = binario;

    while (p && *p ) {
        r <<= 1;
        r += (unsigned int)((*p++) & 0x01);
    }
    return (int) r;
}

static uint32_t rotl(uint32_t value, int shift) {
    return (value << shift) | (value >> (32 - shift));
}
 
void quarter_round(uint32_t a, uint32_t b, uint32_t c, uint32_t d) {
    b ^= rotl(a + d, 7);
    c ^= rotl(b + a, 9);
    d ^= rotl(c + b, 13);
    a ^= rotl(d + c, 18);
}

void salsa20_block(uint32_t out[16], uint32_t const in[16]) {
  	int i;
  	uint32_t x[16];

  	for (i = 0; i < 16; ++i) {
  		x[i] = in[i];
    }

    for (i = 0; i < 20; i += 2) {
		quarter_round(x[ 0], x[ 4], x[ 8], x[12]);
		quarter_round(x[ 5], x[ 9], x[13], x[ 1]);
		quarter_round(x[10], x[14], x[ 2], x[ 6]);
		quarter_round(x[15], x[ 3], x[ 7], x[11]);
	
		quarter_round(x[ 0], x[ 1], x[ 2], x[ 3]);
		quarter_round(x[ 5], x[ 6], x[ 7], x[ 4]);
		quarter_round(x[10], x[11], x[ 8], x[ 9]);
		quarter_round(x[15], x[12], x[13], x[14]);
	  }

    for (i = 0; i < 16; ++i) {
        out[i] = x[i] + in[i];
    }
}

unsigned int_to_bin(unsigned num) {
    if (num == 0) return 0;
    if (num == 1) return 1;
    return (num % 2) + 10 * int_to_bin(num / 2);
}

void generate_data(uint32_t array[16]) {
    char bin[8];

    for(int i=0; i<16; i++) {
        int temp = int_to_bin(array[i]);
        printf("%d", temp);
    }
    printf("\n");
}

int main(){
    uint32_t input[16], output[16];
    unsigned char input_ascii[32];
    char input_bin[128]= "";

    for(int i=0; i<16; i++){
        input[i] = 0;
    }

    printf("Insira um input de 16 caracteres: ");
    scanf("%s", input_ascii);    

    for(int i=0; i<strlen(input_ascii); i++){
        input[i] = asciiInt(input_ascii[i]);
    }

    salsa20_block(output, input);
    generate_data(output);

    return 0;
}
