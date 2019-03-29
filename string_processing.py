# -*- coding:utf-8 -*-
# @DateTime     : 2019-03-27 15:02 
# @Author       : WangTao master
# @Email        : cs.power.supply@gmail.com
# @FileName     : string_processing.py
# @Editor       : PyCharm


# 1. python 字符串处理, 对字符串进行数组化处理,每个字母为一个值.
def str_proc(str):
    for a in range(len(str)):
        if type(str[a]) == list:

            str_proc(str[a])

        else:
            print('-------------str[%d]=%s' % (a, str[a]))


str01 = 'ABCDE abcde'
str02 = ['abcde',
         'fghij',
         'klmno',
         'pqrst',
         'uvwxyz',
         '01234',
         '56789']
str03 = ('12345ab', 'assda', ['sdfdf', 'dfsdfasdfsd', '323'], 'dfsadf', '555555')

# str_proc(str01)
# str_proc(str02)
str_proc(str03)
