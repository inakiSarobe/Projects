#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Nodo genérico
typedef struct tipo_nodo_cola {
    void *dato;
    struct tipo_nodo_cola *sig;
} nodo_cola;

// Cola genérica
typedef struct tipo_cola {
    nodo_cola *primero, *ultimo;
    size_t tam_dato; // tamaño del tipo que almacena
} t_cola;

// Crear cola
void crear_cola(t_cola *cola, size_t tam_dato) {
    cola->primero = NULL;
    cola->ultimo = NULL;
    cola->tam_dato = tam_dato;
}

// Encolar genérico
void encolar(t_cola *cola, void *dato) {
    nodo_cola *nuevo = (nodo_cola *)malloc(sizeof(nodo_cola));
    nuevo->dato = malloc(cola->tam_dato);
    memcpy(nuevo->dato, dato, cola->tam_dato);
    nuevo->sig = NULL;

    if (cola->ultimo == NULL) {
        cola->primero = nuevo;
        cola->ultimo = nuevo;
    } else {
        cola->ultimo->sig = nuevo;
        cola->ultimo = nuevo;
    }
}

// Desencolar genérico
int desencolar(t_cola *cola, void *dato) {
    if (cola->primero == NULL)
        return 0; // cola vacía

    nodo_cola *aux = cola->primero;
    memcpy(dato, aux->dato, cola->tam_dato);
    cola->primero = aux->sig;
    if (cola->primero == NULL)
        cola->ultimo = NULL;

    free(aux->dato);
    free(aux);
    return 1;
}

// Verifica si está vacía
int cola_vacia(t_cola cola) {
    return cola.primero == NULL;
}

// Liberar memoria
void destruir_cola(t_cola *cola) {
    nodo_cola *act = cola->primero, *sig;
    while (act != NULL) {
        sig = act->sig;
        free(act->dato);
        free(act);
        act = sig;
    }
    cola->primero = cola->ultimo = NULL;
}
