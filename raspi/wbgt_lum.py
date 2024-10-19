#!/usr/bin/env python3
# coding: utf-8

################################################################################
# 温湿度センサ SENSIRION SHT31 と照度センサ BH1750FVI から温湿度と照度を取得し、
# WBGT に換算します。
# 
# 詳細情報：
# https://bokunimo.net/blog/raspberry-pi/5036/
# ※本スクリプトは独自の推定条件に基づいています。
# ※使用される場合は、十分に検証してください。
# ※不具合や考え違いなどがあったとしても、当方は一切の責任を負いません。
#
#                                               Copyright (c) 2024 Wataru KUNINO
################################################################################

################################################################################
# ご注意 #######################################################################
################################################################################
# 本プログラムは、筆者による想定や独自の解釈が含まれています。                 #
# 主にインターネットにて調べた内容に基づいていますが、誤った内容が含まれている #
# 可能性があります。                                                           #
# ご指摘いただいた場合は、訂正や加筆いたしますが、それ以上の責任は負いません。 #
# 予めご容赦いただき、十分に検証してから、ご活用ください。                     #
################################################################################

sht31  = 0x44                                       # SHT31 0x44 又は 0x45
bh1750 = 0x23                                       # 照度センサBH1750FVI

wbgt_ver = 3                                        # WBGTバージョン 3または4
wbgt_wide = True                                    # 筆者の独自拡張Wide版

import smbus
from time import sleep                              # 時間取得を組み込む

def word2uint(d1,d2):
    i = d1
    i <<= 8
    i += d2
    return i

i2c = smbus.SMBus(1)
math_pi = 3.1415927                                 # 円周率
temp = 0.                                           # 温度値を保持する変数
hum  = 0.                                           # 湿度値を保持する変数
lux  = 0.                                           # 照度値を保持する変数
wbgt = 0.                                           # WGBTを保持する変数
phantom_s = (0.58 / (2*math_pi))**2 * math_pi       # 照射面積(m2)

while i2c:
    i2c.write_byte_data(sht31,0x24,0x00)
    sleep(0.018)
    data = i2c.read_i2c_block_data(sht31,0x00,6)
    data += i2c.read_i2c_block_data(bh1750,0x21,2)
    if len(data) == 8:
        temp = float(word2uint(data[0],data[1])) / 65535. * 175. - 45.
        hum  = float(word2uint(data[3],data[4])) / 65535. * 100.
        lux  = float(word2uint(data[6],data[7])) / 1.2
        if wbgt_ver == 3 and wbgt_wide == False:
            wbgt = 0.687 * temp + 0.0360 * hum + 0.00367 * temp * hum - 2.062
        elif wbgt_ver == 3 and wbgt_wide == True:
            wbgt = 0.725 * temp + 0.0368 * hum + 0.00364 * temp * hum - 3.246
        elif wbgt_ver == 4 and wbgt_wide == False:
            wbgt = 0.724 * temp + 0.0342 * hum + 0.00277 * temp * hum - 3.007
        elif wbgt_ver == 4 and wbgt_wide == True:
            wbgt = 0.754 * temp + 0.0382 * hum + 0.00264 * temp * hum - 3.965
        print("Temp. = %.2f ℃, Humid. = %.0f ％" % (temp,hum),end='')
        print(", Ilum. = %.0f lx" % lux, end='')
        print(", WBGT = %.2f ℃" % wbgt, end='')
        
        # 照度分をWGBTに加算する計算
        Psun_w = 6e-3 * lux * math_pi * phantom_s
        delta = 0.8 * Psun_w * 1.5 * 3600 / 5 / (4184 * (0.37 + 0.63 * 0.55))
        wbgt_lum = wbgt + delta
        print(", WBGT_lum = %.2f ℃" % wbgt_lum)
    sleep(1)

''' ----------------------------------------------------------------------------
実行例(一部修正)
Temp.=29.20 ℃, Humid.=70 ％, Ilum.=108 lx, WBGT=27.93 ℃, WBGT_lum=27.94 ℃
Temp.=29.20 ℃, Humid.=70 ％, Ilum.=103 lx, WBGT=27.93 ℃, WBGT_lum=27.94 ℃
Temp.=29.20 ℃, Humid.=70 ％, Ilum.=60 lx, WBGT=27.93 ℃, WBGT_lum=27.93 ℃
Temp.=29.21 ℃, Humid.=70 ％, Ilum.=12854 lx, WBGT=27.95 ℃, WBGT_lum=28.55 ℃
Temp.=29.24 ℃, Humid.=70 ％, Ilum.=10190 lx, WBGT=27.98 ℃, WBGT_lum=28.45 ℃
Temp.=29.21 ℃, Humid.=70 ％, Ilum.=53420 lx, WBGT=27.95 ℃, WBGT_lum=30.42 ℃
Temp.=29.21 ℃, Humid.=70 ％, Ilum.=17812 lx, WBGT=27.96 ℃, WBGT_lum=28.78 ℃
Temp.=29.18 ℃, Humid.=70 ％, Ilum.=3169 lx, WBGT=27.93 ℃, WBGT_lum=28.08 ℃
Temp.=29.21 ℃, Humid.=70 ％, Ilum.=7770 lx, WBGT=27.99 ℃, WBGT_lum=28.35 ℃
Temp.=29.21 ℃, Humid.=71 ％, Ilum.=4394 lx, WBGT=28.03 ℃, WBGT_lum=28.23 ℃
--------------------------------------------------------------------------------
参考文献1
  Raspberry Pi で 暑さ指数 WBGT その4: 照度の影響を考える
  https://bokunimo.net/blog/raspberry-pi/5036/  2024年10月19日 Wataru KUNINO
--------------------------------------------------------------------------------
参考文献2
  Raspberry Pi で 暑さ指数 WBGT その3: ラズパイ Pico 2
  https://bokunimo.net/blog/raspberry-pi/4988/  2024年9月16日 Wataru KUNINO
--------------------------------------------------------------------------------
参考文献3
  温湿度センサ SENSIRION SHT31 から温度と湿度を取得します。
  https://github.com/bokunimowakaru/RaspberryPi/blob/master/gpio/raspi_sht31.py
                                                Copyright (c) 2021 Wataru KUNINO
--------------------------------------------------------------------------------
参考文献4
  IchigoJam S+温湿度センサSi7021で暑さ指数WBGTを計算して、熱中症予防
  https://bokunimo.net/blog/ichigo-jam/29/      2018年8月11日 Wataru KUNINO
---------------------------------------------------------------------------- '''
