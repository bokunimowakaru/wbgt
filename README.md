# WBGT
Pseudo WBGT Feeling Temperature Measurement

![Fig. Measurement Environment](https://bokunimo.net/blog/wp-content/uploads/2024/07/wbgt2.png)

## Supported Target MCU Devices

- Raspberry Pi
- IchigoJam

## Supported Sensor Devices

- Sensirion SHT31, SHT30 

## Calculate the heat index WBGT

### What is the heat index WBGT?

WBGT; Wet Bulb Globe Temperature is one of the internationally standardized heat indexes.  
The value is in degrees Celsius, making it an easy-to-understand index. However, a special measuring device called a wet bulb globe thermometer is required to measure it.
There is also a simpler method of measuring it, which is created by the Japanese Society of Biometeorology (日本生気象学会), and estimated it from temperature and humidity. But, since there was no data below 20°C in the published table.
So, I also used data from the other WBGT estimation formula derived from meteorological data for six cities by Masashi Ono of the National Institute for Environmental Studies (国立環境研究所).

### Method of Calculation

The pseudo WBGT formula I created for indoor use is:

```
WBGT = 0.725*Ta + 0.0368*RH + 0.00364*Ta*RH – 3.246
```

- [Detail of Formula (Google Translation)](https://bokunimo-net.translate.goog/blog/ichigo-jam/29/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=ja&_x_tr_pto=wapp)  
- [Detail of Formula In Japanese](https://bokunimo.net/blog/ichigo-jam/29/)  
- [How to Make it on Raspberry Pi (Google Translation)](https://bokunimo-net.translate.goog/blog/raspberry-pi/4721/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=ja&_x_tr_pto=wapp)  
- [How to Make it on Raspberry Pi in Japanese](https://bokunimo.net/blog/raspberry-pi/4721/)  
- [MIT LICENSE](https://github.com/bokunimowakaru/wbgt/blob/master/LICENSE)  

## Schematic for Connection

Connect an I2C interface of M5Stack ENV II or III Unit to the GPIO header pins on your Raspberry Pi.  

![Fig. Schematic](https://bokunimo.net/blog/wp-content/uploads/2024/07/schema.jpg)

## The Simplest Code

Which is used the bc command. It's useful for calculations on a Linux-based OS such as Raspberry Pi.
You can get a WBGT value to substitute temperature for the variable TMPL and humidity for HUM, and execute the following command.

```bash
echo "0.725 * ${TMPL} + 0.0368 * ${HUMI} + 0.00364 * ${TMPL} * ${HUMI} - 3.246"|bc
```

Example:
```bash
pi@raspberrypi:~ $ TMPL=28
pi@raspberrypi:~ $ HUMI=90
pi@raspberrypi:~ $ echo "0.725 * ${TMPL} + 0.0368 * ${HUMI} + 0.00364 * ${TMPL} * ${HUMI} - 3.246"|bc
29.53880
```

## Software on GitHub

- [Raspberry Pi](https://github.com/bokunimowakaru/wbgt/blob/master/raspi)
- [IchigoJam](https://github.com/bokunimowakaru/wbgt/blob/master/ichigojam)

----------------------------------------------------------------

## URL of This Document

- [https://git.bokunimo.com/wbgt/](https://git.bokunimo.com/wbgt/)  


## Authored by Wataru KUNINO

- Author's Web Page: [https://bokunimo.net/](https://bokunimo.net/)
- Blog Page: [https://bokunimo.net/blog/](https://bokunimo.net/blog/)
- GitHub Pages site: [http://git.bokunimo.com/](http://git.bokunimo.com/)

----------------------------------------------------------------
