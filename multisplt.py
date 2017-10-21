#!/usr/bin/python
# coding=UTF-8

import sys
import re
import os
import math


# Time formats
# mm:ss with mm > 59, mm > 99
# hh:mm:ss with mm <= 59, ss <= 59

# Arguments format
# 01 52nd Street Theme 00:11 02 A Night in Tunisia 05:03 03 All The Things You Are 08:07 04 Embraceable You 15:21
# 00:00:00 01 Serenade Grotesque 00:03:20 02 Menuet Antique 00:09:31 03 Pavane Pour Une infante defunte 00:15:55 04 Jeux D'eau

# The song names don't have to be between quotes and can be before or after the timestamps (the regex don't care)

# mp3splt format
# mp3splt foo.mp3  0.30 1.00 2.00 EOF -o @n
# 1.mp3 0:30 - 1:00
# 2.mp3 1:00 - 2:00
# 3.mp3 3:00 - EOF


def toMinSec(time):
    splited = re.split(":", time)
    if (len(splited) is 2):
        # No need to convert
        return (splited[0]+"."+splited[1])
    elif (len(splited) is 3):
        minutes = int(splited[0])*60 + int(splited[1])
        minutes = str(minutes)
        return(minutes+"."+splited[2])
    else:
        return None

# TODO if the argument has ' quotes must be closed even when the script doesn't use them. This happens before the script runs

inputfile = sys.argv[1]
argv = ' '.join(sys.argv[2:len(sys.argv)])
# Removes name of the program argv[0] and input file argv[1] and converts it to srt separated by ' '


# \d+:\d{2} -> mm:ss
# \d+:\d{2}:\d{2} -> hh:mm:ss

time_regex = r'\d+:\d{2}:\d{2}|\d+:\d{2}'

arg_time = re.findall(time_regex, argv)
num_time = len(arg_time)

arg_name = re.split(time_regex, argv)


# arg_name has some empty strings entries we need to remove
try:
    # Only eliminates one '' each time
    for i in range(0, len(arg_name)):
        arg_name.remove('') # If it doesn't find it throws an error
except ValueError:
    pass


num_name = len(arg_name)

# There's always a space at the end of arg_name[0] y the rest have spaces both at the end and the beggining

temp = arg_name[0][0:len(arg_name[0])-1]
arg_name[0] = temp

for i in range(1, num_name):
    temp = arg_name[i][1:len(arg_name[i])-1]
    arg_name[i] = temp



# TODO check that nun_name = num_time + 1
# Initial timestamp may be implicit and num_name = num_time + 2



if (num_name == num_time):
    mp3args = inputfile+" "
    for i in range(0, num_time):
        mp3args += toMinSec(arg_time[i])+" "

    mp3args += "EOF -o @n"

else:

    sys.exit("The number of names and timestamps doesn't match")



os.system("mp3splt "+mp3args)

pad = math.floor(math.log10(num_name))+1

# The mp3splt name files will be str(i).zfill(pad)

for i in range(1, num_name+1):
    print (str(i).zfill(pad)+".mp3")
    seqname = str(i).zfill(pad)
    filename = '"' +seqname+" - "+arg_name[i-1]+".mp3"+ '"'
    os.system("mv "+seqname+".mp3"+" "+filename)
