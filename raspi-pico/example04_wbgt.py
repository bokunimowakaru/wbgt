################################################################################
# 温湿度センサ SENSIRION SHT31 から温度と湿度を取得し WBGT に換算します。
# for Raspberry Pi Pico / Pico W / Pico 2
#                                          Copyright (c) 2021-2024 Wataru KUNINO
################################################################################
# WBGTバージョンの違い、筆者の独自拡張(Wide版)については下記を参照ください。
# https://bokunimo.net/blog/raspberry-pi/4777/
################################################################################
# 参考文献
# ・IchigoJam S+温湿度センサSi7021で暑さ指数WBGTを計算して、熱中症予防
#   https://bokunimo.net/blog/ichigo-jam/29/      2018年8月11日 Wataru KUNINO
# ・温湿度センサ SENSIRION SHT31 から温度と湿度を取得します。
#   https://github.com/bokunimowakaru/RaspberryPi/blob/master/gpio/raspi_sht31.py
# ・https://github.com/bokunimowakaru/iot/tree/master/micropython/raspi-pico
# ・https://github.com/bokunimowakaru/pico/blob/master/examples/example04_hum_udp.py
################################################################################

# 温湿度センサ AE-SHT31 ピン接続図
##############################
#   SHT31 # Pico # GPIO
##############################
#     +V  #  5   # GP3
#    SDA  #  6   # GP4
#    SCL  #  7   # GP5
#    ADD  #  8   # GND
#    GND  #  9   # GP6
##############################

sht31 = 0x44                            # 温湿度センサSHT31のI2Cアドレス
wbgt_ver = 3                            # WBGTバージョン 3 または 4
wbgt_wide = True                        # 筆者の独自拡張Wide版

from machine import Pin,I2C             # ライブラリmachineのI2Cを組み込む
from utime import sleep                 # μtimeからsleepを組み込む

led = Pin(25, Pin.OUT)                  # GPIO出力用インスタンスledを生成
gnd = Pin(6, Pin.OUT)                   # GP6をSHT31のGNDピンに接続
gnd.value(0)                            # GND用に0Vを出力
vdd = Pin(3, Pin.OUT)                   # GP3をSHT31のV+ピンに接続
vdd.value(1)                            # V+用に3.3Vを出力
i2c = I2C(0, scl=Pin(5), sda=Pin(4))    # GP5をSHT31のSCL,GP4をSDAに接続

temp = 0.                               # 温度値を保持する変数tempを生成
hum  = 0.                               # 湿度値を保持する変数humを生成
while True:                             # 繰り返し処理
    i2c.writeto_mem(sht31,0x24,b'\x00') # SHT31にコマンド0x2400を送信する
    # i2c.writeto(sht31,b'\x24\x00')    # SHT31仕様に合わせた2バイト送信表記
    sleep(0.018)                        # SHT31の測定待ち時間
    data = i2c.readfrom_mem(sht31,0x00,6)   # SHT31から測定値6バイトを受信
    if len(data) >= 5:                  # 受信データが5バイト以上の時
        temp = float((data[0]<<8) + data[1]) / 65535. * 175. - 45.
        hum  = float((data[3]<<8) + data[4]) / 65535. * 100.
    if wbgt_ver == 3 and wbgt_wide == False:
        wbgt = 0.687 * temp + 0.0360 * hum + 0.00367 * temp * hum - 2.062
    elif wbgt_ver == 3 and wbgt_wide == True:
        wbgt = 0.725 * temp + 0.0368 * hum + 0.00364 * temp * hum - 3.246
    elif wbgt_ver == 4 and wbgt_wide == False:
        wbgt = 0.724 * temp + 0.0342 * hum + 0.00277 * temp * hum - 3.007
    elif wbgt_ver == 4 and wbgt_wide == True:
        wbgt = 0.754 * temp + 0.0382 * hum + 0.00264 * temp * hum - 3.965
    else:
        print("ERROR:WBGTバージョンが不正")

    s = str(round(temp,1))              # 小数点第1位で丸めた結果を文字列に
    print('Temperature =',s, end=', ')  # 温度値を表示
    s = str(round(hum,1))               # 小数点第1位で丸めた結果を文字列に
    print('Humidity =',s, end=', ')     # 湿度値を表示
    s = str(round(wbgt,1))              # 小数点第1位で丸めた結果を文字列に
    print('WBGT =',s)                   # WBGT値を表示
    led.value(1)                        # LEDをONにする
    sleep(0.1)                          # 0.1秒間の待ち時間処理
    led.value(0)                        # LEDをOFFにする
    sleep(5)                            # 5秒間の待ち時間処理
