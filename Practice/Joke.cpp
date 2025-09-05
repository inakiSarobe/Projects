// ITS A JOKE
#include <stdio.h>
#include <stdlib.h>



void Size(int x){
	if (x > 1){
		for (int i=1; i <= x; i++){
			printf(" ");	
		}
	}
}

int main(){
	int cont = 1;
	
	while (cont == 1){
		//size = " " * x      in python
		int y = 1;	
		printf("define Size of TITS\n");
		scanf("%d", &y);
		if (y == 1) {
			printf("\n(.Y.)");
		} else {
			printf("\n(");
			Size(y);
			printf(".");
			Size(y);
			printf(") ");
			printf("(");
			Size(y);
			printf(".");
			Size(y);
			printf(")");
		}
		printf("\n\n-----------------------\n");
		printf("\nNew tits? \nYES = 1\nNO = 0\n");
		scanf("%d", &cont);
		system("cls");
	}	
	
}


