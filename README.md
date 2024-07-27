# wgbt
Pseudo WGBT Feeling Temperature Measurement

## Supported Devices

- [Raspberry Pi](https://github.com/bokunimowakaru/wgbt/blob/master/raspi)
- [IchigoJam](https://github.com/bokunimowakaru/wgbt/blob/master/ichigojam)

## Calculate the heat index WBGT

### What is the heat index WBGT?

WBGT; Wet Bulb Globe Temperature is one of the internationally standardized heat indexes.  
The value is in degrees Celsius, making it an easy-to-understand index. However, a special measuring device called a wet bulb globe thermometer is required to measure it.
There is also a simpler method of measuring it, which is created by the Japanese Society of Biometeorology (日本生気象学会), and estimated it from temperature and humidity. But, since there was no data below 20°C in the published table.
So, I also used data from the other WBGT estimation formula derived from meteorological data for six cities by Masashi Ono of the National Institute for Environmental Studies (国立環境研究所).

### Method of Calculation

The pseudo WGBT formula I created for indoor use is:

```
WBGT = 0.725*Ta + 0.0368*RH + 0.00364*Ta*RH – 3.246
```

- [Detail of Formula (Google Translation)](https://bokunimo-net.translate.goog/blog/ichigo-jam/29/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=ja&_x_tr_pto=wapp)  
- [Detail of Formula In Japanese](https://bokunimo.net/blog/ichigo-jam/29/)  
- [MIT LICENSE](https://github.com/bokunimowakaru/wgbt/blob/master/LICENSE)

## The Simplest Code

Which is used the bc command. It's useful for calculations on a Linux-based OS such as Raspberry Pi.
You can get a WBGT value to substitute temperature for the variable TMPL and humidity for HUM, and execute the following command.

```bash
echo “0.725 * ${TMPL} + 0.0368 * ${HUMI} + 0.00364 * ${TMPL} * ${HUMI} – 3.246″|bc
```

----------------------------------------------------------------

by Wataru KUNINO 
- Web Page [https://bokunimo.net/](https://bokunimo.net/)
- Blog Page [https://bokunimo.net/blog/](https://bokunimo.net/blog/)

----------------------------------------------------------------

## GitHub Pages  

*  (This Document)  
  [https://git.bokunimo.com/wbgt/](https://git.bokunimo.com/wbgt/)  

----------------------------------------------------------------

# git.bokunimo.com GitHub Pages site
[http://git.bokunimo.com/](http://git.bokunimo.com/)  

----------------------------------------------------------------
