import qrcode


url = 'http://192.168.1.108:8000'
url = 'http://192.168.3.24:8000'

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("django_qr_code2.png")


import qrcode

ssid = 'Keenetic-6348'
password = 'UfPFYaTH'
wifi_type = 'WPA'

wifi_data = f'WIFI:T:{wifi_type};S:{ssid};P:{password};;'

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(wifi_data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("wifi_qr_code.png")