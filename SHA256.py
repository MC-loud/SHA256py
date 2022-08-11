def main(arg):

    #Creates a multiple of 512 binary string
    block_multiple = pre_process(arg)

    h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

    k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    #Converts all items in k from hex to binary
    kbin = []
    for i in k:
        kbin.append(bin(i)[2:].zfill(32))
    w = []

    #Splits input into 512-bit chunks and puts into array w
    for i in range(int(len(block_multiple)/512)):
        w.append(block_multiple[i*512:i*512+512])

    #Initialize 32 characters in 64 segments in an array for each 512-bit chunk
    w2 = [['00000000000000000000000000000000' for i in range(64)]
           for x in range(len(w))]
    
    #Following steps occur for each 512-bit chunk   
    

    #64 indices of 32-bits
    for i in range(len(w)):
        for x in range(16):
            w2[i][x] = w[i][x*32:x*32+32]
    del w

    for i in range(len(w2)):
        for x in range(16,64):
            a1 = right_rotate(w2[i][x-15],7)
            b1 = right_rotate(w2[i][x-15],18)
            c1 = right_shift(w2[i][x-15],3)
            
            s0 = sxor(a1,b1,c1)
            a2 = right_rotate(w2[i][x-2],17)
            b2 = right_rotate(w2[i][x-2],19)
            c2 = right_shift(w2[i][x-2],10)

            s1 = sxor(a2,b2,c2)
            a = bin_addition(w2[i][x-16],w2[i][x-7])
            b = bin_addition(s0,s1)
            w2[i][x] = bin_addition(a,b)

    for i in range(0,len(w2)):
        hbin = []
        for b in h:
            hbin.append(bin(b)[2:].zfill(32))
        for j in range(0,64):
            s1 = sxor(right_rotate(hbin[4],6),right_rotate(hbin[4],11),right_rotate(hbin[4],25))

            ch1 = bin(int(hbin[4],2) & int(hbin[5],2))[2:].zfill(32)
                
            ch2 = bin((int(snot(hbin[4]),2)) & int(hbin[6],2))[2:].zfill(32)
            ch = ''.join(format(ord(a), '') for a in (sxor2(ch1,ch2)))
            temp1 = bin_addition5(hbin[7], s1, ch, kbin[j], w2[i][j])

            s0 = sxor(right_rotate(hbin[0],2), right_rotate(hbin[0],13), right_rotate(hbin[0],22))
            maj = sxor(bin((int(hbin[0],2)) & int(hbin[1],2))[2:].zfill(32),bin((int(hbin[0],2)) & int(hbin[2],2))[2:].zfill(32),bin((int(hbin[1],2)) & int(hbin[2],2))[2:].zfill(32))

            temp2 = bin_addition(s0, maj)

            hbin[7] = hbin[6]
            hbin[6] = hbin[5]
            hbin[5] = hbin[4]
            hbin[4] = bin_addition(hbin[3], temp1)
            hbin[3] = hbin[2]
            hbin[2] = hbin[1]
            hbin[1] = hbin[0]
            hbin[0] = bin_addition(temp1, temp2)
        for i in range(0,8):
            h[i] = int(bin_addition(bin(h[i])[2:].zfill(32), hbin[i]),2)

    #Appends the formulated h-values
    digest = ''
    for i in h:
        digest += hex(i)[2:].zfill(8)
    print('SHA256:', digest)

def pre_process(input):
    try:
        file = open(input,"rb")
        string = file.read()
    except:
        string = input
    finally:
        binary_rep = ''.join(format(ord(i), '08b') for i in string)
        binary_rep2 = binary_rep + '1'
        block_multiple = 512
        while len(binary_rep2) > (block_multiple-64):
            block_multiple += 512
        while len(binary_rep2) + 64 < block_multiple:
            binary_rep2+='0'
        big_endian = "{0:b}".format(len(binary_rep))
        for i in range(64-len(big_endian)):
            binary_rep2 +='0'
        binary_rep2 +=big_endian
        return(binary_rep2)

def right_rotate(input, factor):

    return input[len(input)-factor:len(input)] + input[0:len(input)-factor]

def right_shift(input, factor):
    i = ''
    for x in range(factor):
        i +='0'
    return i + input[0:len(input)-factor]

def sxor2(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def sxor(s1, s2, s3):
    return ''.join(chr(ord(a) ^ ord(b) ^ ord(c)) for a,b,c in zip(s1,s2,s3))

def snot(s):
    s1 = ''
    for i in s:
        if (i == '1'):
            s1 += '0'
        else:
            s1 += '1'
    return s1

def format2(s):
    s1 = ''
    for i in range(1,len(s)):
        if ((i-1)%4):
            s1 += s[i]
    return s1

def bin_addition(s1, s2):
    sum = int(s1, 2) + int(s2, 2)
    if (sum >=pow(2,32)):
        sum -= pow(2,32)
    return bin(sum)[2:].zfill(32)

def bin_addition5(s1, s2, s3, s4, s5):
    return bin_addition(bin_addition(bin_addition(bin_addition(s1,s2),s3),s4),s5)

if __name__ == "__main__":
    print('Enter a string: ')
    input = input()
    main(input)