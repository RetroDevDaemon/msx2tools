#!/usr/bin/env python3
#######################
# MSX BASIC Detokenizer
#
# takes a binary BASIC file (header: FFh)
#  and creates a BASIC listing with proper line endings.
# [incomplete but workable.]
#
# $ python3 ./pydetokenmsx.py <INPUTFILE>
#
#   Output: "INPUTFILE"-listing.bas
# ** Requires msxbasic-tokenlist.txt **

import sys 

f=open('msxbasic-tokenlist.txt','r')
i = 0
tokens = []
while i < 16:
    inl=f.readline()
    inl = inl.split(',')
    inl[15] = inl[15][:-1]
    for p in inl:
        tokens.append(p)
    i += 1

outstring = ''

tokens[44] = ','
subtokens = [] 
i = 0
while i < 4:
    inl=f.readline()
    inl = inl.split(',')
    inl[len(inl)-1] = inl[len(inl)-1][:-1]
    for p in inl:
        subtokens.append(p)
    i += 1
f.close()
f=open(sys.argv[1],'rb')
inbytes=f.read()
f.close()
bc = 0
if inbytes[bc] != 255:
    print("This is not a MSX tokenized BASIC file!")
    sys.exit()

def print_token():
    global bc 
    global outstring
    b = inbytes[bc]
    if b == 0:
        bc += 3
        outstring += str((inbytes[bc+1] * 256) + inbytes[bc]) + " "
        bc += 1
        return 
    elif b == 11:
        print('[octal]')
        bc += 2
    elif b == 12:
        bc += 1
        outstring += '&H' + hex((inbytes[bc+1]*256)+inbytes[bc])[2:]
        bc += 1
    elif b == 14:
        bc += 1
        outstring += str((inbytes[bc+1]*256)+inbytes[bc])
        bc += 1
    elif b == 15:
        outstring += str(inbytes[bc+1])
        bc += 1
    elif b == 28:
        bc += 1 
        outstring += str((inbytes[bc+1]*256)+inbytes[bc])
        bc += 1
    elif b == 255:
        bc += 1
        b = inbytes[bc]
        outstring += subtokens[b-128]
    else:
        outstring += tokens[b]

bc += 1
startaddr = hex((inbytes[bc+1] * 256) + inbytes[bc])
outstring += "1 REM Start address: " + startaddr + '\r\n'

bc += 2
outstring += str((inbytes[bc+1] * 256) + inbytes[bc]) + " "

def process_file():
    global outstring
    global bc 
    global inbytes 
    while bc < len(inbytes):
        bc += 2
        while inbytes[bc] != 0:
            print_token()
            bc += 1
        if inbytes[bc] == 0:
            if inbytes[bc+1] == 0:
                if inbytes[bc+2] == 0:
                    return 
        bc += 1
        bc += 2
        outstring += "\r\n"+str((inbytes[bc+1] * 256) + inbytes[bc]) + " "

process_file()

f = open(sys.argv[1]+'-listing.bas', 'w')
f.write(outstring)
f.close()

print (sys.argv[1]+'-listing.bas written successfully!')
