#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tad_Lista_Ordenada.c"
#include "TAD_Cola.c"
#include "TAD_Pila.c"

#define MAX_STR 200

typedef struct {
    char nombre[50];
    char apellido[50];
    int edad;
    long dni;
    char descripcion[200];
} Persona;

/* Prototipos específicos */
int comparar_por_dni(const void *a, const void *b);
int comparar_por_nombre(const void *a, const void *b);
void imprimir_persona(const void *p);
void leer_cadena(const char *prompt, char *buffer, size_t tam);
long leer_dni(const char *prompt);
int leer_entero(const char *prompt);
void mostrar_cola_personas(t_cola cola);
void mostrar_pila_personas(t_pila pila);

int main(void) {
    Lista porDNI, porNombre;
    crear_lista(&porDNI, comparar_por_dni, imprimir_persona);
    crear_lista(&porNombre, comparar_por_nombre, imprimir_persona);
    t_cola colaPersonas;
    crear_cola(&colaPersonas, sizeof(Persona));
    t_pila pilaPersonas;
    crear_pila(&pilaPersonas, sizeof(Persona));
    
    int opcion = 0;
    Persona p, temp;
    while (1) {
        printf("\n--- MENU ---\n");
        printf("1) Ingresar persona\n");
        printf("2) Mostrar lista ordenada por DNI\n");
        printf("3) Mostrar lista ordenada por Apellido,Nombre\n");
        printf("4) Buscar persona por DNI\n");
        printf("5) Eliminar persona por DNI\n");
        printf("6) Buscar persona por Nombre\n");
        printf("7) Eliminar persona por Nombre\n");
    	printf("8) Desencolar persona\n");
    	printf("9) Mostrar cola\n");
    	printf("10) Desapilar persona\n");
    	printf("11) Mostrar pila\n");
        printf("12) Salir\n");
        opcion = leer_entero("Seleccione una opcion: ");

		if (opcion == 1) {
		    Persona p;
		    leer_cadena("Nombre: ", p.nombre, sizeof(p.nombre));
		    leer_cadena("Apellido: ", p.apellido, sizeof(p.apellido));
		    p.edad = leer_entero("Edad: ");
		    p.dni = leer_dni("DNI (solo numeros): ");
		    leer_cadena("Descripcion: ", p.descripcion, sizeof(p.descripcion));
		
		    // --- Buscar si ya existe ---
		    Persona temp = {0};
		    temp.dni = p.dni;
		    Nodo *res = buscar_valor(&porDNI, &temp);
		
		    if (res) {
		        Persona *existente = (Persona *)res->dato;
		        printf("La persona ya existe. Actualizando edad de %d a %d.\n", existente->edad, p.edad);
		        existente->edad = p.edad;  // ?? Actualiza solo la edad
		    } else {
		        // ?? Si no existe, insertar normalmente
		        insertar_ordenado(&porDNI, &p, sizeof(Persona));
		        insertar_ordenado(&porNombre, &p, sizeof(Persona));
		        encolar(&colaPersonas, &p);
		        apilar(&pilaPersonas, &p);
		        printf("Persona agregada.\n");
		    }
		}

        else if (opcion == 2) {
            printf("\n--- Lista por DNI ---\n");
            imprimir_lista(&porDNI);
        }
        else if (opcion == 3) {
            printf("\n--- Lista por Apellido, Nombre ---\n");
            imprimir_lista(&porNombre);
        }
        else if (opcion == 4) {
            long dni = leer_dni("DNI a buscar: ");
            Persona temp = {0};
            temp.dni = dni;
            Nodo *res = buscar_valor(&porDNI, &temp);
            if (res) {
                printf("Encontrado:\n");
                imprimir_persona(res->dato);
            } else {
                printf("No se encontro persona con DNI %ld\n", dni);
            }
        }
        else if (opcion == 5) {
            long dni = leer_dni("DNI a eliminar: ");
            Persona temp = {0};
            temp.dni = dni;
            eliminar_nodo(&porDNI, &temp);
            eliminar_nodo(&porNombre, &temp);
            printf("Si existia, la persona fue eliminada de ambas listas.\n");
        }
        else if (opcion == 6) {
            Persona temp = {0};
            leer_cadena("Nombre a buscar: ", temp.nombre, sizeof(temp.nombre));
            Nodo *res = buscar_valor(&porNombre, &temp);
            if (res) {
                printf("Encontrado:\n");
                imprimir_persona(res->dato);
            } else {
                printf("No se encontro persona con Nombre %s\n", temp.nombre);
            }
        }
		else if (opcion == 7) {
		    Persona temp = {0};
		    leer_cadena("Nombre a buscar: ", temp.nombre, sizeof(temp.nombre));
		
		    Nodo *res = buscar_valor(&porNombre, &temp);
		    if (res) {
		        Persona *p_encontrada = (Persona*)res->dato;
		        eliminar_nodo(&porNombre, p_encontrada);
		        eliminar_nodo(&porDNI, p_encontrada);
		        printf("Persona eliminada de ambas listas.\n");
		    } else {
		        printf("No se encontró persona con ese nombre.\n");
		    }
		}
        else if (opcion == 8) {
			desencolar(&colaPersonas, &temp);
        }
        else if (opcion == 9) {
            mostrar_cola_personas(colaPersonas);
        }
        else if (opcion == 10) {
			desapilar(&pilaPersonas, &temp);
        }
        else if (opcion == 11) {
            mostrar_pila_personas(pilaPersonas);
        }
        else if (opcion == 12) {
            liberar_lista(&porDNI);
            liberar_lista(&porNombre);
            destruir_cola(&colaPersonas);
            destruir_pila(&pilaPersonas);
            printf("Saliendo...\n");
            break;
        }
        else {
            printf("Opcion invalida.\n");
        }
    }

    return 0;
}

/* Comparador por DNI (menor -> orden ascendente) */
int comparar_por_dni(const void *a, const void *b) {
    const Persona *pa = (const Persona*)a;
    const Persona *pb = (const Persona*)b;
    if (pa->dni < pb->dni) return -1;
    if (pa->dni > pb->dni) return 1;
    return 0;
}

/* Comparador por Apellido, luego Nombre (lexicográfico) */
int comparar_por_nombre(const void *a, const void *b) {
    const Persona *pa = (const Persona*)a;
    const Persona *pb = (const Persona*)b;
    int cmp = strcmp(pa->nombre, pb->nombre);
    if (cmp != 0) return cmp;
    return strcmp(pa->nombre, pb->nombre);
}

/* Imprimir persona */
void imprimir_persona(const void *p) {
    const Persona *pp = (const Persona*)p;
    printf("Apellido: %s, Nombre: %s | Edad: %d | DNI: %ld | Desc: %s\n",
           pp->apellido, pp->nombre, pp->edad, pp->dni, pp->descripcion);
}

/* Lectura segura de cadenas (quita el '\n') */
void leer_cadena(const char *prompt, char *buffer, size_t tam) {
    printf("%s", prompt);
    if (fgets(buffer, (int)tam, stdin) != NULL) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') buffer[len-1] = '\0';
    } else {
        buffer[0] = '\0';
    }
}

/* Leer DNI como número largo */
long leer_dni(const char *prompt) {
    char buf[64];
    leer_cadena(prompt, buf, sizeof(buf));
    return atol(buf);
}

/* Leer entero simple */
int leer_entero(const char *prompt) {
    char buf[64];
    leer_cadena(prompt, buf, sizeof(buf));
    return atoi(buf);
}


// COLA

void mostrar_cola_personas(t_cola cola) {
    nodo_cola *act = cola.primero;
    if (act == NULL) {
        printf("La cola esta vacia.\n");
        return;
    }
    printf("\n--- COLA DE PERSONAS ---\n");
    while (act != NULL) {
        Persona *p = (Persona *)act->dato;
    	printf("Apellido: %s, Nombre: %s | Edad: %d | DNI: %ld | Desc: %s\n", p->apellido, p->nombre, p->edad, p->dni, p->descripcion);
    	act = act->sig;
	}
}

// PILA

void mostrar_pila_personas(t_pila pila) {
    nodo_pila *act = pila.tope;
    if (act == NULL) {
        printf("La pila esta vacia.\n");
        return;
    }
    printf("\n--- PILA DE PERSONAS ---\n");
    while (act != NULL) {
        Persona *p = (Persona *)act->dato;
    	printf("Apellido: %s, Nombre: %s | Edad: %d | DNI: %ld | Desc: %s\n", p->apellido, p->nombre, p->edad, p->dni, p->descripcion);
    	act = act->sig;
	}
}



