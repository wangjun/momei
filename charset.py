#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""简单猜测字符串编码并返回 Unicode 字符串
"""

def decode_(str_):
    """
    """
    text = str_
    charests = ('utf8', 'gbk', 'gb2312', 'big5', 'ascii',
                'shift_jis', 'euc_jp', 'euc_kr', 'iso2022_kr',
                'latin1', 'latin2', 'latin9', 'latin10', 'koi8_r',
                'cyrillic', 'utf16', 'utf32'
                 )
    if isinstance(text, unicode):
        return text
    else:
        for i in charests:
            try:
                return text.decode(i)
                break
            except:
                pass
        else:
            return None

if __name__ == '__main__':
    text = 'abc你'
    print repr(decode_(text))
