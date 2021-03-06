# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 17:10:29 2018

@author: Grzesiek-DevDoBlog {devdo.eu}
"""

import sys, getopt
from PIL import Image
import numpy as np
from math import floor

openEmbbed = "<data>"
closeEmbbed = "</data>"

def setBit(var, offset):
    mask = 1 << offset
    return(var | mask)

def clearBit(var, offset):
    mask = ~(1 << offset)
    return(var & mask)

def testBit(var, offset):
    mask = 1 << offset
    return(var & mask)

def decryptFlat(channels):
    bits = 0
    chars = 0
    output = ""
    byteList = []
    for idx, byte in enumerate(channels):
        chars += testBit(channels[idx], 0)<<bits
        bits = (bits + 1) % 8
        if bits == 0:
            output += chr(chars)
            byteList.append(chars)
            chars = 0
            if output.find(closeEmbbed) != -1:
                return output[len(openEmbbed):output.index(closeEmbbed)], byteList[len(openEmbbed):output.index(closeEmbbed)]
    return "error - no data"

def encryptFlat(channels, information):
    bits = 0
    chars = 0
    for idx, byte in enumerate(channels):
        if testBit(information[chars], bits):
            channels[idx] = setBit(channels[idx], 0)
        else:
            channels[idx] = clearBit(channels[idx], 0)
                
        bits = (bits + 1) % 8
        if bits == 0:
            chars += 1
                
        if chars >= len(information):
            break
    return bits, chars  

def main(argv):
    picfile = ''
    textfile = ''
    mode = ''
    try:
        opts, args = getopt.getopt(argv,"hp:t:m:",["pic=","tfile=", "mode="])
    except getopt.GetoptError:
        print('stego.py -p <picture> -t <text> -m <encode|decode>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( 'stego.py -p <picture> -t <text> -m <encode|decode>')
            sys.exit()
        elif opt in ("-p", "--pic"):
            picfile = arg
        elif opt in ("-t", "--tfile"):
            textfile = arg
        elif opt in ("-m", "--mode"):
            mode = arg
            
    imgIn = Image.open(picfile)
    imgArray = np.array(imgIn)
    shape = imgArray.shape
    imgArray = imgArray.reshape(-1)
    
    if mode == "decode":       
        output, list_ = decryptFlat(imgArray)
        list_ = bytearray(list_)
        print('hidden message: ', list_.decode('cp1250'))
       
        file = open(textfile, 'wb')
        for byte in list_:
            file.write(byte.to_bytes(1, byteorder='big'))
        file.close()
       
        print('Decription process succesfull')
       
    elif mode == "encode":
        textfile = open(textfile)
        text = textfile.read()
        textfile.close()
        text = openEmbbed + text + closeEmbbed
        text = bytearray(text.encode('cp1250'))
        
        capacity = floor(imgArray.size / 8) - len(openEmbbed + closeEmbbed)
        print("You can hide", capacity, "bytes inside this picture")
        if capacity < len(text):
            print("picture is too small to hide such amount of text!")
            sys.exit()
           
        _, chars = encryptFlat(imgArray, text)
        imgArray = imgArray.reshape(shape)
        imgOut = Image.fromarray(imgArray)
        imgOut.save('encrypted.png')
        print(chars, 'bytes encripted into picture')
        print('Encription process succesfuly ended')
    else :
        print("Unknown mode!")
    

if __name__ == "__main__":
   main(sys.argv[1:])
