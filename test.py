# Author: David Allen
#
# created using the ideas from 
# http://blog.iconfinder.com/detecting-duplicate-images-using-python/

from PIL import Image
import sys
import os

#Global image hash dict
#Move from global later (possible use high order func)
image_hash = {}

def dhash(img, size = 16):
    width = size + 1
    height = size

    img = Image.open(img).convert('L')
    img = img.resize((width, height))
    px = img.load()
    
    hash_array = []
    for x in range(width-1):
        for y in range(height):
            # print(px[x, y])
            if px[x,y] > px[x+1,y]:
                hash_array.append('1')
            else:
                hash_array.append('0')
    
    l = len(hash_array)
    hex_val = 0
    dh = []
    for x in range(l):
        if hash_array[x] == '1':
            hex_val += 2**(x % 8)
        if x % 8 == 7:
            # print(hex_val)
            dh.append(hex(hex_val)[2:].rjust(2, '0'))
            hex_val = 0

    return ''.join(dh)

# From wikipedia
def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1, s2))

def get_input(msg, good_input):
    answer = raw_input(msg)
    while (answer not in good_input):
        answer = raw_input(msg)
    return answer

def del_one(img1, img2):
    img1_name = img1
    img2_name = img2
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    img1.show()
    img2.show()

    print(img1.size)
    print(img2.size)
    sfile = img1_name
    bfile = img2_name

    if (img1.height * img1.width < img2.height * img2.width):
        print(img1_name + " is smaller.\n")
        sfile = img1_name
        bfile = img2_name
    elif (img1.height * img1.width > img2.height * img2.width):
        print(img2_name + " is smaller.\n")
        sfile = img2_name
        bfile = img1_name
    else:
        print("The files are the same size.\n")

    good_inputs = ['n', 'N', 'y', 'Y']
    answer = get_input("Would you like to delete one of the files? ", good_inputs)
    if (answer == 'y' or answer == 'Y'):
        answer = get_input("Would you like to delete " + sfile + " ? ", good_inputs)
        if (answer == 'n' or answer == 'N'):
            answer = get_input("Would you like to delete " + bfile + " ? ", good_inputs)
            if (answer == 'y' or answer == 'Y'):
                os.remove(bfile)
        else:
            os.remove(sfile)

def is_image(tfile):
    try:
        Image.open(tfile)
    except IOError:
        return False
    return True

def compare(img1, img2, size=16):
    if img1 in image_hash:
        hash_1 = image_hash[img1]
    else:
        hash_1 = dhash(img1, size)
        image_hash[img1] = hash_1

    if img2 in image_hash:
        hash_2 = image_hash[img2]
    else:
        hash_2 = dhash(img2, size)
        image_hash[img2] = hash_2

    hd = hammingDistance(hash_1, hash_2)
    ret = None
    similarity = 100 - int(100 * (float(hd)/(size*size)))

    if similarity >= 90:
        ret = (True, similarity)
        print(str(similarity) + "% similar.")
    else:
        ret = (False, similarity)

    if ret[0]:
        del_one(img1, img2)

    return ret[0]

def main(argv):
    print("Hello There!\nDavids image comparator.")
    path = "."
    count = 0
    if len(argv) == 1:
        path = argv[0]
    if not os.path.exists(path):
        print("does not work")
        return 1
    print("Comparing files in " + path)

    image_files = []

    for root, dirs, files in os.walk(path):
        files = [os.path.join(path, f) for f in files if is_image(os.path.join(path, f))]
        image_files += files

    num_files = len(image_files)
    for x in range(num_files - 1):
        for y in range(x + 1, num_files):
            try:
                if (compare(files[x], files[y])):
                    count += 1
            except IOError:
                continue

    print("Found {} similar images.".format(count))
    
    return None

if __name__ == "__main__":
    main(sys.argv[1:])
