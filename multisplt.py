#!/usr/bin/python
# coding=UTF-8

# import argparse
import sys
import re
import os
import math


# Formatos que tiene que reconocer
# mm:ss con mm > 59, mm > 99
# hh:mm:ss con mm <= 59, ss <= 59

# Formato de argumentos del script de python
# 01 52nd Street Theme 00:11 02 A Night in Tunisia 05:03 03 All The Things You Are 08:07 04 Embraceable You 15:21
# 00:00:00 01 Serenade Grotesque 00:03:20 02 Menuet Antique 00:09:31 03 Pavane Pour Une infante defunte 00:15:55 04 Jeux D'eau
# Los nombres de canciones no tienen que estar entre comillas y pueden ir antes o después de los títulos
# A las regex les da igual si el título está antes o después del tiempo

# Formato de mp3splt
# mp3splt foo.mp3  0.30 1.00 2.00 EOF -o @n
# 1.mp3 0:30 - 1:00
# 2.mp3 1:00 - 2:00
# 3.mp3 3:00 - EOF


def toMinSec(time):
    splited = re.split(":", time)
    if (len(splited) is 2):
        # No hay que convertir
        return (splited[0]+"."+splited[1])
    elif (len(splited) is 3):
        minutes = int(splited[0])*60 + int(splited[1])
        minutes = str(minutes)
        return(minutes+"."+splited[2])
    else:
        return None

# TODO si el argumento de entrada tiene ' hay que cerrarlas aunque luego el programa no las interpreta. Esto ocurre antes de que se empieze el script

inputfile = sys.argv[1]
#del sys.argv[0] # Nombre del programa
#del sys.argv[0] # Archivo de entrada
argv = ' '.join(sys.argv[2:len(sys.argv)])
# Quita lo de arriba y lo convierte en str separado por ' '


# \d+:\d{2} -> mm:ss
# \d+:\d{2}:\d{2} -> hh:mm:ss

time_regex = r'\d+:\d{2}:\d{2}|\d+:\d{2}'

arg_time = re.findall(time_regex, argv)
num_time = len(arg_time)

arg_name = re.split(time_regex, argv)

try:
    # Sólo elimina un '' de cada vez
    for i in range(0, len(arg_name)):
        arg_name.remove('') # Si no lo encuentra lanza un error
except ValueError:
    pass


num_name = len(arg_name)

# Siempre hay un espacio al final de arg_name[0] y para todos los siguientes hay espacios al principio y al final

temp = arg_name[0][0:len(arg_name[0])-1]
arg_name[0] = temp

for i in range(1, num_name):
    temp = arg_name[i][1:len(arg_name[i])-1]
    arg_name[i] = temp

#print(arg_name)
#print (arg_time)


# TODO comprobar que num_name = num_time + 1
# Puede ser que el tiempo inicial esté implícito y num_name = num_time+2



if (num_name == num_time):
    mp3args = inputfile+" "
    for i in range(0, num_time):
        mp3args += toMinSec(arg_time[i])+" "

    mp3args += "EOF -o @n"

else:

    sys.exit("El número de tiempos y nombres no coindide")



os.system("mp3splt "+mp3args)

pad = math.floor(math.log10(num_name))+1

# Los nombres de archivo seran str(i).zfill(pad)

for i in range(1, num_name+1):
    print (str(i).zfill(pad)+".mp3")
    seqname = str(i).zfill(pad)+".mp3"
    os.system("mv "+seqname+" "+'"'+arg_name[i-1]+".mp3"+'"')
