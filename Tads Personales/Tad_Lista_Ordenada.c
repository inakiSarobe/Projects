#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Nodo genérico */
typedef struct nodo {
    void *dato;
    struct nodo *sig;
} Nodo;

/* Lista genérica */
typedef struct {
    Nodo *cabeza;
    int (*comparar)(const void*, const void*);
    void (*imprimir)(const void*);
} Lista;

/* ------------------ FUNCIONES ------------------ */

/* Crear lista */
void crear_lista(Lista *lista, int (*cmp)(const void*, const void*), void (*print)(const void*)) {
    lista->cabeza = NULL;
    lista->comparar = cmp;
    lista->imprimir = print;
}

/* Insertar ordenado */
void insertar_ordenado(Lista *lista, void *dato, size_t tamDato) {
    Nodo *nuevo = (Nodo*)malloc(sizeof(Nodo));
    nuevo->dato = malloc(tamDato);
    memcpy(nuevo->dato, dato, tamDato);
    nuevo->sig = NULL;

    Nodo *actual = lista->cabeza;
    Nodo *anterior = NULL;

    while (actual != NULL && lista->comparar(actual->dato, dato) < 0) {
        anterior = actual;
        actual = actual->sig;
    }

    if (anterior == NULL) {
        nuevo->sig = lista->cabeza;
        lista->cabeza = nuevo;
    } else {
        nuevo->sig = actual;
        anterior->sig = nuevo;
    }
}

/* Eliminar nodo */
void eliminar_nodo(Lista *lista, void *dato) {
    Nodo *actual = lista->cabeza;
    Nodo *anterior = NULL;

    while (actual != NULL && lista->comparar(actual->dato, dato) != 0) {
        anterior = actual;
        actual = actual->sig;
    }

    if (actual != NULL) {
        if (anterior == NULL)
            lista->cabeza = actual->sig;
        else
            anterior->sig = actual->sig;

        free(actual->dato);
        free(actual);
    }
}

/* Buscar valor */
Nodo* buscar_valor(Lista *lista, void *dato) {
    Nodo *aux = lista->cabeza;
    while (aux != NULL && lista->comparar(aux->dato, dato) != 0)
        aux = aux->sig;
    return aux;
}

/* Imprimir lista */
void imprimir_lista(Lista *lista) {
    Nodo *aux = lista->cabeza;
    printf("\n********** LISTA ORDENADA **********\n");
    while (aux != NULL) {
        lista->imprimir(aux->dato);
        aux = aux->sig;
    }
}

/* Liberar lista completa */
void liberar_lista(Lista *lista) {
    Nodo *aux;
    while (lista->cabeza != NULL) {
        aux = lista->cabeza;
        lista->cabeza = lista->cabeza->sig;
        free(aux->dato);
        free(aux);
    }
}

