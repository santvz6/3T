# uso de if en variables
numero = 0
numero = 'cero' if numero == 0 else 'no es cero'
print(numero)

numero = 1
numero = 'cero' if numero == 0 else 'no es cero'
print(numero)

# uso de for en listas
lista = ['elemento' for _ in range(3)]
print(lista)

# uso de dos for para matrices
array = [['array' for _ in range(3)] for i in range(3)]
print(array)
