#include <iostream>
#include <string>

using namespace std;

int main() {
	string resp;
	
	do {
		
	    double precioRepuesto;
	    double precioFinal;
	    double envio = 0;
	    double precioAmigo = 0;
	
	    string respuestaEnvio, respuestaAmigo;
	
	    // Pedir precio del repuesto
	    cout << "Ingrese el precio del repuesto: ";
	    cin >> precioRepuesto;
	
	    // Preguntar si quiere envío
	    cout << "¿Desea envío? (S/N): ";
	    cin >> respuestaEnvio;
	    if (respuestaEnvio == "S" || respuestaEnvio == "s") {
	        envio = 2000;
	    }
	
	    // Preguntar tipo de precio (amigo, no, personalizado)
	    cout << "¿Es precio amigo? (S/N/O): ";
	    cin >> respuestaAmigo;
	
	    if (respuestaAmigo == "S" || respuestaAmigo == "s") {
	        precioAmigo = 15000;
	    } else if (respuestaAmigo == "N" || respuestaAmigo == "n") {
	        precioAmigo = 20000;
	    } else if (respuestaAmigo == "O" || respuestaAmigo == "o") {
	        cout << "Ingrese el precio de la mano de obra: ";
	        cin >> precioAmigo;
	    } else {
	        cout << "Opción no válida. Se tomará precio como 0.\n";
	    }
	
	    // Calcular precio final
	    precioFinal = precioRepuesto + envio + precioAmigo;
	
	    // Mostrar resultado
	    cout << "El precio a pagar es: $" << precioFinal << endl;
	    
	    cout << "\nDebe averiguar otro precio? (S/N): ";
	    cin >> resp;

	} while (resp == "S" || resp == "s");
    return 0;
}

