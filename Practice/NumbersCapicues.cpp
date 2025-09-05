// Possibilities for palindromic numbers within X digits

#include <stdio.h>
#include <stdlib.h>


int reverseN(int x) {
	int reverse = 0;
	while(x > 0) {
		int digits = x % 10;
		reverse = reverse * 10 + digits;
		x = x / 10;
	}
	return reverse;
}

int fewerDigits(int x, int y) {
	int CerosRight = 0;
	int digits = 0;
	int temp = x;
	if(temp > 0 && temp < 10) {
        digits = 1;
    } else {
        while(temp >= 10) {
            temp /= 10;
            digits++;
        }
    }
    
	if (x != 0) {
	    while(x % 10 == 0) {
	        CerosRight++;
	        x /= 10;
	        temp = x;
	    }
	}
	
    int nBare = temp;
    
    if (digits == CerosRight && nBare == reverseN(nBare)) {
    	return 1;
	} else {
		return 0;
	}
}

int numberOfDigits(int x) {
    int n = 1;
    for (int i = 0; i < x; i++){
        n *= 10;
    }
    n = n - 1;
    return n;
}

int nTesting(int x) {
	int tempX = x;
	int digits = 0;
	if(tempX >= 0 && tempX < 10) {
        digits ++;
    } else {
        while(tempX > 0) {
            tempX /= 10;
            digits++;       
        }
    }
    return digits;
}

int comparison(int x, int y) {
	int nCapicua = 0;
	int nReversed = reverseN(x);
	int digits = nTesting(x);
	if(digits >= 1 && digits < y) {
		bool test = fewerDigits(x, y);
		if(test == 1){
			x = nReversed;
		} else {
			x = 0;
		}
	}
	if(x == nReversed) {
		printf("\nPalindromic number = ");
		if(digits < y) {
			if (x == 0){
				printf("0");
				printf("%i", nReversed);
				printf("0");
			} else {
				int missingDigits = y - digits;
				for (int i = 0; i < missingDigits; i++) printf("0");
				printf("%i", nReversed);
				for (int i = 0; i < missingDigits; i++) printf("0");
			}
		} else {
			printf("%i", nReversed);
		}
		
		nCapicua = nCapicua + 1;
	}
	return nCapicua;
}

int loopN(int x, int y) {
	int nCapicua = 0;
	int cantX = x;

	for (int i = 0; i <= cantX; i++) {
		nCapicua += comparison(x, y);
		x = x -1 ;
	}

	return nCapicua;
}

int main() {
	bool loop = 1;
	while(loop){
	    int digits = 0;
	    printf("Enter the number of digits to check for palindromic numbers (e.g., 3 means from 0 to 999): ");
	    scanf("%i", &digits);
	    int result = numberOfDigits(digits);	
	    int nCapicua = loopN(result, digits);
	    printf("\n\nTotal palindromic numbers = %i", nCapicua);
	    float possibilityOfPalindromic = (float)nCapicua / ((float)result + 1);
	    printf("\nChance of getting a palindromic number with %i digits is %.2f%%\n", digits, possibilityOfPalindromic * 100);
		printf("\nIndicates if it ends (1.- NO; 0.- YES) \n");
		scanf("%d", &loop);	
		system("cls");
	}
}


