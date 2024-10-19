#!/usr/bin/env python3
# coding: utf-8

################################################################################
# 温湿度センサ SENSIRION SHT31 から温度と湿度を取得し WBGT に換算します。
#
#                                               Copyright (c) 2024 Wataru KUNINO
################################################################################

sht31 = 0x44                                        # sht31 = 0x44 又は 0x45

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
temp = 0.                                           # 温度値を保持する変数
hum  = 0.                                           # 湿度値を保持する変数
wbgt = 0.                                           # WGBTを保持する変数

while i2c:
    i2c.write_byte_data(sht31,0x24,0x00)
    sleep(0.018)
    data = i2c.read_i2c_block_data(sht31,0x00,6)
    if len(data) >= 5:
        temp = float(word2uint(data[0],data[1])) / 65535. * 175. - 45.
        hum  = float(word2uint(data[3],data[4])) / 65535. * 100.
        if wbgt_ver == 3 and wbgt_wide == False:
            wbgt = 0.687 * temp + 0.0360 * hum + 0.00367 * temp * hum - 2.062
        elif wbgt_ver == 3 and wbgt_wide == True:
            wbgt = 0.725 * temp + 0.0368 * hum + 0.00364 * temp * hum - 3.246
        elif wbgt_ver == 4 and wbgt_wide == False:
            wbgt = 0.724 * temp + 0.0342 * hum + 0.00277 * temp * hum - 3.007
        elif wbgt_ver == 4 and wbgt_wide == True:
            wbgt = 0.754 * temp + 0.0382 * hum + 0.00264 * temp * hum - 3.965
        print("Temp. = %.2f ℃, Humid. = %.0f ％" % (temp,hum),end='')
        print(", WBGT = %.2f ℃" % wbgt)
    sleep(1)

''' ----------------------------------------------------------------------------
参考文献1
  Raspberry Pi で 暑さ指数 WBGT その3: ラズパイ Pico 2
  https://bokunimo.net/blog/raspberry-pi/4988/  2024年9月16日 Wataru KUNINO
--------------------------------------------------------------------------------
参考文献2
  温湿度センサ SENSIRION SHT31 から温度と湿度を取得します。
  https://github.com/bokunimowakaru/RaspberryPi/blob/master/gpio/raspi_sht31.py
                                                Copyright (c) 2021 Wataru KUNINO
--------------------------------------------------------------------------------
参考文献3
  IchigoJam S+温湿度センサSi7021で暑さ指数WBGTを計算して、熱中症予防
  https://bokunimo.net/blog/ichigo-jam/29/      2018年8月11日 Wataru KUNINO
---------------------------------------------------------------------------- '''
