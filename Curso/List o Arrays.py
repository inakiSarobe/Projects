usuarios = ["Juan", "Rodrigo", "Raul", "Nazaret", "Iñaki"]
print(f"Usuarios: {usuarios}")

usuarios.sort() #El metodo sort ordena alfabeticamente las list
print(f"Usuarios ordenados alfabeticamente: {usuarios}")

usuarios[3] = "Magaldi" 
print(f"Usuario cambiado a: {usuarios[3]}\nla lista quedo como: {usuarios}")

usuarios.append("Loren") #El metodo append agrega un elemento al final de la lista
print(usuarios)

usuarios.pop() #El metodo pop elimina el ultimo elemento de la lista
print(usuarios)

del usuarios[2] #Eliminamos un elemento especifico

usuarios.pop(1) #El metodo pop tambien puede eliminar por ubicacion especifica

print(usuarios)

usuarios.remove("Rodrigo") #El metodo remove elimina por nombre
print (usuarios)


"""

ITERADORES

"""
i = 0
for usuario in usuarios: #se suele utilizar como buena practica el singular como nombre de la lista. Es mas facil iterar que a comparacion de C ya que no necesitamos expresar cuantas veces, el compilador ya sabe que es hasta terminar la lista
    i += 1
    print(f"El usuario numero {i} es: {usuario}")

for numero in range(1, 10, 2): #Esto imprime del 1 al 9 ya que 10 es limite de rango (a, b) cuando a es (=) y b es (<). (a, b, c) c seria el incremento
    print(numero)