# AmazonFireDebloat


This is a project for cusomizing the Amazon Firestick's homescreen. It is a rewrite of my older project [old](https://github.com/HeronErin/FuckAmz) which focused on aviary.amazon.com api. This project focuses on the ktpx.amazon.com api. This project is very much a work in progress, it is not stable, but if you are like me and hate ads, you may find it useful.

The following are some useful adb commands for playing around with the firestick.

* Start the dev menu for changing the http proxy.
```bash
adb shell am start com.amazon.ssm/com.amazon.ssm.ControlPanel
```
* Load the installer for a custom certificate authority
```bash
adb shell am start -a "android.intent.action.VIEW" -d "file:///storage/emulated/0/Download/mitmproxy-ca-cert.pem" -t "application/x-x509-ca-cert"
```
* Reboot the firestick
```bash
adb shell reboot
```
* Clear launcher data, along with resetting cache and all TTLs
```bash
adb shell pm clear com.amazon.tv.launcher
```


Kodi plugin avalible at `http://ifdh.eu.org` and act as an intent forwarder for lauching arbirary kodi builtin functions from intents



To download cookies click [here](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc?pli=1)
