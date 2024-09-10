import qrcode

# URL вашего Django-приложения
url = 'http://192.168.1.108:8000'

# Генерация QR-кода
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Создание изображения QR-кода
img = qr.make_image(fill_color="black", back_color="white")

# Сохранение изображения
img.save("django_qr_code.png")
