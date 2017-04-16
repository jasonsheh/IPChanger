#!/usr/bin/python
# __author__ = 'jasonsheh'
# -*- coding:utf-8 -*-

import winreg
import binascii

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections",
                     0, winreg.KEY_ALL_ACCESS)

# 获取该键的所有键值，遍历枚举


def to_byte(obj):
    return str(obj).encode(encoding="utf-8")

try:
    # value, _type = winreg.QueryValueEx(key, "DefaultConnectionSettings")

    ip = b'110.77.197.111:8080'
    ip_length = to_byte(hex(len(ip)).replace('0x', ''))

    ip_length_hex = binascii.hexlify(ip_length)
    ip_hex = binascii.hexlify(ip)

    # print(ip_length)
    # print(ip_length_hex)
    # print(ip_hex)

    value = b'46000000da020000' \
            b'03000000%s000000' \
            b'%s00000000210000' \
            b'0100000000000000' \
            b'0000000000000000' \
            b'0000000000000000' \
            b'0000000000000000' % (ip_length, ip_hex)

    default_value = b'46000000da020000' \
                    b'0100000000000000' \
                    b'0000000000000000' \
                    b'0100000000000000' \
                    b'0000000000000000' \
                    b'0000000000000000' \
                    b'0000000000000000'

    '''
    value = r'4600000da020000' \
            r'01000000%s000000' \
            r'0000000000000000' \
            r'0100000000000000' \
            r'0000000000000000' \
            r'0000000000000000' \
            r'0000000000000000' % (to_hex(ip_length))
    '''

    winreg.SetValueEx(key, "DefaultConnectionSettings", 0, winreg.REG_BINARY, binascii.unhexlify(value))
    # print(value, '\n', _type)
    # print(value)
    # print(binascii.unhexlify(value))
    # print(ip_hex)

    key.Close()

except WindowsError:
    print('error')

