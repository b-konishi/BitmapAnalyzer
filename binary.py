####################
# bitmap Analysis ##
####################

import binascii as bin
import sys

FILE_NAME = './character/1.bmp'
FILE_NAME = sys.argv[1] if len(sys.argv) == 2 else FILE_NAME
print(FILE_NAME)

# Start data-bit address
bfOffBitsStart = 10 #byte
bfOffBits = 4

# Image(width, height)
bfWidthStart = 18
bfHeightStart = 22
bfWidth = 4
bfHeight = 4

file = open(FILE_NAME, 'r')
data = file.read()
file.closed
# Loaded BMP-file data in hexadecimal
data = bin.hexlify(data)

def func(data, start, length):
    address = start * 2
    value = data[address : address+(length*2)]
    list = []
    # Get value (Note to reverse data)
    for i in range(0, len(value)/2):
        list.append(value[i*2 : i*2+2])
    list.reverse()
    # Convert to decimal
    value = int(''.join(list), 16)
    return value
    

bfOffBitsData = func(data, bfOffBitsStart, bfOffBits)
print('bfOffBitsData: ' + str(bfOffBitsData))

bfWidthData = func(data, bfWidthStart, bfWidth)
print('bfWidthData: ' + str(bfWidthData))

bfHeightData = func(data, bfHeightStart, bfHeight)
print('bfHeightData: ' + str(bfHeightData))

# Data must be every 4byte
# So, padding is reminder of the data
padding = 0 if (bfWidthData % 4 == 0) else (4-(bfWidthData%4))*2
print('padding: '+str(padding))

palette = []
paletteAddress = bfOffBitsData*2
paletteDataSize = (bfWidthData*2+padding)*(bfHeightData*2+padding)
for i in range(paletteAddress, paletteAddress+((bfWidthData*2+padding)*bfHeightData))[::bfWidthData*2+padding]:
    palette.append(data[i : i+(bfWidthData*2)])
palette.reverse()
palette = ''.join(palette)
bitData = ''
# Write ascii charcter '0' or '1'
for i in range(0, bfWidthData*bfHeightData):
    if palette[i*2] == '0':
        bitData += chr(1)
    else:
        bitData += chr(0)
bitData = bitData.strip()
print('Data: ' + str(bitData))
file = open('data', 'w')
file.write(bitData)
file.closed

