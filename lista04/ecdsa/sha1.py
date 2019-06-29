def sha1(data):
    bytes = ""

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for n in range(len(data)):
        bytes+='{0:08b}'.format(ord(data[n]))
    bits = bytes+"1"
    pBits = bits
    
    # Padding
    while len(pBits)%512 != 448:
        pBits+="0"
    
    pBits+='{0:064b}'.format(len(bits)-1)

    print(pBits)
   

    return 'mensagem'
