from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Получение данных изображения
def get_img_data(path):
    img = Image.open(path).convert('RGBA')
    byte_img = img.tobytes()
    size = len(byte_img)
    exp_len = (size + 16 - size % 16) - size
    byte_img += (b'\x00' * exp_len)
    return [img.mode, img.size, [byte_img[i:i+16] for i in range(0, len(byte_img), 16)]]


# Преобразование байтов в целые числа
def data_to_int(img_bytes):
    return [int.from_bytes(i, byteorder='big', signed=False) for i in img_bytes]


# Шифрование изображения с использованием AES
def encryptAES(path, key, iv, keySize):

    imgEncArray = (get_img_data(path))

    imgMode = imgEncArray[0]
    imgSize = imgEncArray[1]
    imgInt = data_to_int(imgEncArray[2])

    encData = []
    aes_cipher = AES.new(key.to_bytes(keySize, byteorder='big'), AES.MODE_CBC, iv)
    for block in imgInt:
        secret_block = aes_cipher.encrypt(block.to_bytes(16, byteorder='big'))
        encData.append(secret_block)

    return [encData, imgMode, imgSize]


# Расшифровка изображения, зашифрованного с использованием AES
def decryptAES(path, key, iv, keySize):

    imgDecArray = (get_img_data(path))

    imgMode = imgDecArray[0]
    imgSize = imgDecArray[1]
    imgEncInt = data_to_int(imgDecArray[2])

    decData = []
    aes_cipher = AES.new(key.to_bytes(keySize, byteorder='big'), AES.MODE_CBC, iv)
    for block in imgEncInt:
        img_block = aes_cipher.decrypt(block.to_bytes(16, byteorder='big'))
        imgInt = img_block
        decData.append(imgInt)

    return [decData, imgMode, imgSize]


# Запуск шифрования и расшифровки изображения с использованием сторонней библиотеки
def encByLibRun(path, origFN, keyInt, iv, keySize):
    
    encFN = '\\encByLibImg.png'
    decFN = '\\decByLibImg.png'

    imgPath = path+origFN

    iv = get_random_bytes(16)

    # Шифрование изображения
    encData = encryptAES(imgPath, keyInt, iv, keySize)

    data = b''.join(encData[0])
    enc = Image.frombytes(encData[1], encData[2], data)
    enc.save(path+encFN, format='PNG')

    print('\n   E N C R Y P T E D by lib\n')

    encPath = path + encFN

    # Расшифровка изображения
    decData = decryptAES(encPath, keyInt, iv, keySize)

    data = b''.join(decData[0])
    dec = Image.frombytes(decData[1], decData[2], data)
    dec = dec.quantize(colors=256, method=2)
    dec.save(path+decFN, format='PNG')

    print('\n   D E C R Y P T E D by lib\n')

