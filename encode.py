# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 21:24:15 2018

@author: Grzesiek-UC
"""
#!/usr/bin/python

import sys, getopt
from PIL import Image
import numpy as np
from math import floor

def setBit(var, offset):
    mask = 1 << offset
    return(var | mask)

def clearBit(var, offset):
    mask = ~(1 << offset)
    return(var & mask)

def testBit(var, offset):
    mask = 1 << offset
    return(var & mask)

def encryptFlat(channel, information):
    bits = 0
    chars = 0
    for idx, byte in enumerate(channel):
        if testBit(information[chars], bits):
            channel[idx] = setBit(channel[idx], 0)
        else:
            channel[idx] = clearBit(channel[idx], 0)
                
        bits = (bits + 1) % 8
        if bits == 0:
            chars += 1
                
        if chars >= len(information):
            break
    return bits, chars  

def main(argv):
   picfile = ''
   textfile = ''
   try:
      opts, args = getopt.getopt(argv,"hp:t:",["pfile=","tfile="])
   except getopt.GetoptError:
      print('encode.py -p <picture> -t <text>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print( 'encode.py -p <picture> -t <text>')
         sys.exit()
      elif opt in ("-p", "--pfile"):
         picfile = arg
      elif opt in ("-t", "--tfile"):
         textfile = arg

   textfile = open(textfile)
   text = textfile.read()
   text = "<data>" + text + "</data>"
   text = bytearray(text.encode('cp1250'))
   #text = str(text, 'utf-8')
   #text = text.encode()
   textfile.close()
    
   imgIn = Image.open(picfile)
   imgArray = np.array(imgIn)
   shape = imgArray.shape
   imgArray = imgArray.reshape(-1)
   capacity = floor(imgArray.size / 8)
   if capacity < len(text):
       print("picture is too small to hide such amount of text!")
       sys.exit()
       
   _, chars = encryptFlat(imgArray, text)
   imgArray = imgArray.reshape(shape)
   imgOut = Image.fromarray(imgArray)
   imgOut.save('encrypted.png')
   print(chars, 'bytes encripted into picture')
   print('Encription process succesfuly ended')
    

if __name__ == "__main__":
   main(sys.argv[1:])