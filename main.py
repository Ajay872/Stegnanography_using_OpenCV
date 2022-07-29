#split the byte into bits
#def split(data): #data: 104 ---> [3,2,0]
    #extract last 2 bits
    #blue_bits = data & 0x3
    #lose last 2 bits
    #data  = data >> 2
    #extra 3 bits
    #green_bits = data & 0x7
    #lose last 3 bits
    #red_bits = data >> 3
    #return [red_bits, green_bits, blue_bits]
    #return [data >> 5, (data>>2)& 0x7, data & 0x3]


#l = split(ord('h'))
#print(l)

# def extract_bits(band, n):
#     return band & (2**n -1)

#def merge_bits(rbits, gbits, bbits):
    #data = rbits
    #data = data << 3 # make room for 3 bits
    #data = data | gbits # merge the gbits
    #data = data << 2 #make room for 2 bits
    #data = data | bbits
    #return data
    #return (((rbits<< 3) | gbits) << 2) | bbits

split = lambda data: [data >> 5, (data>>2)& 0x7, data & 0x3]
extract_bits = lambda band, n : band & (2**n-1)
merge_bits = lambda rbits,gbits, bbits :(((rbits<< 3) | gbits) << 2) | bbits

def main():
    print('Enter data (0-255) : ')
    x = int(input()) #104 (h)
    print(x)
    bits = split(x)
    print(bits)

    #extract
    a = extract_bits(bits[0], 3)
    b = extract_bits(bits[1], 3)
    c = extract_bits(bits[2], 2)
    data = merge_bits(a,b,c)
    print(data, chr(data))

main()