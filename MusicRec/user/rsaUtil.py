import base64
import os

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

current_path = os.path.dirname(__file__)


def decrypt(cipher_text):
    """
        RSA私钥解密
    :param cipher_text: string,加密后的字符串
    :return: str || False
        成功解密则返回解密后的str,解密失败返回False
    """
    with open('D:/MusicRec/MusicRec/user/key/ghost_private.pem') as f:
        key = f.read()
        # 导入读取到的私钥
        rsa_key = RSA.importKey(key)
        # 生成对象
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        # 将密文解密成明文，返回的是一个bytes类型数据，需要转换成str
        text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR")
        if text != 'ERROR':
            return str(text, encoding='utf-8')
        else:
            return False


def encrypt(text):
    """
        RSA公钥加密文本
    :param text: str    加密的文本
    :return: bytes  加密后的文本
    """
    with open('D:/MusicRec/MusicRec/user/key/ghost_public.pem', "r") as f:
        key = f.read()
        # 导入读取到的公钥
        rsa_key = RSA.importKey(key)
        # 生成对象
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        # 通过生成的对象加密明文text，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
        cipher_text = base64.b64encode(cipher.encrypt(
            text.encode()))
        return cipher_text


# 通过公钥加密qaz123456的默认密码,每次生成结果不一，只取其中一个
default_password = 'lgvjXx6Lk7Ah2mIkOrT6ZMBfYbCTSGNkjhtJNALAVyssYJtF0aEyThReYaiK+5HL' \
                   '9VSbVhzTYpeX9rwLmpIhKL+GH5La3axrET/JV+u4IOBRNpe/KiLykgzCBiwZTnjUa6W' \
                   'x6Bbplopb9eJ+0xJOCNLn8ZMfbgFzY1343l9V1DaV7dOFXYhkKL+CaJi5sDrfoJPiak7OP' \
                   '0vJTN48WwKjvLJ1O/hcBFqIZl/9nRLYTVHoUc9qzvdKFMfSCxbvUghxo5pY/jbBT14zUARLl' \
                   '7HHYykyCsPXjZAVRmx5KhS5Rwhzpoa6ZtLZ5Jhn4NfcafHphnlwCzay5Svy6hL6ndWWEg=='


# 前端发送数据到后端----------前端公钥加密，后端私钥解密
# 后端发送数据到前端----------后端私钥签名，前端公钥验签
class RsaUtil:
    # 伪随机数生成器
    random_generator = Random.new().read
    # rsa算法生成实例
    rsa = RSA.generate(2048, random_generator)
    
    # master的秘钥对的生成
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    
    # def __init__(self):
    #     # ----------------生成公私钥对文件-----------
    #     with open('key/master_private.pem', 'wb') as file:
    #         file.write(self.private_pem)
    #
    #     public_pem = self.public_pem
    #     with open('key/master_public.pem', 'wb') as file:
    #         file.write(public_pem)
    #
    #     # ghost的秘钥对的生成,跟之前的一样
    #     private_pem = self.rsa.exportKey()
    #     with open('key/ghost_private.pem', 'wb') as file:
    #         file.write(private_pem)
    #
    #     public_pem = self.public_pem
    #     with open('key/ghost_public.pem', 'wb') as file:
    #         file.write(public_pem)


if __name__ == '__main__':

    rsaUtil = RsaUtil()
    test = "Y5pLnacjHXpXppBI00kUexQRMQ59UKa8FT85I/3WQ4pLeVJgTrNPAqiufXEKAtLHAQJHF1F2g+iy93dNRKiYgZzEfXabUqqMkFxiq1PBx9BK7XkmXUActLrY8pDdcMAvgpbxeOGNH78fqEynGHDqKrE8rJEdzBrDmC+e5yagGrQfMvs3wypdEQyS6Np2zG8suPOSW8KYIWlsrqvc8CpJCICNVdCZwcCGvz7Gzg/eWK+q3SzrT6Lu0XCrkxwLHV87met6EhLmQW53yUqsE126hbIplnwyqpWrvVIX32YOu+2YBqnb4RDErztULmfcn6HQpUmaw220rDsM2uECh99IQg=="
    print(test)
    print(decrypt(test))

