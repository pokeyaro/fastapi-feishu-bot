# -*- coding: utf-8 -*-
from Crypto import Random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class EncryptAES:

    """
    pip install pycryptodome

    AES加密方式有五种：ECB, CBC, CTR, CFB, OFB
    CBC加密需要一个十六位的key(密钥)和一个十六位iv(偏移量)  常用
    ECB加密不需要iv
    cryptor不能写在主函数中同时给加密函数与解密函数使用，所以加密和解密都要重新创建对象
    """

    _secret_key = "ZLUc@a0DgWC716Wb"
    _secret_vector = b'\xa6\x97\x1a\xec\xd4\xe7\x82cG\x11\xfb\x0e\x7f)\xd1\x9b'

    def __init__(self, key=None, mode=AES.MODE_CBC, iv=None):
        """
        key 秘钥必须是16（AES-128）,24, 32
        iv 长度等于AES块大小的不可重复的秘钥向量
        本类内实现了 ECB, CBC 两种加密模式，默认为 AES.MODE_CBC 加密模式
        """
        self.mode = mode

        if key is None:
            self.key = self._secret_key.encode('utf-8')
        else:
            self.key = str(key).encode('utf-8')

        if iv is None:
            self.iv = self._secret_vector
        else:
            self.iv = Random.new().read(AES.block_size)

    @staticmethod
    def _add_to_16(text):
        """ 如果string不足16位则用空格补齐16位 """
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text += ("\0" * add)
        return text.encode('utf-8')

    def encode_aes(self, text) -> str:
        """ 使用 AES 加密字符串 """
        if self.mode == AES.MODE_ECB:
            cryptos = AES.new(key=self.key, mode=self.mode)
        else:
            cryptos = AES.new(key=self.key, mode=self.mode, iv=self.iv)
        cipher_text = cryptos.encrypt(self._add_to_16(text))
        # 由于AES加密后的字符串不一定是ascii字符集，所以转为16进制字符串
        return b2a_hex(cipher_text).decode('utf-8')

    def decode_aes(self, text) -> str:
        """ 使用 AES 解密 并去掉补足的空格 """
        if self.mode == AES.MODE_ECB:
            cryptos = AES.new(key=self.key, mode=self.mode)
        else:
            cryptos = AES.new(key=self.key, mode=self.mode, iv=self.iv)
        plain_text = cryptos.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip("\0")


if __name__ == '__main__':
    p = EncryptAES()
    result = p.encode_aes("root")
    print(result)
    r = p.decode_aes("b69611b50aa877aeb40dab9c2c83da46")
    print(r)
