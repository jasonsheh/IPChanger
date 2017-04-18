#!/usr/bin/python
# __author__ = 'jasonsheh'
# -*- coding:utf-8 -*-

import winreg
import binascii
import ctypes


def to_byte(obj):
    return str(obj).encode(encoding="utf-8")


def pppoe_changer():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections',
                             0, winreg.KEY_ALL_ACCESS)

        ip = b'ip'
        ip_length_hex = to_byte(hex(len(ip)).replace('0x', ''))
        ip_hex = binascii.hexlify(ip)

        value = b'46000000da020000' \
                b'03000000%s000000' \
                b'%s00000000210000' \
                b'0100000000000000' \
                b'0000000000000000' \
                b'0000000000000000' \
                b'0000000000000000' % (ip_length_hex, ip_hex)

        default_value = b'46000000da020000' \
                        b'0100000000000000' \
                        b'0000000000000000' \
                        b'0100000000000000' \
                        b'0000000000000000' \
                        b'0000000000000000' \
                        b'0000000000000000'
        # enable
        winreg.SetValueEx(key, "DefaultConnectionSettings", 0, winreg.REG_BINARY, binascii.unhexlify(value))

        # disable
        winreg.SetValueEx(key, "DefaultConnectionSettings", 0, winreg.REG_BINARY, binascii.unhexlify(default_value))

        key.Close()
    except WindowsError:
        print('error')


def lan_changer():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                 0, winreg.KEY_ALL_ACCESS)
        flag = int(input('flag:'))

        if flag:
            # enable
            print('启用代理')
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "202.121.96.33:8086")
        else:
            # disable
            print('取消代理')
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    except WindowsError:
        print('error')

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
    internet_set_option(0, 37, 0, 0)
    internet_set_option(0, 39, 0, 0)


def main():
    lan_changer()

if __name__ == '__main__':
    main()
