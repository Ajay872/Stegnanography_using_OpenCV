#split the byte into bits
def split(data): #data: 104 ---> [3,2,0]
    #extract last 2 bits
    #blue_bits = data & 0x3
    #lose last 2 bits
    #data  = data >> 2
    #extra 3 bits
    #green_bits = data & 0x7
    #lose last 3 bits
    #red_bits = data >> 3
    #return [red_bits, green_bits, blue_bits]
    return [data >> 5, (data>>2)& 0x7, data & 0x3]

l = split(ord('h'))
print(l)