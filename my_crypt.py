"""
    以下encSecKey、AES_Encrypt等有关解密的函数来源于知乎,感谢提供
    参考：https://www.zhihu.com/question/36081767
    获取params 注意：评论每一次翻页后的的params都不一样

"""

import base64

from Crypto.Cipher import AES

def get_params(first_param, forth_param):
    i_v = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    h_enc_text = AES_Encrypt(first_param, first_key.encode(), i_v.encode())
    h_enc_text = AES_Encrypt(
        h_enc_text.decode(), second_key.encode(), i_v.encode())
    return h_enc_text.decode()


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def AES_Encrypt(text, key, i_v):
    """AES Encrypt"""
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, i_v)
    encrypt_text = encryptor.encrypt(text.encode())
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def crypt_api(music_id, offset):
    """传入post数据"""
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token=".format(music_id)
    first_param = '''{rid:"", offset:"%s", total:"true", limit:"20", csrf_token:""}''' % offset
    forth_param = "0CoJUm6Qyw8W8jud"
    params = get_params(first_param, forth_param)
    encSecKey = get_encSecKey()
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    return url, data
