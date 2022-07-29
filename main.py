import cv2 #pip install opencv-python

split_byte_to_bits = lambda data: [data >> 5, (data>>2)& 0x7, data & 0x3]
extract_nbits_of_byte = lambda band, n : band & (2**n-1)
merge_bits = lambda rbits,gbits, bbits :(((rbits<< 3) | gbits) << 2) | bbits

def embed(vessel_image, string, target_image):
    #load the image in memory
    mem_image = cv2.imread(vessel_image, cv2.IMREAD_COLOR)
    #type(mem_image) --> numpy.ndarray
    #mem_image.shape --> height, width, pixelsize(bgr)
    h,w,_ = mem_image.shape

    index = 0
    max_size = len(string)

    #reading the pixels of the image
    for i in range(h): #for each row
        if index == max_size:
            break

        for j in range(w): #for each col of the row
            if index == max_size:
                break
            #fetch a pixel
            pixel = mem_image[i,j]
            blue = pixel[0]
            green = pixel[1]
            red = pixel[2]

            #fetch a character from the string
            ch = string[index]
            bits = split_byte_to_bits(ord(ch))

            #free the last 3 bits of red and green
            red = red & (~0x7)
            green = green & (~0x7)
            # free the last 2 bits of blue
            blue = blue & (~0x3)

            #merge
            red = red | bits[0]
            green = green | bits[1]
            blue = blue | bits[2]

            #update the mem_image_pixel[i,j]
            mem_image[i, j, 0] = blue
            mem_image[i, j, 1] = green
            mem_image[i, j, 2] = red

            index+=1

    #save back
    cv2.imwrite(target_image, mem_image)

def extract(image_with_embedding):
    #load the image in memory
    mem_image = cv2.imread(image_with_embedding, cv2.IMREAD_COLOR)
    #type(mem_image) --> numpy.ndarray
    #mem_image.shape --> height, width, pixelsize(bgr)
    h,w,_ = mem_image.shape

    index = 0
    max_size = 26 #len(string)
    string = ''

    #reading the pixels of the image
    for i in range(h): #for each row
        if index == max_size:
            break

        for j in range(w): #for each col of the row
            if index == max_size:
                break
            #fetch a pixel
            pixel = mem_image[i,j]
            blue = pixel[0]
            green = pixel[1]
            red = pixel[2]

            #fetch the last 3 bits of red and green
            red_bits = red & 0x7
            green_bits = green & 0x7
            # fetch the last 2 bits of blue
            blue_bits = blue & 0x3

            #merge the bits to form a byte
            ch = chr(merge_bits(red_bits, green_bits, blue_bits))
            string = string + ch

            index+=1

    return string


def main():
    embed('C:/Users/DELL/OneDrive/Desktop/Stegnanography/Stegnanography_using_OpenCV/e_kids.png', 'This is a sample sentence!', 'C:/Users/DELL/OneDrive/Desktop/Stegnanography/Stegnanography_using_OpenCV/e_kids.png')
    print('Embedding Done')
    string = extract('C:/Users/DELL/OneDrive/Desktop/Stegnanography/Stegnanography_using_OpenCV/e_kids.png')
    print(string)

main()