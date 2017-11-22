from hashlib import sha1

def get_hash(str):
    '''获取一个字符串的hash值'''
    sh = sha1()  # 实例化一个hash类对象
    sh.update(str.encode("utf8"))  # hash算法只对于byte类型 因此取hash前需要编码
    return sh.hexdigest()  # 获取到使用sha1算法得到的字符串




# from hashlib import sha1
#
# sh = sha1()
# sh.update("12345678".encode("utf-8"))
# print(sh.hexdigest())
#
# str1 = "7c222fb2927d828af22f592134e8932480637c0d"
# len(str1)
