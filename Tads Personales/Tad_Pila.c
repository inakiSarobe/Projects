#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Nodo genérico
typedef struct tipo_nodo_pila {
    void *dato;
    struct tipo_nodo_pila *sig;
} nodo_pila;

// Pila genérica
typedef struct {
    nodo_pila *tope;
    size_t tam_dato;
} t_pila;

// Crear pila
void crear_pila(t_pila *pila, size_t tam_dato) {
    pila->tope = NULL;
    pila->tam_dato = tam_dato;
}

// Apilar un elemento
void apilar(t_pila *pila, void *dato) {
    nodo_pila *nuevo = (nodo_pila *)malloc(sizeof(nodo_pila));
    nuevo->dato = malloc(pila->tam_dato);
    memcpy(nuevo->dato, dato, pila->tam_dato);

    nuevo->sig = pila->tope;
    pila->tope = nuevo;
}

// Desapilar un elemento
int desapilar(t_pila *pila, void *dato) {
    if (pila->tope == NULL)
        return 0; // Pila vacía

    nodo_pila *aux = pila->tope;
    memcpy(dato, aux->dato, pila->tam_dato);
    pila->tope = aux->sig;
    free(aux->dato);
    free(aux);
    return 1;
}

// Verificar si la pila está vacía
int pila_vacia(t_pila pila) {
    return pila.tope == NULL;
}

/* Mostrar pila (recibe puntero a función para imprimir el dato)
void mostrar_pila(t_pila pila, void (*mostrar)(const void *)) {
    nodo_pila *actual = pila.tope;
    printf("\n********** PILA **********\n");
    while (actual != NULL) {
        mostrar(actual->dato);
        actual = actual->sig;
    }
    printf("**************************\n");
} */ 

// Liberar memoria
void destruir_pila(t_pila *pila) {
    nodo_pila *act = pila->tope;
    while (act) {
        nodo_pila *sig = act->sig;
        free(act->dato);
        free(act);
        act = sig;
    }
    pila->tope = NULL;
}
