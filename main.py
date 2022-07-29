import cv2 #pip install opencv-python
import os

split_byte_to_bits = lambda data: [data >> 5, (data>>2)& 0x7, data & 0x3]
extract_nbits_of_byte = lambda band, n : band & (2**n-1)
merge_bits = lambda rbits,gbits, bbits :(((rbits<< 3) | gbits) << 2) | bbits

def generate_embedded_imagename(vessel_img):
    #vessel image:- c:/images/kids.jpg
    #embedded image:- c:/images/kids.jpg
    if '/' in vessel_img:
        temp = vessel_img.split('/') # ['c:', 'images', 'kids.jpg']
        temp[-1] = 'e_'+ temp[-1]
        ename = '/'.join(temp)
        if ename.lower().endswith('.jpg'):
            ename = ename.replace('.jpg', '.png')
        elif ename.lower().endswith('.jpeg'):
            ename = ename.replace('.jpeg', '.png')
        return ename
    else:
        print('Use / as separator')
        return None

def generate_header(doc):
    #20 bytes name + 10 bytes size
    #d:/imp_content/secret.docx
    name = doc.split('/')[-1] # [d:, imp_content, secret.docx]

    l = len(name)
    if l >20:
        name = name[l-20:] #trim
    elif l <20:
        name = name.rjust(20, '*') #pad

    size = str(os.path.getsize(doc))
    size = size.rjust(10, '*')
    return name+size

def embed(vessel_image, doc):
    #does the vessel_img and the doc exist?
    if not os.path.exists(vessel_image) :
        print(vessel_image, 'not found')
        return None
    if not os.path.exists(doc) :
        print(doc, 'not found')
        return None

    #load the image in memory
    mem_image = cv2.imread(vessel_image, cv2.IMREAD_COLOR)
    #type(mem_image) --> numpy.ndarray
    #mem_image.shape --> height, width, pixelsize(bgr)
    h,w,_ = mem_image.shape

    #know the size of the document
    doc_size = os.path.getsize(doc)

    #generate the header
    header = generate_header(doc)

    #test the embedding capacity
    capacity =  h*w
    if doc_size + len(header) > capacity:
        print(doc ,' too large to fit in', vessel_image )
        return None

    #embed
    index = 0

    #open the file for reading in binary mode
    file_handle = open(doc, 'rb')
    #reading the pixels of the image
    for i in range(h): #for each row
        if index == doc_size:
            break

        for j in range(w): #for each col of the row
            if index == doc_size:
                break
            #fetch a pixel
            pixel = mem_image[i,j]
            blue = pixel[0]
            green = pixel[1]
            red = pixel[2]

            #fetch a byte from the file
            ch = file_handle.read(1)
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

    file_handle.close()
    #save back
    target_image = generate_embedded_imagename(vessel_image)
    cv2.imwrite(target_image, mem_image)

    return target_image

def main():
    while True:
        print('1. Embed')
        print('2. Extract')
        print('3. Exit')
        print('Enter Choice ')
        ch = int(input())

        if ch == 1:
            print('Enter vessel image path')
            vessel_img = input()
            print('Enter file to embed')
            doc = input()

            result =  embed(vessel_img, doc)
            if result != None:
                print('Embedding Done, result: ', result)
            else:
                print('Embedding Failed')
        elif ch == 2:
            pass
        elif ch == 3:
            break
        else:
            print('Wrong Choice')

main()