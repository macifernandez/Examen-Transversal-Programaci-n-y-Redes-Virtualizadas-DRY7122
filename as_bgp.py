numero_as = int(input("Ingrese el numero de AS de BGP: "))
if 64512 <= numero_as <= 65534:
    print("AS privado")
else: 
    print("AS publico")