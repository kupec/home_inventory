from fpdf import FPDF
import qrcode
import math
import sys

margin = 5
media_width = 210
media_height = 297
N = 16
qr_size = 15
gap = 10

margin = max(margin, gap)
page_width = media_width - 2 * margin
page_height = media_height - 2 * margin
cols = int((page_width + gap) / (qr_size + gap))
rows = int(math.ceil(N / cols))

urls = [line.strip() for line in sys.stdin]

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_margin(margin)
pdf.add_page()

for r in range(rows):
    if not urls:
        break

    for c in range(cols):
        if not urls:
            break
        url = urls.pop(0)

        qr = qrcode.QRCode(border=0)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()

        x = margin + c * (qr_size + gap)
        y = margin + r * (qr_size + gap)
        pdf.image(img.get_image(), x=x, y=y, w=qr_size, h=qr_size)

pdf.output('out.pdf')
