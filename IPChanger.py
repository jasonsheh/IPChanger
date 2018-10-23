#!/usr/bin/python
# __author__ = 'jasonsheh'
# -*- coding:utf-8 -*-

import winreg
import binascii
import ctypes
import argparse
from FreeHttpProxy import FreeHttpProxy


class IPChanger:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--enable',
                            help='set proxy', action="store_true")
        parser.add_argument('-d', '--disable',
                            help='disable proxy', action="store_true")
        parser.add_argument('-p', '--proxy',
                            help="assign proxy")

        args = parser.parse_args()

        if args.enable:
            self.mode = True

            if args.proxy:
                self.proxy = args.proxy
            else:
                print("# 未指定代理, 自动从网络获取")
                self.proxy = FreeHttpProxy().get()[0]['http'].split("//")[1]
                print("# 自动获取到: ", self.proxy)

        elif args.disable:
            self.mode = False

        self.key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                  0, winreg.KEY_ALL_ACCESS)

    @staticmethod
    def to_byte(obj):
        return str(obj).encode(encoding="utf-8")

    def run(self):
        try:
            if self.mode:
                # enable
                print('# 启用代理')
                winreg.SetValueEx(self.key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(self.key, "ProxyServer", 0, winreg.REG_SZ, self.proxy)
            else:
                # disable
                print('# 禁用代理')
                winreg.SetValueEx(self.key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        except WindowsError:
            print('error')

        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
        internet_set_option(0, 37, 0, 0)
        internet_set_option(0, 39, 0, 0)

    def pppoe_changer(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections',
                                 0, winreg.KEY_ALL_ACCESS)

            ip = b'ip'
            ip_length_hex = self.to_byte(hex(len(ip)).replace('0x', ''))
            ip_hex = binascii.hexlify(ip)

            change_value = b'46000000da020000' \
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
            winreg.SetValueEx(key, "DefaultConnectionSettings", 0, winreg.REG_BINARY, binascii.unhexlify(change_value))

            # disable
            winreg.SetValueEx(key, "DefaultConnectionSettings", 0, winreg.REG_BINARY, binascii.unhexlify(default_value))

            key.Close()
        except WindowsError:
            print('error')


if __name__ == '__main__':
    IPChanger().run()
