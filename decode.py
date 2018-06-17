# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 21:46:35 2018

@author: Grzesiek-UC
"""

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

def decryptFlat(channel):
    bits = 0
    chars = 0
    output = ""
    l = []
    for idx, byte in enumerate(channel):
        chars += testBit(channel[idx], 0)<<bits
        bits = (bits + 1) % 8
        if bits == 0:
            output += chr(chars)
            l.append(chars)
            chars = 0
        if output.find("</data>") != -1:
            return output[6:output.index('</data>')], l[6:output.index('</data>')]
    return "error - no data"

def main(argv):
   picfile = ''
   textfile = ''
   try:
      opts, args = getopt.getopt(argv,"hp:t:",["pfile=","tfile="])
   except getopt.GetoptError:
      print('decode.py -p <picture> -t <text>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print( 'decode.py -p <picture> -t <text>')
         sys.exit()
      elif opt in ("-p", "--pfile"):
         picfile = arg
      elif opt in ("-t", "--tfile"):
         textfile = arg
    
   imgIn = Image.open(picfile)
   imgArray = np.array(imgIn)
   imgArray = imgArray.reshape(-1)
   
   output, list_ = decryptFlat(imgArray)
   list_ = bytearray(list_)
   print('hidden message: ', list_.decode('cp1250'))
   
   file = open(textfile, 'wb')
   for byte in list_:
       file.write(byte.to_bytes(1, byteorder='big'))
   file.close()
   
   print('Decription process succesfull')
    

if __name__ == "__main__":
   main(sys.argv[1:])